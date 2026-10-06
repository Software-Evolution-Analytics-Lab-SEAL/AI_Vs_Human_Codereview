#!/usr/bin/env python3
"""
RQ3 - Table 6: Suggestion Adoption Rates by Feedback Type
Reads pre-computed adoption rates from aggregated results.
Produces: Table 6 in the paper (identical numbers).
"""

import csv
import io
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import RQ3_ADOPTION_BY_FEEDTYPE, RESULTS_DIR


def main():
    input_path = RQ3_ADOPTION_BY_FEEDTYPE
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    raw = input_path.read_text(encoding='utf-8')
    reader = csv.DictReader(io.StringIO(raw))
    rows = list(reader)

    # Print table matching paper TABLE IV format: Human first, then Agent, then vs.Human
    print("=" * 80)
    print("TABLE IV: Suggestion Adoption Rates by Feedback Type")
    print("=" * 80)
    print(f"\n{'Feedback Type':<25} {'Human':^20s} {'Agent':^30s}")
    print(f"{'':25s} {'#Sugg.':>8} {'Adopt':>8}   {'#Sugg.':>8} {'Adopt':>8} {'vs.Human':>10}")
    print("-" * 80)

    for row in rows:
        ft = row['FeedType']
        h_sug = row['HSug'] if row['HSug'] != '-' else '-'
        h_adopt = row['HAdopt'] if row['HAdopt'] != '-' else '-'
        a_sug = row['ASug'] if row['ASug'] != '-' else '-'
        a_adopt = row['AAdopt'] if row['AAdopt'] != '-' else '-'
        diff = row['Diff'] if row['Diff'] != '-' else '-'
        print(f"  {ft:<23} {h_sug:>8} {h_adopt:>8}   {a_sug:>8} {a_adopt:>8} {diff:>10}")

    # Save output CSV
    output_dir = RESULTS_DIR / "tables"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "RQ3_AdoptionRates.csv"
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Feedback_Type', 'Human_Sugg', 'Human_Adopt',
                         'Agent_Sugg', 'Agent_Adopt', 'vs_Human'])
        for row in rows:
            writer.writerow([row['FeedType'],
                             row['HSug'], row['HAdopt'],
                             row['ASug'], row['AAdopt'],
                             row['Diff']])

    print(f"\nTable saved as {output_path}")


if __name__ == "__main__":
    main()
