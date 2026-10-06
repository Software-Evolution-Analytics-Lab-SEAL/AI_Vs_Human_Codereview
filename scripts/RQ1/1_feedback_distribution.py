#!/usr/bin/env python3
"""
RQ1 - Figure 3: Feedback Type Distribution (Stacked Bar Chart)

Reads the pre-computed aggregated summary and produces Figure 3.
Uses the EXACT SAME plotting code as the original RQ1/3_3_plot_comment_taxno.py.

Produces: results/figures/RQ1_comment_taxno.jpeg
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
import os
import argparse
from pathlib import Path
import sys
import io

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import AGG_RQ1, FIGURES_DIR


def main():
    parser = argparse.ArgumentParser(description='Plot feedback type distributions')
    parser.add_argument('--show-N', type=int, default=0, choices=[0, 1],
                        help='Show N (count) in labels: 0=hide (default), 1=show')
    args = parser.parse_args()
    show_n = bool(args.show_N)

    # =========================================================================
    # DATA LOADING: Read pre-computed aggregated summary
    # =========================================================================
    summary_path = AGG_RQ1 / "3_2_summary_feedtype.csv"
    if not summary_path.exists():
        print(f"ERROR: {summary_path} not found")
        return

    # Parse only the first section (raw counts before "Method" line)
    raw_lines = summary_path.read_text(encoding="utf-8").split("\n")
    count_lines = []
    for line in raw_lines:
        if line.startswith("Method,") or line.strip() == "":
            break
        count_lines.append(line)

    count_csv = "\n".join(count_lines)
    df_counts = pd.read_csv(io.StringIO(count_csv), thousands=",", dtype={"feed_type": str})
    df_counts = df_counts[df_counts["feed_type"] != "Total"]

    # Reconstruct row-level DataFrame for the original plotting code
    category_cols = [c for c in df_counts.columns if c not in ("feed_type", "Total")]
    rows = []
    for _, row in df_counts.iterrows():
        ft = row["feed_type"]
        for cat_col in category_cols:
            count = int(row[cat_col])
            for _ in range(count):
                rows.append({"review_category": cat_col, "feed_type": ft, "repo": "x"})

    df = pd.DataFrame(rows)
    print(f"Reconstructed {len(df):,} rows from aggregated summary")

    # =========================================================================
    # EXACT PLOTTING CODE FROM RQ1/3_3_plot_comment_taxno.py
    # =========================================================================

    df = df.dropna(subset=['repo', 'review_category', 'feed_type'])
    mapping = {
        'Agent_Review_Agent': 'ARA',
        'Agent_Review_Human': 'ARH',
        'Human_Review_Human': 'HRH',
        'Human_Review_Agent': 'HRA',
    }
    df['cat4'] = df['review_category'].map(mapping)
    df = df[df['cat4'].isin(['ARA', 'ARH', 'HRH', 'HRA'])]

    # Exclude "Review Tool" feedback type
    initial_count = len(df)
    df = df[df['feed_type'] != 'Review Tool']
    filtered_count = initial_count - len(df)
    if filtered_count > 0:
        print(f"Excluded {filtered_count} 'Review Tool' entries from analysis")

    if df.empty:
        print("ERROR: No valid rows after filtering.")
        return

    desired_order = ['ARA', 'ARH', 'HRH', 'HRA']

    df_detail = df.copy()
    df_detail['cat4'] = df_detail['review_category'].map(mapping)
    df_detail = df_detail[df_detail['cat4'].isin(desired_order)]

    # Build pivot: rows=cat4, cols=feed_type, values=count
    pivot = df_detail.pivot_table(index='cat4', columns='feed_type', values='repo', aggfunc='count', fill_value=0)
    pivot = pivot.reindex(desired_order).fillna(0)

    # Percent within each group
    percent = pivot.apply(lambda row: row / row.sum() * 100 if row.sum() > 0 else row, axis=1)

    # Format group labels
    group_counts = pivot.sum(axis=1)
    if show_n:
        formatted_labels = [f"{cat}\nN={int(n):,}" for cat, n in zip(percent.index, group_counts)]
    else:
        formatted_labels = [f"{cat}" for cat in percent.index]

    plt.figure(figsize=(12, 4))
    ax = plt.gca()
    left = np.zeros(len(percent))
    custom_colors = [
        '#5aa3e8',  # Lighter blue for Code Improvement
        '#aec7e8',  # Light blue for Defects
        '#ff7f0e',  # Orange for External Impact
        '#ffbb78',  # Light orange for Knowledge Transfer
        '#2ca02c',  # Green for Misc
        '#98df8a',  # Light green for No feedback
        '#d62728',  # Red for Social Communication
        '#ff9896',  # Light red/pink for Testing
        '#9467bd',  # Purple for Understanding
    ]
    colors = custom_colors
    y_positions = np.arange(len(percent))
    for i, feed in enumerate(percent.columns):
        ax.barh(y_positions, percent[feed].values, left=left, height=0.525,
                label=feed, color=colors[i % len(colors)])
        left = left + percent[feed].values

    # Percentage labels centered on each segment
    for idx, cat in enumerate(percent.index):
        cum_left = 0.0
        for i, feed in enumerate(percent.columns):
            width = float(percent.iloc[idx][feed])
            if width >= 5:
                ax.text(cum_left + width / 2.0, idx, f"{width:.0f}%",
                        va='center', ha='center', fontsize=18, fontweight='bold', color='black')
            cum_left += width

    ax.set_yticks(y_positions)
    ax.set_yticklabels(formatted_labels, fontweight='bold')
    ax.tick_params(axis='y', pad=15)
    ax.invert_yaxis()
    ax.set_xlabel('Conversations %', fontsize=16, fontweight='bold')
    ax.set_ylabel('')
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=100))
    ax.set_xlim(0, 100)
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    plt.setp(ax.get_xticklabels(), fontsize=16, weight='bold')
    plt.setp(ax.get_yticklabels(), fontsize=20, weight='bold',
             ha='center', va='center', multialignment='center')
    leg = ax.legend(title='Comment Types', bbox_to_anchor=(1.0, 1.15), loc='upper left', frameon=False, prop={'size': 18, 'weight': 'bold'}, labelspacing=0.4, handlelength=0.8, handletextpad=0.5)
    if leg is not None:
        leg.get_title().set_fontsize(18)
        leg.get_title().set_fontweight('bold')
    ax.spines['left'].set_position(('data', 0))
    plt.tight_layout()

    # Save figure
    os.makedirs(FIGURES_DIR, exist_ok=True)
    png_path = os.path.join(FIGURES_DIR, 'RQ1_comment_taxno.jpeg')
    plt.savefig(png_path)
    print(f'Figure 3 saved as {png_path}')


if __name__ == '__main__':
    main()
