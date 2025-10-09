#!/usr/bin/env python3
"""
rf_scanner.py - 433MHz Scanner/Logger mit MQTT via mosquitto_pub

- Läuft im Vordergrund
- CSV-Logging
- MQTT: einzelne Datenpunkte pro Code für iobroker
- Events unter rcscan/event (Code im Payload)
- None-Signale werden ignoriert
"""
import argparse, time, csv, signal, os, shlex, subprocess
from datetime import datetime
from rpi_rf import RFDevice

# ---------------- CLI ----------------
parser = argparse.ArgumentParser(description="433MHz Scanner/Logger mit MQTT via mosquitto_pub")
parser.add_argument("--gpio", "-g", type=int, default=27, help="BCM GPIO für RX (default: 27)")
parser.add_argument("--outfile", "-o", default="~/rf_senders.csv", help="CSV-Datei")
parser.add_argument("--interval", "-i", type=int, default=300, help="Sekunden: wie oft CSV geschrieben wird")
parser.add_argument("--verbose", "-v", action="store_true", help="mehr Konsolenausgaben")
parser.add_argument("--mqtt-broker", default="192.168.1.1", help="MQTT Broker IP")
parser.add_argument("--mqtt-port", type=int, default=1883, help="MQTT Port")
args = parser.parse_args()

OUTFILE = os.path.expanduser(args.outfile)
GPIO = args.gpio
FLUSH_INTERVAL = max(5, args.interval)
MQTT_BROKER = args.mqtt_broker
MQTT_PORT = args.mqtt_port

found = {}  # key=(code,proto,pulselength)

running = True
def sigint_handler(sig, frame):
    global running
    running = False
signal.signal(signal.SIGINT, sigint_handler)

def now_ts():
    return datetime.utcnow().isoformat(sep=' ', timespec='seconds') + "Z"

# ---------------- MQTT via mosquitto_pub ----------------
def mosquitto_pub(topic, payload):
    cmd = f"mosquitto_pub -h {MQTT_BROKER} -p {MQTT_PORT} -t {shlex.quote(topic)} -m {shlex.quote(payload)}"
    try:
        subprocess.call(cmd, shell=True)
    except Exception as e:
        if args.verbose:
            print(f"[{now_ts()}] mosquitto_pub failed: {e}")

def mqtt_publish_state(code, proto, pl, stats):
    """
    Sendet 6 einzelne Datenpunkte per MQTT für iobroker:
     - date (YYYY-MM-DD)
     - time (HH:MM:SS)
     - code
     - proto
     - pulselength
     - count
    """
    base_topic = f"rcscan/code/{code}"

    # last_seen im Format "YYYY-MM-DD HH:MM:SSZ" -> split in date / time (ohne Z)
    last_seen = stats.get("last_seen", "")
    date_part = ""
    time_part = ""
    if last_seen:
        parts = last_seen.split()
        if len(parts) >= 1:
            date_part = parts[0]
        if len(parts) >= 2:
            time_part = parts[1].rstrip("Z")

    mosquitto_pub(f"{base_topic}/date", date_part)
    mosquitto_pub(f"{base_topic}/time", time_part)
    mosquitto_pub(f"{base_topic}/code", str(code))
    mosquitto_pub(f"{base_topic}/proto", str(proto))
    mosquitto_pub(f"{base_topic}/pulselength", str(pl))
    mosquitto_pub(f"{base_topic}/count", str(stats.get("count", 0)))

def mqtt_publish_event(code, proto, pl, timestamp):
    """
    Einfaches Event unter einem Topic mit Code im Payload:
    payload = code,proto,pulselength,timestamp
    """
    topic = "rcscan/event"
    payload = f"{code},{proto},{pl},{timestamp}"
    mosquitto_pub(topic, payload)

# ---------------- CSV Logging ----------------
def write_csv():
    header = ["code","proto","pulselength","first_seen_utc","last_seen_utc","count"]
    write_header = not os.path.exists(OUTFILE) or os.path.getsize(OUTFILE) == 0
    try:
        with open(OUTFILE, "a", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow(header)
            for (code, proto, pl), stats in sorted(found.items(), key=lambda kv: -kv[1]["count"]):
                w.writerow([code, proto, pl, stats["first_seen"], stats["last_seen"], stats["count"]])
    except Exception as e:
        print(f"Error writing CSV: {e}")

def print_summary():
    total_codes = len(found)
    total_events = sum(v["count"] for v in found.values())
    print(f"[{now_ts()}] Summary: unique_codes={total_codes}, total_events={total_events}")
    if args.verbose and total_codes:
        top = sorted(found.items(), key=lambda kv: -kv[1]["count"])[:10]
        for (code, proto, pl), st in top:
            print(f"  Code={code} proto={proto} pl={pl} count={st['count']} first={st['first_seen']} last={st['last_seen']}")

# ---------------- RF Device ----------------
rf = RFDevice(GPIO)
rf.enable_rx()
print(f"[{now_ts()}] Scanner gestartet auf GPIO {GPIO}. Schreibe alle {FLUSH_INTERVAL}s nach {OUTFILE}")
last_flush = time.time()

try:
    while running:
        if rf.rx_code_timestamp != 0:
            code = rf.rx_code
            proto = rf.rx_proto
            pl = rf.rx_pulselength

            # ---------------- None-Signale ignorieren ----------------
            if code is None:
                if args.verbose:
                    print(f"[{now_ts()}] INCOMPLETE signal ignored (code None). proto={proto} pl={pl}")
                rf.rx_code_timestamp = 0
                continue

            code_s = str(code)
            proto_i = int(proto) if proto is not None else 0
            pl_i = int(pl) if pl is not None else 0

            key = (code_s, proto_i, pl_i)
            t = now_ts()

            if key not in found:
                found[key] = {"first_seen": t, "last_seen": t, "count": 1}
                if args.verbose:
                    print(f"[{t}] NEW: Code={code_s} proto={proto_i} pl={pl_i}")
            else:
                found[key]["last_seen"] = t
                found[key]["count"] += 1
                if args.verbose:
                    print(f"[{t}] SEEN: Code={code_s} proto={proto_i} pl={pl_i} count={found[key]['count']}")

            # ---------------- MQTT ----------------
            mqtt_publish_event(code_s, proto_i, pl_i, t)
            mqtt_publish_state(code_s, proto_i, pl_i, found[key])

            rf.rx_code_timestamp = 0

        if time.time() - last_flush >= FLUSH_INTERVAL:
            write_csv()
            print_summary()
            last_flush = time.time()

        time.sleep(0.02)

except Exception as e:
    print("Fehler im Scanner:", e)

finally:
    print("\nBeende Scanner, schreibe finale CSV...")
    write_csv()
    print_summary()
    try:
        rf.cleanup()
    except:
        pass
    print("Fertig.")
