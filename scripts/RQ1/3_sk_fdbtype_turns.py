#!/usr/bin/env python3
"""
RQ1 - Table III: Scott-Knott ESD Rankings of Feedback Types by Discussion Rounds

Reads pre-computed SK ranking data and produces Table III.

Produces: results/tables/RQ1_sk_fdbtype_turns.csv
"""

import csv
import io
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import RQ1_SK_FDBTYPE_TURNS, TABLES_DIR

CATEGORIES = ["HRH", "HRA", "ARH", "ARA"]


def main():
    input_path = RQ1_SK_FDBTYPE_TURNS
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    raw = input_path.read_text(encoding="utf-8")
    reader = csv.DictReader(io.StringIO(raw))
    rows = list(reader)

    # Print formatted table
    print("=" * 100)
    print("Table III: Scott-Knott ESD Rankings of Feedback Types by Discussion Rounds")
    print("=" * 100)

    header = f"{'Feedback Type':<22}"
    for cat in CATEGORIES:
        header += f" {'R':>3} {'AvgC':>5} {'>1C':>5} |"
    print(f"\n{'':<22} {'HRH':^15}| {'HRA':^15}| {'ARH':^15}| {'ARA':^15}")
    print(f"{'Feedback Type':<22} {'R':>3} {'AvgC':>5} {'>1C':>5} | {'R':>3} {'AvgC':>5} {'>1C':>5} | {'R':>3} {'AvgC':>5} {'>1C':>5} | {'R':>3} {'AvgC':>5} {'>1C':>5}")
    print("-" * 100)

    for row in rows:
        ft = row["FeedbackType"]
        line = f"  {ft:<20}"
        for cat in CATEGORIES:
            r = row.get(f"{cat}_R", "").strip()
            avgc = row.get(f"{cat}_AvgC", "").strip()
            gt1c = row.get(f"{cat}_GT1C", "").strip()
            if r:
                line += f" {r:>3} {avgc:>5} {gt1c:>5} |"
            else:
                line += f" {'-':>3} {'-':>5} {'-':>5} |"
        print(line)

    print("-" * 100)

    # Save as CSV for replication
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = TABLES_DIR / "RQ1_sk_fdbtype_turns.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header_row = ["FeedbackType"]
        for cat in CATEGORIES:
            header_row.extend([f"{cat}_R", f"{cat}_AvgC", f"{cat}_GT1C"])
        writer.writerow(header_row)
        for row in rows:
            out_row = [row["FeedbackType"]]
            for cat in CATEGORIES:
                out_row.append(row.get(f"{cat}_R", "").strip() or "-")
                out_row.append(row.get(f"{cat}_AvgC", "").strip() or "-")
                out_row.append(row.get(f"{cat}_GT1C", "").strip() or "-")
            writer.writerow(out_row)

    print(f"\nTable III saved as {output_path}")


if __name__ == "__main__":
    main()
