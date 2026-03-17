#!/usr/bin/env python3
"""
RQ2 - Table: Average Comment Count (AvgC) by Review Category and Outcome
Reads pre-computed table to reproduce the paper's exact numbers.
Produces: results/tables/RQ2_AvgDuration.csv

Adapted from: RQ2/1_allturns/8_2_generate_avg_duration_table.py
"""

import csv
import io
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import RQ2_TABLE_IV, TABLES_DIR


def main():
    input_path = RQ2_TABLE_IV
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    raw = input_path.read_text(encoding='utf-8')
    reader = csv.DictReader(io.StringIO(raw))
    rows = list(reader)

    # Print table
    print("=" * 50)
    print("Table: Average Comment Count (AvgC) by Review Category and Outcome")
    print("=" * 50)
    print(f"\n{'Category':<10} {'AvgC':>8} {'vs HRH':>10} "
          f"{'in ACC':>8} {'in REJ':>8}")
    print("-" * 50)

    for row in rows:
        cat = row['Category']
        vs_hrh = row['Total_Delta'] if row['Total_Delta'] != '-' else ''
        print(f"  {cat:<8} {row['Total_ATC']:>8} {vs_hrh:>10} "
              f"{row['ACC_ATC']:>8} {row['REJ_ATC']:>8}")

    # Save output CSV
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = TABLES_DIR / "RQ2_AvgDuration.csv"
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Category', 'AvgC', 'vs_HRH',
                         'in_ACC', 'in_REJ'])
        for row in rows:
            writer.writerow([row['Category'],
                             row['Total_ATC'], row['Total_Delta'],
                             row['ACC_ATC'], row['REJ_ATC']])

    print(f"\nTable saved as {output_path}")


if __name__ == "__main__":
    main()
