#!/usr/bin/env python3
"""
RQ1 - Table 1: Dataset Distribution

Reads the pre-computed dataset summary to reproduce Table 1.

Produces: Table 1 printed to console (identical numbers to paper).
"""

import csv
from pathlib import Path
import sys
import io

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import RQ1_DATASET_SUMMARY


def main():
    input_path = RQ1_DATASET_SUMMARY
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    # This CSV has two sections separated by a blank line
    sections = input_path.read_text(encoding="utf-8").strip().split("\n\n")

    # Parse section 1 with csv module (handles quoted commas)
    reader1 = csv.DictReader(io.StringIO(sections[0]))
    row1 = next(reader1)

    print("=" * 65)
    print("Table 1: Dataset Distribution")
    print("=" * 65)
    print(f"\n  Repositories:       {row1['number_of_repos']}")
    print(f"  Pull Requests:      {row1['number_of_prs']}")
    print(f"  Conversations:      {row1['number_of_convos']}")

    # Parse section 2: per-category counts
    reader2 = csv.DictReader(io.StringIO(sections[1]))
    print(f"\n{'Category':<25} {'Conversations':>15}")
    print("-" * 42)
    total = 0
    for row in reader2:
        cat = row['category']
        count_str = row['count']
        count_val = int(count_str.replace(",", ""))
        total += count_val
        print(f"  {cat:<23} {count_str:>15}")
    print("-" * 42)
    print(f"  {'Total':<23} {total:>15,}")


if __name__ == "__main__":
    main()
