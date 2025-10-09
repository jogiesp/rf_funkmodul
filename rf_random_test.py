#!/usr/bin/env python3
import random
import subprocess
import time

GPIO = 17        # TX GPIO
REPEAT = 5       # Wiederholungen pro Code
NUM_CODES = 200  # Anzahl zufälliger Codes
SLEEP = 0.05     # Pause zwischen den Sends (Sekunden)

for i in range(NUM_CODES):
    code = random.randint(1, 9999999)      # Zufalls-Code
    proto = random.randint(1, 5)           # Protocol 1–5
    pl = random.randint(100, 1000)         # Pulselength
    print(f"[{i+1}/{NUM_CODES}] Sende Code={code} proto={proto} pl={pl}")
    cmd = f"sudo rpi-rf_send -g {GPIO} -p {pl} -t {proto} -r {REPEAT} {code}"
    subprocess.call(cmd, shell=True)
    time.sleep(SLEEP)

print("Fertig: 200 zufällige Codes gesendet!")
