#!/usr/bin/env python3
"""
RQ3 - Code Quality Impact Analysis
1. Outputs CSV of all 111 metrics tested (full list).
2. Prints TABLE VI: 6 statistically significant metrics grouped by category.
Produces: results/tables/RQ3_AllMetrics.csv, results/tables/RQ3_SignificantMetrics.csv
"""

import csv
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import RQ3_SIGDIFF_METRICS, TABLES_DIR

# Category mapping for significant metrics
METRIC_CATEGORIES = {
    'SumStrictModifiedCyclomaticComplexity': ('Complexity', 'Sum Strict Modified CC'),
    'SumStrictCyclomaticComplexity': ('Complexity', 'Sum Strict CC'),
    'SumModifiedCyclomaticComplexity': ('Complexity', 'Sum Modified CC'),
    'SumCyclomaticComplexity': ('Complexity', 'Sum CC'),
    'ExecutableStatements': ('Code Size', 'Executable Statements'),
    'Statements': ('Code Size', 'Statements'),
}


def main():
    input_path = RQ3_SIGDIFF_METRICS
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    with open(input_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    n_tests = len(rows)
    threshold = 0.05 / n_tests if n_tests > 0 else 0.05

    # =========================================================================
    # 1. Save full list of all metrics tested
    # =========================================================================
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    all_path = TABLES_DIR / "RQ3_AllMetrics.csv"
    with open(all_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Metric', 'P_Value', 'Significant', 'Effect_Size',
                         'Cliffs_Delta', 'Mean_Human', 'Mean_AI'])
        for row in rows:
            p = float(row['P_Value'])
            sig = 'Yes' if p < threshold else 'No'
            writer.writerow([row['Metric'], row['P_Value'], sig,
                             row['Effect_Size'], row['Cliffs_Delta'],
                             row['Mean_Human'], row['Mean_AI']])

    print(f"All {n_tests} metrics saved to {all_path}")

    # =========================================================================
    # 2. TABLE VI: Significant metrics grouped by category
    # =========================================================================
    sig_rows = [r for r in rows if float(r['P_Value']) < threshold]

    print(f"\nBonferroni threshold: p < {threshold:.6f}")
    print(f"Significant metrics: {len(sig_rows)} / {n_tests}")

    print("\n" + "=" * 75)
    print("TABLE VI: Code Quality Impact of Adopted Suggestions")
    print("=" * 75)
    print(f"\n{'Category':<12} {'Metric':<28} {'Human':>10} {'Agent':>10}")
    print(f"{'':12s} {'':28s} {'Mean D':>10} {'Mean D':>10}")
    print("-" * 75)

    # Group by category
    prev_cat = None
    for row in sig_rows:
        metric = row['Metric']
        cat, short_name = METRIC_CATEGORIES.get(metric, ('Other', metric))
        cat_display = cat if cat != prev_cat else ''
        prev_cat = cat
        h_mean = float(row['Mean_Human'])
        a_mean = float(row['Mean_AI'])
        print(f"  {cat_display:<10} {short_name:<28} {h_mean:>10.3f} {a_mean:>10.3f}")

    # Save significant metrics CSV
    sig_path = TABLES_DIR / "RQ3_SignificantMetrics.csv"
    with open(sig_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Category', 'Metric', 'Human_Mean_Delta', 'Agent_Mean_Delta',
                         'P_Value', 'Cliffs_Delta', 'Effect_Size'])
        for row in sig_rows:
            metric = row['Metric']
            cat, short_name = METRIC_CATEGORIES.get(metric, ('Other', metric))
            writer.writerow([cat, short_name,
                             row['Mean_Human'], row['Mean_AI'],
                             row['P_Value'], row['Cliffs_Delta'],
                             row['Effect_Size']])

    print(f"\nSignificant metrics saved to {sig_path}")


if __name__ == "__main__":
    main()
