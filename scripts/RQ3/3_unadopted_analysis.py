#!/usr/bin/env python3
"""
RQ3 - Figure 8 & Table 7: Unadopted AI Suggestions Analysis
Reads pre-computed classified reasons and plots distribution.
Produces: Figure 8 and Table 7 in the paper (identical colors, fonts, layout).

Adapted from: RQ3/3_unadopted/plot_unadopted_categories.py (EXACT SAME styling)
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import RQ3_CLASSIFIED_REASONS, RESULTS_DIR, FIGURES_DIR, TABLES_DIR

# =========================================================================
# EXACT SAME CONFIG FROM RQ3/3_unadopted/plot_unadopted_categories.py
# =========================================================================

CATEGORY_CONFIG = {
    'Incorrect Suggestion': {
        'short': 'Incorrect',
        'definition': 'AI suggestion is wrong or breaks the code',
    },
    'Alternative Fix': {
        'short': 'Alternative Fix',
        'definition': 'Developer applies a different fix',
    },
    'Not Needed': {
        'short': 'Not Needed',
        'definition': 'Suggestion is unnecessary or already handled',
    },
    'Claimed Fixed (Unverified)': {
        'short': 'Claimed Fixed',
        'definition': "Developer claims ``Fixed'' but no commits to the file",
    },
    'Developer Preference': {
        'short': 'Dev. Preference',
        'definition': 'Developer prefers a different design or coding style',
    },
    'Deferred': {
        'short': 'Deferred',
        'definition': 'Developer plans to address in future work',
    },
    'Others': {
        'short': 'Others',
        'definition': 'Unclear or ambiguous response',
    },
}

BAR_COLOR = '#808080'


def main():
    input_path = RQ3_CLASSIFIED_REASONS
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    df = pd.read_csv(input_path, low_memory=False)
    print(f"Loaded {len(df):,} unadopted suggestion records")

    output_dir = RESULTS_DIR / "RQ3"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Count categories
    category_counts = df['rejection_category'].value_counts()

    # =========================================================================
    # Print Table 7
    # =========================================================================
    print("\n" + "=" * 60)
    print(f"Table 7: Categories of Unadopted AI Code Suggestions (N={len(df)})")
    print("=" * 60)
    for cat, count in category_counts.items():
        pct = 100 * count / len(df)
        short = CATEGORY_CONFIG.get(cat, {}).get('short', cat)
        print(f"  {short:<25} {count:>6} ({pct:.1f}%)")

    # =========================================================================
    # Figure 8: EXACT SAME plotting code as original
    # =========================================================================
    categories = []
    counts = []
    raw_names = []
    for cat in category_counts.index:
        if cat in CATEGORY_CONFIG:
            categories.append(CATEGORY_CONFIG[cat]['short'])
            counts.append(category_counts[cat])
            raw_names.append(cat)

    fig, ax = plt.subplots(figsize=(12, 5))

    y_pos = range(len(categories))
    bars = ax.barh(y_pos, counts, color=BAR_COLOR, edgecolor='black', linewidth=0.5)

    for bar, count in zip(bars, counts):
        percentage = 100 * count / len(df)
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
                f'{count} ({percentage:.1f}%)',
                va='center', ha='left', fontsize=18, fontweight='bold')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=20, fontweight='bold')
    ax.set_xlabel('Number of Cases', fontsize=20, fontweight='bold')
    ax.set_title(f'Reasons for Unadopted AI Code Suggestions (N={len(df)})',
                 fontsize=20, fontweight='bold')
    ax.tick_params(axis='x', labelsize=20)
    ax.invert_yaxis()
    ax.set_xlim(0, max(counts) * 1.3)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    jpeg_path = FIGURES_DIR / "RQ3_unadopted_categories.jpeg"
    plt.savefig(jpeg_path, bbox_inches='tight', dpi=300)
    print(f"\nFigure 8 saved: {jpeg_path}")

    # Save summary CSV
    summary = pd.DataFrame({
        'Category': [CATEGORY_CONFIG.get(c, {}).get('short', c) for c in raw_names],
        'Raw_Category': raw_names,
        'Count': counts,
        'Percentage': [100 * c / len(df) for c in counts]
    })
    csv_path = output_dir / "unadopted_categories.csv"
    summary.to_csv(csv_path, index=False)
    print(f"Summary saved: {csv_path}")


if __name__ == "__main__":
    main()
