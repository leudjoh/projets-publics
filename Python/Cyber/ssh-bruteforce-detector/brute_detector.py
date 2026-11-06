import argparse
import csv
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


def read_file(path):
    path = Path(path)
    text = path.read_text()
    lines = text.splitlines()
    return lines


def extract_ips(lines):
    ips = []
    for line in lines:
        words = line.split()
        if "from" in words:
            position = words.index("from") + 1
            ip = words[position]
            ips.append(ip)
    return ips


def count_ip(ips):
    ips_count = Counter(ips)
    return ips_count


def analysis_time():
    date = datetime.now().isoformat(timespec="seconds")
    return date


parser = argparse.ArgumentParser(
    description="compte le nombre d'apparition d'IP dans un fichier de logs"
)
parser.add_argument("path", help="le chemin du fichier à analyser")
parser.add_argument("--force", help="écraser les anciens rapports", action="store_true")
parser.add_argument(
    "--threshold",
    type=int,
    default=1,
    help="nombre minimum comptés pour l'affichage d'une IP",
)
args = parser.parse_args()
path = args.path
try:
    lines = read_file(path)
except FileNotFoundError:
    print(f"le fichier \"{path}\" n'existe pas ou n'a pas été trouvé")
    sys.exit(1)
ips = extract_ips(lines)
ips_count = count_ip(ips)
filtered = []
date = analysis_time()
report = f"Analysis date: {date}\nRapport de comptage d'ip sur le fichier {path} :\n"
json_report = []
for counted_ip in ips_count.most_common():
    if counted_ip[1] >= args.threshold:
        filtered.append(counted_ip)
        report += f"{counted_ip[0]}, {counted_ip[1]}x\n"
        json_report.append(
            {"ip": counted_ip[0], "count": counted_ip[1], "analysis_date": date}
        )
path_json = Path(path).parent / "report.json"
path_report = Path(path).parent / "report.txt"
path_csv = Path(path).parent / "report.csv"
if not args.force and (path_report.exists() or path_csv.exists() or path_json.exists()):
    print(
        f"Pas de rapports générés :\nLe(s) fichier(s) {path_report}, {path_csv} et {path_json} déjà présent(s), utiliser --force pour écraser."
    )
    sys.exit(1)
print(report, end="")
path_report.write_text(report)
json_text = json.dumps(json_report, indent=4)
path_json.write_text(json_text)
with open(path_csv, "w", newline="") as report_csv:
    writer = csv.writer(report_csv)
    writer.writerow(["ip", "count", "analysis_date"])
    for filtered_ip in filtered:
        writer.writerow([filtered_ip[0], filtered_ip[1], date])
