#!/usr/bin/env python3
"""
RQ1 - Figure 5: Scott-Knott ESD on Comment-to-Code Density (CD)

Reads pre-computed CD detail data and SK rankings to reproduce Figure 5.
Uses the EXACT SAME styling as the original RQ1/4_2_plot_cd.R.

Produces: results/figures/RQ1_CD_ranking.jpeg
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import FIGURES_DIR

# Resolve data paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CD_DETAIL = PROJECT_ROOT / "data" / "results" / "RQ1" / "4_1_cd_detail_slim.csv"
SK_RESULTS = PROJECT_ROOT / "data" / "results" / "RQ1" / "4_2_cd_scottknott.csv"

# Plot settings (match original R script)
PLOT_WIDTH = 12
PLOT_HEIGHT = 4
PLOT_DPI = 300

# Rank colors (same as original)
RANK_COLORS = {
    1: '#2ca02c',  # rank1 - darker green
    2: '#FFFF99',  # rank2 - yellow
    3: '#FFCC99',  # rank3 - light orange
    4: '#FF9999',  # rank4 - light red
    5: '#DDDDDD',  # rank5 - gray
}


def main():
    if not CD_DETAIL.exists():
        raise FileNotFoundError(f"Input not found: {CD_DETAIL}")
    if not SK_RESULTS.exists():
        raise FileNotFoundError(f"Input not found: {SK_RESULTS}")

    # Load data
    df = pd.read_csv(CD_DETAIL)
    df = df.dropna(subset=['CD'])
    df = df[df['CD'] > 0]
    df = df[np.isfinite(df['CD'])]
    print(f"Loaded {len(df):,} valid CD values")

    # Load SK rankings
    sk = pd.read_csv(SK_RESULTS)
    sk = sk.sort_values('SK_rank')
    print(f"\nScott-Knott ESD Rankings:")
    for _, row in sk.iterrows():
        print(f"  G{row['SK_rank']}: {row['category']} (mean={row['mean_val']:.1f})")

    # Merge rank info
    df = df.merge(sk[['category', 'SK_rank', 'SK_group']], on='category', how='inner')
    df['log_CD'] = np.log10(df['CD'])

    # Group by SK_group for faceting
    groups = sk[['SK_group', 'SK_rank']].drop_duplicates().sort_values('SK_rank')

    # Create faceted figure
    n_facets = len(groups)
    # Count categories per facet for relative widths
    cats_per_facet = []
    for _, g in groups.iterrows():
        n_cats = len(sk[sk['SK_group'] == g['SK_group']])
        cats_per_facet.append(n_cats)

    fig = plt.figure(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
    gs = gridspec.GridSpec(1, n_facets, width_ratios=cats_per_facet, wspace=0.08)

    # Compute global y-axis limits
    y_min = df['log_CD'].quantile(0.001)
    y_max = df['log_CD'].quantile(0.999)
    y_range = y_max - y_min
    y_min -= y_range * 0.02
    y_max += y_range * 0.05

    # Nice tick values for log scale
    tick_values = [0.01, 0.10, 1.00, 10.00, 100.00, 1000.00]
    tick_positions = [np.log10(v) for v in tick_values]
    tick_labels = [f'{v:,.2f}' for v in tick_values]

    # Filter to visible range
    visible_ticks = [(pos, lab) for pos, lab in zip(tick_positions, tick_labels)
                     if y_min <= pos <= y_max]

    rank_order = sk.sort_values('SK_rank')['category'].tolist()

    for facet_idx, (_, g_row) in enumerate(groups.iterrows()):
        ax = fig.add_subplot(gs[facet_idx])
        sk_group = g_row['SK_group']
        sk_rank = g_row['SK_rank']
        facet_label = f"G{sk_rank}"

        # Categories in this facet (ordered by rank_order)
        facet_cats = [c for c in rank_order
                      if c in sk[sk['SK_group'] == sk_group]['category'].values]

        # Draw violins
        parts_data = []
        positions = []
        for i, cat in enumerate(facet_cats):
            cat_data = df[df['category'] == cat]['log_CD'].values
            parts_data.append(cat_data)
            positions.append(i + 1)

        color = RANK_COLORS.get(sk_rank, '#DDDDDD')

        if parts_data:
            vp = ax.violinplot(parts_data, positions=positions, showmeans=False,
                               showmedians=False, showextrema=False, widths=0.8)
            for body in vp['bodies']:
                body.set_facecolor(color)
                body.set_edgecolor('black')
                body.set_alpha(0.85)
                body.set_linewidth(0.8)

        # Add mean line and annotation
        for i, cat in enumerate(facet_cats):
            cat_data = df[df['category'] == cat]['CD']
            mean_val = cat_data.mean()
            mean_log = np.log10(mean_val)

            # Mean line
            ax.hlines(mean_log, positions[i] - 0.3, positions[i] + 0.3,
                      colors='black', linewidths=1.1, zorder=5)

            # Mean annotation
            ax.text(positions[i], mean_log, f'{mean_val:.1f}',
                    ha='center', va='bottom', fontsize=14, fontweight='bold',
                    color='black', zorder=6,
                    bbox=dict(boxstyle='round,pad=0.1', facecolor='white',
                              edgecolor='none', alpha=0.7))

        # Axes
        ax.set_ylim(y_min, y_max)
        if visible_ticks:
            ax.set_yticks([t[0] for t in visible_ticks])
            if facet_idx == 0:
                ax.set_yticklabels([t[1] for t in visible_ticks],
                                   fontsize=20, fontweight='bold')
            else:
                ax.set_yticklabels([])

        ax.set_xticks(positions)
        ax.set_xticklabels(facet_cats, fontsize=16, fontweight='bold', color='black')
        ax.set_xlim(0.3, len(facet_cats) + 0.7)

        # Grid
        ax.yaxis.grid(True, linestyle='--', color='#e0e0e0', alpha=0.7)
        ax.xaxis.grid(False)
        ax.set_axisbelow(True)

        # Border
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('black')
            spine.set_linewidth(1)

        # Facet header (gray background like ggplot)
        ax.text(0.5, 1.02, facet_label, transform=ax.transAxes,
                ha='center', va='bottom', fontsize=16, fontweight='bold',
                bbox=dict(boxstyle='square,pad=0.3', facecolor='#E5E5E5',
                          edgecolor='black', linewidth=1))

        # Y-axis label only on leftmost facet
        if facet_idx == 0:
            ax.set_ylabel('Comment-to-Code Density (CD)', fontsize=16,
                          fontweight='bold', color='black')

    # X-axis label centered
    fig.text(0.5, -0.02, 'Review Category', ha='center', fontsize=16, fontweight='bold')

    plt.tight_layout()

    # Save
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / 'RQ1_CD_ranking.jpeg'
    plt.savefig(output_path, dpi=PLOT_DPI, bbox_inches='tight', facecolor='white')
    print(f'\nFigure 5 saved as {output_path}')

    # Summary
    print(f"\nSummary Statistics:")
    for _, row in sk.iterrows():
        cat = row['category']
        cat_data = df[df['category'] == cat]
        n = len(cat_data)
        mean_cd = cat_data['CD'].mean()
        median_cd = cat_data['CD'].median()
        print(f"  {cat}: N={n:,}, Mean={mean_cd:.2f}, Median={median_cd:.2f}, Rank={row['SK_rank']}")


if __name__ == '__main__':
    main()
