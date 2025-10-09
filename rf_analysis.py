#!/usr/bin/env python3
import csv
from collections import defaultdict, Counter

CSV_FILE = "/home/pi/rf_senders.csv"
TOP_N = 20  # Anzahl Top-Codes, die angezeigt werden

# Data-Strukturen
counts_per_code = Counter()
pl_proto_per_code = defaultdict(Counter)

# CSV einlesen
with open(CSV_FILE, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        code = row["code"]
        proto = row["proto"]
        pl = row["pulselength"]
        count = int(row.get("count", 1))
        counts_per_code[code] += count
        pl_proto_per_code[code][(proto, pl)] += count

# Ausgabe Top-Codes
print(f"\nTop {TOP_N} Codes nach Anzahl empfangener Events:")
print(f"{'Code':>10} | {'Events':>6} | {'häufigstes proto/pl':>20}")
print("-"*45)
for code, total_count in counts_per_code.most_common(TOP_N):
    most_common_pl_proto, freq = pl_proto_per_code[code].most_common(1)[0]
    proto, pl = most_common_pl_proto
    print(f"{code:>10} | {total_count:>6} | proto={proto} pl={pl} ({freq} mal)")

# Gesamtstatistik
total_events = sum(counts_per_code.values())
total_unique_codes = len(counts_per_code)
print(f"\nGesamt empfangene Events: {total_events}")
print(f"Einzigartige Codes: {total_unique_codes}\n")
