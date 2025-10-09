# 🛸 RF Funkmodul Deluxe – Rettet die 433 MHz Welt!

> **Achtung!** ⚠️  
> Dieses Projekt ist so **wichtig**, dass es das Gleichgewicht des Universums beeinflusst.  
> Wer hier nicht sauber GPIO 27 & 17 benutzt, riskiert, dass sein Kaffee kalt wird und die Maus im Keller die Weltherrschaft übernimmt.

---

## 🔥 Was ist das?

`rf_funkmodul` ist **das ultimative 433 MHz Scanner- und Test-Toolkit** für Raspberry Pi 64‑Bit:

- **`rf_scanner.py`** – Lauscht wie ein Geheimagent auf allen 433 MHz Signalen. Speichert alles, was piept, blubbert oder klickt.  
- **`rf_analysis.py`** – Macht Ordnung im Chaos. Analysiert die empfangenen Codes und zeigt die Top‑Codes an.  
- **`rf_random_test.py`** – Für waghalsige Experimente. Sendet zufällige Codes ins Äther‑Universum und beobachtet, wie das System reagiert.

---

## ⚙️ Installation (für Mutige & Sparsame)

```bash
# Update dein System – sonst rebelliert es!
sudo apt update
sudo apt install -y python3 python3-pip mosquitto-clients git

# Rpi-RF installieren (geheimes Funkwerkzeug für Agenten)
sudo pip3 install rpi-rf

    Hinweis: Wer das nicht installiert, wird niemals die geheimen Signale der Fernbedienungen entschlüsseln.

🚀 Starten
Scanner starten (empfängt alles, was piept)

sudo python3 rf_scanner.py --gpio 27 --outfile ~/rf_senders.csv --interval 300 --verbose

    Lauscht auf GPIO 27 – sonst rebellieren die Funkdosen.

    CSV‑Log wird alle 5 Minuten geschrieben, damit auch die faule Katze alles nachlesen kann.

Codes senden (für mutige Tests)

sudo rpi-rf_send -g 17 -p 329 -t 1 -r 10 4199697

    GPIO 17 – Sender.

    -r 10 wiederholt den Code 10 Mal (manche Steckdosen brauchen Wiederholung).

📡 MQTT Integration (für ioBroker‑Helden)

    Alles, was empfangen wird, kann via MQTT an deinen Broker gesendet werden.

    Standard‑Broker‑IP (Beispiel): 192.168.1.1

    Topics:

        Events: rcscan/event (Payload: code,proto,pulselength,timestamp)

        State: rcscan/code/<code>/<field> (z. B. rcscan/code/4199697/count)

Beispiel:

mosquitto_sub -h 192.168.1.1 -t "rcscan/event" -v
mosquitto_sub -h 192.168.1.1 -t "rcscan/code/4199697/#" -v

🧰 Tools & Scripts im Repo

    rf_scanner.py — Hauptscanner (CSV + MQTT via mosquitto_pub)

    rf_analysis.py — einfache Auswertung (Top‑Codes & beste proto/pulselength)

    rf_random_test.py — sendet zufällige Codes (zum Testen)

🐭 Sicherheits‑ & Hausmeister‑Hinweise

    Achte auf Mäuse. Sie beobachten dich heimlich.

    Schütze Kabel vor Nageattacken (Kabelkanal verwenden).

    Respektiere die Funkfrequenzen — nicht die Nachbarn stören.

    Bei Dauerbetrieb: gelegentlich tail -n 200 ~/rf_senders.csv prüfen.

🧾 Lizenz

MIT — weil das Leben zu kurz für komplizierte Lizenzen ist.
🎩 Epilog (sehr wichtig & ein bisschen albern)

Wenn du dieses Repo benutzt hast und dein Empfänger wieder munter ist:

    Trink einen Kaffee (oder Tee).

    Sag „Hallo“ zur Maus (freundlich).

    Erzähle einem Freund von deinem Triumph über 32→64‑Bit‑Albträume.

Viel Spaß beim Funk‑Tüfteln! 🚀
