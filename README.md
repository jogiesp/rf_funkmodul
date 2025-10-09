# 🛸 RF Funkmodul Deluxe – Rettet die 433 MHz Welt!

> **Achtung!** ⚠️
> Dieses Projekt ist so **wichtig**, dass es das Gleichgewicht des Universums beeinflusst.
> Wer hier nicht sauber GPIO 27 & 17 benutzt, riskiert, dass sein Kaffee kalt wird und die Maus im Keller die Weltherrschaft übernimmt.

---

## 🔥 Was ist das?

`rf_funkmodul` ist **das ultimative 433 MHz Scanner- und Test-Toolkit** für Raspberry Pi 64‑Bit — und ja: jetzt **auch zum Steuern von Funksteckdosen**.

* **`rf_scanner.py`** – Lauscht wie ein Geheimagent auf allen 433 MHz Signalen. Speichert alles, was piept, blubbert oder klickt.
* **`rf_analysis.py`** – Macht Ordnung im Chaos. Analysiert die empfangenen Codes und zeigt die Top‑Codes an.
* **`rf_random_test.py`** – Für waghalsige Experimente. Sendet zufällige Codes ins Äther‑Universum und beobachtet, wie das System reagiert.
* **Neu: `rf_sender.py` / rpi-rf_send-Beispiele** – Sendet erkannte Codes gezielt, z. B. um Funksteckdosen zu schalten (funktioniert auf 64‑Bit Raspberry Pi).

---

## 🔌 Neue Funktion: Funksteckdosen steuern (jetzt mit 64‑Bit Support)

Du kannst mit diesem Projekt jetzt nicht nur abhören — du kannst auch **schalten**. Ablauf (kurz & knackig):

1. **Code erfassen:** Starte den Scanner und drücke die Taste an deiner Funkfernbedienung. Notiere `code`, `proto` und `pulselength` aus der CSV oder dem Scanner‑Output.

```bash
sudo python3 rf_scanner.py --gpio 27 --outfile ~/rf_senders.csv --interval 60 --verbose
```

2. **Code prüfen/analysieren:** Mit `rf_analysis.py` findest du die häufigsten/zuverlässigsten Codes.

```bash
python3 rf_analysis.py ~/rf_senders.csv
```

3. **Code senden (testen):**

Beispiel mit dem mitgelieferten CLI‑Tool `rpi-rf_send` (sollte mit `rpi-rf` installiert sein):

```bash
# Beispiel: sende Code 4199697 via GPIO 17, verwende protocol/pulselength falls nötig
sudo rpi-rf_send -g 17 -p 329 -t 1 -r 10 4199697
```

* `-g 17` — Pin für Sender (GPIO 17).
* `-p 329` — (optional) Pulselength / Protokollparameter — oft notwendig, damit die Steckdose den Code versteht.
* `-r 10` — Wiederholungen (einige Steckdosen brauchen mehrere Wiederholungen).

4. **Python‑Variante (kleines Script):**

```python
# rf_sender.py — einfaches Beispiel mit rpi_rf
from rpi_rf import RFDevice
import time

rf = RFDevice(17)
rf.enable_tx()
try:
    code = 4199697        # vom Scanner erfasst
    pulselength = 329     # optional, vom Scanner empfohlen
    proto = 1             # falls bekannt
    for _ in range(10):
        rf.tx_code(code, proto=proto, pulselength=pulselength)
        time.sleep(0.1)
finally:
    rf.cleanup()
```

---

## 🎬 Video (Prinzipübertragbar)

Es gibt ein älteres, aber sehr nützliches Video, das das Prinzip zeigt — auch wenn es sich auf ein anderes Projekt bezieht, lässt sich das Vorgehen 1:1 übertragen:
[https://www.youtube.com/watch?v=rSnYOeeKrS8&t=250s](https://www.youtube.com/watch?v=rSnYOeeKrS8&t=250s)

Schau dir das an, wenn du lieber eine visuelle Schritt‑für‑Schritt‑Erklärung möchtest. (Spoiler: Kaffee wird zwischendurch gemopst.)

---

## ⚙️ Installation (für Mutige & Sparsame)

```bash
# Update dein System – sonst rebelliert es!
sudo apt update
sudo apt install -y python3 python3-pip mosquitto-clients git

# Rpi-RF installieren (geheimes Funkwerkzeug für Agenten)
sudo pip3 install rpi-rf
```

**Hinweis:** Wer das nicht installiert, wird niemals die geheimen Signale der Fernbedienungen entschlüsseln.

🚀 **Starten**

Scanner starten (empfängt alles, was piept):

```bash
sudo python3 rf_scanner.py --gpio 27 --outfile ~/rf_senders.csv --interval 300 --verbose
```

Codes senden (für mutige Tests):

```bash
sudo rpi-rf_send -g 17 -p 329 -t 1 -r 10 4199697
```

📡 **MQTT Integration (für ioBroker‑Helden)**

Alles, was empfangen wird, kann via MQTT an deinen Broker gesendet werden.

Standard‑Broker‑IP (Beispiel): `192.168.1.1`

Topics:

```
Events: rcscan/event (Payload: code,proto,pulselength,timestamp)
State: rcscan/code/<code>/<field> (z. B. rcscan/code/4199697/count)
```

Beispiel:

```bash
mosquitto_sub -h 192.168.1.1 -t "rcscan/event" -v
mosquitto_sub -h 192.168.1.1 -t "rcscan/code/4199697/#" -v
```

---

## 🧰 Tools & Scripts im Repo

* `rf_scanner.py` — Hauptscanner (CSV + MQTT via mosquitto_pub)
* `rf_analysis.py` — einfache Auswertung (Top‑Codes & beste proto/pulselength)
* `rf_random_test.py` — sendet zufällige Codes (zum Testen)
* `rf_sender.py` — **neu**: Beispielskript zum Senden von Codes (siehe oben)

---

## 🐭 Sicherheits‑ & Hausmeister‑Hinweise

* Achte auf Mäuse. Sie beobachten dich heimlich.
* Schütze Kabel vor Nageattacken (Kabelkanal verwenden).
* Respektiere die Funkfrequenzen — **stör nicht die Nachbarn**. Wenn du fremde Geräte schaltest, bist du kein Hero, du bist ein Problem.
* Bei Dauerbetrieb: gelegentlich `tail -n 200 ~/rf_senders.csv` prüfen.

---

## 🧾 Lizenz

MIT — weil das Leben zu kurz für komplizierte Lizenzen ist.

---

## 🎩 Epilog (sehr wichtig & ein bisschen albern)

Wenn du dieses Repo benutzt hast und dein Empfänger wieder munter ist:

* Trink einen Kaffee (oder Tee).
* Sag „Hallo“ zur Maus (freundlich).
* Erzähle einem Freund von deinem Triumph über 32→64‑Bit‑Albträume.

Viel Spaß beim Funk‑Tüfteln! 🚀
