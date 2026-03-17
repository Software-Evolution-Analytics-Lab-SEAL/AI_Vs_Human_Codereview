#!/usr/bin/env python3
"""
RQ2 - Figure 5: FSM Interaction Pattern Visualization (State Machine Trees)
Reads pre-computed transition data and plots state machine diagrams.
Produces: Figure 5 (4 sub-figures) in the paper (identical colors, fonts, layout).

Adapted from: RQ2/1_allturns/4_1plot_allturn_trees.py (EXACT SAME plotting code)
"""

import argparse
import csv
import collections
from pathlib import Path
from typing import Dict, List
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path as MplPath
from PIL import Image
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import (RQ2_TRANSIT_FROM_AC, RQ2_TRANSIT_FROM_HC,
                    RQ2_TABLE_IV, FIGURES_DIR)

# =========================================================================
# BELOW IS THE EXACT PLOTTING CODE FROM RQ2/1_allturns/4_1plot_allturn_trees.py
# =========================================================================

# Categories Configuration
CATEGORIES = {
    'HRH': {'title': 'Human Reviewer → Human Code', 'start_label': 'H'},
    'HRA': {'title': 'Human Reviewer → Agent Code', 'start_label': 'A'},
    'ARH': {'title': 'Agent Reviewer → Human Code', 'start_label': 'H'},
    'ARA': {'title': 'Agent Reviewer → Agent Code', 'start_label': 'A'}
}

# Color Scheme
ROLE_COLORS = {
    'H': {'facecolor': '#E3F2FD', 'edgecolor': '#1976D2'},      # Blue
    'A': {'facecolor': '#FFF3E0', 'edgecolor': '#F57C00'},      # Orange
    'HC': {'facecolor': '#BBDEFB', 'edgecolor': '#0D47A1'},     # Darker Blue (Start)
    'AC': {'facecolor': '#FFE0B2', 'edgecolor': '#E65100'},     # Darker Orange (Start)
    'Merge': {'facecolor': '#C8E6C9', 'edgecolor': '#388E3C'},  # Light Green
    'Unmerge': {'facecolor': '#FFCDD2', 'edgecolor': '#D32F2F'} # Light Red
}


def load_avg_duration_data(input_path: Path) -> Dict[str, Dict]:
    """Load average duration metrics for each category."""
    data = {}
    if not input_path.exists():
        print(f"Warning: Avg duration file {input_path} not found.")
        return data

    with input_path.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row['Category']
            data[cat] = {
                'Total_ATC': float(row['Total_ATC']),
                'Total_Delta': row['Total_Delta'],
                'ACC_ATC': float(row['ACC_ATC']),
                'ACC_Delta': row['ACC_Delta'],
                'REJ_ATC': float(row['REJ_ATC']),
                'REJ_Delta': row['REJ_Delta'],
            }
    return data


def load_edge_data(input_paths: List[Path]) -> Dict[str, List[Dict]]:
    """Load edge data grouped by category from multiple files."""
    data = collections.defaultdict(list)

    for path in input_paths:
        if not path.exists():
            print(f"Warning: Input file {path} not found.")
            continue

        with path.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data[row['Category']].append(row)

    for cat in data:
        data[cat].sort(key=lambda x: int(x['Step']))

    return data


def draw_state_machine(ax, rows: List[Dict], group_name: str, config: Dict):
    """Draws the transparent state machine based on the rows."""

    num_steps = len(rows)

    X_SPACING = 6.0
    X_SPACING_FIRST = X_SPACING * 0.8
    Y_CENTER = 0
    BOX_W = 0.9
    BOX_H = 0.9

    margin = 1.0
    ax.set_xlim(-margin, (num_steps * X_SPACING) + margin)
    ax.set_ylim(-3.0, 2.0)
    ax.axis('off')
    ax.set_aspect('equal')

    for i, row in enumerate(rows):
        step = int(row['Step'])
        role = row['Role']

        if step == 0:
            x = 0
        elif step == 1:
            x = X_SPACING_FIRST
        else:
            x = X_SPACING_FIRST + (step - 1) * X_SPACING
        y = Y_CENTER

        color_key = role
        if role not in ROLE_COLORS:
            if 'H' in role: color_key = 'H'
            elif 'A' in role: color_key = 'A'

        colors = ROLE_COLORS.get(color_key, ROLE_COLORS['H'])

        if role in ['AC', 'HC']:
            w = 1.2
            h = 1.2
            font_s = 17
        else:
            w = BOX_W
            h = BOX_H
            font_s = 17

        box = FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w, h,
            boxstyle='round,pad=0.05',
            facecolor=colors['facecolor'],
            edgecolor=colors['edgecolor'],
            linewidth=2.0,
            zorder=10
        )
        ax.add_patch(box)

        ax.text(x, y, role, fontsize=font_s, ha='center', va='center', weight='bold', zorder=11)

        avg_turns = row['Loop_Avg']
        one_turn_pct = row.get('One_Turn_Pct', '')
        multi_turn_pct = row.get('Multi_Turn_Pct', '')

        if role not in ['AC', 'HC']:
            has_multi_turn = False
            if multi_turn_pct:
                try:
                    multi_turn_val = float(multi_turn_pct.strip('%'))
                    has_multi_turn = multi_turn_val > 0
                except:
                    has_multi_turn = False

            if avg_turns and has_multi_turn:
                start_x = x - w/2
                end_x = x + w/2
                connect_x = end_x - 0.08
                ctrl_y = y + h + 0.15
                h_spread = 0.1

                verts = [
                    (start_x, y + h/2),
                    (start_x - h_spread, ctrl_y),
                    (end_x + h_spread, ctrl_y),
                    (connect_x, y + h/2),
                ]
                codes = [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4]
                path = MplPath(verts, codes)

                patch = mpatches.PathPatch(path, facecolor='none', edgecolor='#7B1FA2', linewidth=2.0, zorder=5)
                ax.add_patch(patch)

                ax.add_patch(FancyArrowPatch(
                     (connect_x + 0.06, y + h/2 + 0.20), (connect_x, y + h/2),
                     arrowstyle='-|>', mutation_scale=10.5, color='#7B1FA2'
                ))

            if one_turn_pct or avg_turns:
                base_y = y + h + 0.25

                font_size = 9
                stat_color = '#7B1FA2'

                line_spacing = 0.22 * 1.3 * 1.2 * 1.2

                current_y = base_y

                one_turn_display = one_turn_pct if one_turn_pct else ""
                multi_turn_display = multi_turn_pct if multi_turn_pct else ""

                if one_turn_display.startswith('>'):
                    one_turn_display = "100%"
                if multi_turn_display.startswith('<'):
                    multi_turn_display = "0%"

                if one_turn_pct and not multi_turn_pct:
                    try:
                        one_turn_val = float(one_turn_pct.strip('%').lstrip('>').lstrip('<'))
                        if one_turn_val >= 99.9:
                            multi_turn_display = "0%"
                    except:
                        pass

                text_x = x + 1.3
                if multi_turn_display:
                    ax.text(text_x, current_y, f">1C={multi_turn_display}", fontsize=font_size, ha='right', va='bottom',
                            color=stat_color, weight='bold')
                current_y += line_spacing

                if one_turn_display:
                    ax.text(text_x, current_y, f"1C={one_turn_display}", fontsize=font_size, ha='right', va='bottom',
                            color=stat_color, weight='bold')
                current_y += line_spacing

                atc_display = avg_turns
                if not avg_turns and one_turn_pct:
                    try:
                        one_turn_val = float(one_turn_pct.strip('%'))
                        if one_turn_val == 100.0:
                            atc_display = "1.0"
                    except:
                        pass
                if atc_display:
                    ax.text(text_x, current_y, f"CPS={atc_display}", fontsize=font_size, ha='right', va='bottom',
                            color=stat_color, weight='bold')

        merge_prob_str = row.get('Merge_Prob', '')
        unmerge_prob_str = row.get('Unmerge_Prob', '')

        has_merge = bool(merge_prob_str and float(merge_prob_str.strip('%')) > 0)
        has_unmerge = bool(unmerge_prob_str and float(unmerge_prob_str.strip('%')) > 0)

        OFFSET_X = 1.9
        OFFSET_Y = 2.3

        if has_unmerge:
            target_x = x + OFFSET_X
            target_y = y - OFFSET_Y

            u_colors = ROLE_COLORS['Unmerge']
            circle = mpatches.Circle(
                (target_x, target_y),
                radius=0.6,
                facecolor=u_colors['facecolor'],
                edgecolor=u_colors['edgecolor'],
                linewidth=2.0,
                zorder=10
            )
            ax.add_patch(circle)
            ax.text(target_x, target_y, "REJ", fontsize=10, ha='center', va='center', weight='bold', zorder=11, color="black")

            start_pos = (x + w/4, y - h/2)
            end_pos = (target_x - 0.2, target_y + 0.55)

            arrow = FancyArrowPatch(
                 start_pos, end_pos,
                 arrowstyle='-|>', mutation_scale=15, color='black', linewidth=1.5,
                 linestyle='dashed'
             )
            ax.add_patch(arrow)

            mid_x = (start_pos[0] + end_pos[0]) / 2 + 0.1
            mid_y = (start_pos[1] + end_pos[1]) / 2
            ax.text(mid_x, mid_y, unmerge_prob_str, fontsize=9, ha='left', va='bottom', color='#D32F2F', weight='bold')

        if has_merge:
            target_x = x - OFFSET_X
            target_y = y - OFFSET_Y

            m_colors = ROLE_COLORS['Merge']
            circle = mpatches.Circle(
                (target_x, target_y),
                radius=0.6,
                facecolor=m_colors['facecolor'],
                edgecolor=m_colors['edgecolor'],
                linewidth=2.0,
                zorder=10
            )
            ax.add_patch(circle)
            ax.text(target_x, target_y, "ACC", fontsize=10, ha='center', va='center', weight='bold', zorder=11, color="black")

            start_pos = (x - w/4, y - h/2)
            end_pos = (target_x + 0.2, target_y + 0.55)

            arrow = FancyArrowPatch(
                 start_pos, end_pos,
                 arrowstyle='-|>', mutation_scale=15, color='black', linewidth=2.0,
                 linestyle='solid'
             )
            ax.add_patch(arrow)

            mid_x = (start_pos[0] + end_pos[0]) / 2 - 0.1
            mid_y = (start_pos[1] + end_pos[1]) / 2
            ax.text(mid_x, mid_y, merge_prob_str, fontsize=9, ha='right', va='bottom', color='black', weight='bold')

        next_prob_str = row['Next_Prob']
        if next_prob_str:
            next_prob_val = float(next_prob_str.strip('%'))
            if next_prob_val > 0:
                is_terminal_next = (i == len(rows) - 1) or (int(rows[i+1]['Step']) != step + 1)

                if not is_terminal_next:
                    if step == 0:
                        edge_spacing = X_SPACING_FIRST
                    else:
                        edge_spacing = X_SPACING

                    start_pos = (x + w/2, y)
                    end_pos = (x + edge_spacing - BOX_W/2, y)

                    arrow = FancyArrowPatch(
                         start_pos, end_pos,
                         arrowstyle='-|>', mutation_scale=20, color='black', linewidth=2.5
                    )
                    ax.add_patch(arrow)

                    mid_x = (start_pos[0] + end_pos[0]) / 2
                    ax.text(mid_x, y + 0.2, next_prob_str, fontsize=11, ha='center', va='bottom', weight='bold')


def main():
    parser = argparse.ArgumentParser(description="Plot State Machines from Truth Table")
    args = parser.parse_args()

    inputs = [RQ2_TRANSIT_FROM_AC, RQ2_TRANSIT_FROM_HC]
    data = load_edge_data(inputs)
    avg_duration_data = load_avg_duration_data(RQ2_TABLE_IV)

    if not data:
        print("No transition data found.")
        print("The pre-computed transition data should be in data/results/RQ2/")
        return

    # Global Layout based on Max Complexity (HRA standard)
    global_max_steps = 0
    for cat, rows in data.items():
        if cat in CATEGORIES:
            global_max_steps = max(global_max_steps, len(rows))

    X_SPACING = 6.0
    X_SPACING_FIRST = X_SPACING * 0.8
    BOX_W = 0.9

    fig_width = 12
    fig_height = 8

    if global_max_steps <= 1:
        max_node_x = 0
    elif global_max_steps == 2:
        max_node_x = X_SPACING_FIRST
    else:
        max_node_x = X_SPACING_FIRST + (global_max_steps - 2) * X_SPACING
    global_xlim = (-0.8, max_node_x + 2.8)

    print(f"Global Layout: Max Steps={global_max_steps}, Size={fig_width:.1f}x{fig_height}, Xlim={global_xlim}")

    output_dir = FIGURES_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    crop_widths = {
        'HRH': 5.2,
        'HRA': None,
        'ARA': 7.5,
        'ARH': 10
    }

    latex_display_ratios = {
        'HRH': 0.28,
        'HRA': 0.71,
        'ARA': 0.42,
        'ARH': 0.58
    }

    for category, rows in data.items():
        if category not in CATEGORIES:
            continue

        print(f"Plotting {category}...")
        config = CATEGORIES[category]

        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        draw_state_machine(ax, rows, category, config)

        ax.set_xlim(global_xlim)
        ax.set_ylim(-3.0, 5.0)

        # Calculate font scale factor for header
        reference_ratio = 12 / 0.73
        actual_width = crop_widths.get(category) or 12
        display_ratio = latex_display_ratios[category]
        font_scale = (actual_width / display_ratio) / reference_ratio

        # Add header with AvgC metrics
        if category in avg_duration_data:
            metrics = avg_duration_data[category]

            target_width_inches = crop_widths.get(category)
            if target_width_inches is not None:
                total_width = global_xlim[1] - global_xlim[0]
                visible_ratio = target_width_inches / fig_width
                visible_xlim_right = global_xlim[0] + total_width * visible_ratio
                center_x = (global_xlim[0] + visible_xlim_right) / 2
            else:
                center_x = (global_xlim[0] + global_xlim[1]) / 2

            base_fontsize = 12
            table_fontsize = base_fontsize * font_scale
            line_y = 4.8
            line_spacing = 0.45 * font_scale

            if category == 'HRH':
                header_line = "  AvgC    in ACC   in REJ  "
                value_line = f"  {metrics['Total_ATC']:.2f}     {metrics['ACC_ATC']:.2f}     {metrics['REJ_ATC']:.2f}  "
                line_half_width = 4.0 * font_scale
            else:
                header_line = " AvgC (vs. HRH)   in ACC   in REJ  "
                value_line = f" {metrics['Total_ATC']:.2f} ({metrics['Total_Delta']:>7s})   {metrics['ACC_ATC']:.2f}     {metrics['REJ_ATC']:.2f}  "
                line_half_width = 5.5 * font_scale

            y_pos = line_y

            ax.plot([center_x - line_half_width, center_x + line_half_width], [y_pos, y_pos],
                   color='#000000', linewidth=1.0 * font_scale, solid_capstyle='butt', zorder=20)
            y_pos -= line_spacing

            ax.text(center_x, y_pos, header_line,
                   fontsize=table_fontsize, ha='center', va='center', weight='bold',
                   color='#000000', family='monospace', zorder=20)
            y_pos -= line_spacing

            ax.plot([center_x - line_half_width, center_x + line_half_width], [y_pos, y_pos],
                   color='#000000', linewidth=0.8 * font_scale, solid_capstyle='butt', zorder=20)
            y_pos -= line_spacing

            ax.text(center_x, y_pos, value_line,
                   fontsize=table_fontsize, ha='center', va='center', weight='bold',
                   color='#000000', family='monospace', zorder=20)
            y_pos -= line_spacing

            ax.plot([center_x - line_half_width, center_x + line_half_width], [y_pos, y_pos],
                   color='#000000', linewidth=1.0 * font_scale, solid_capstyle='butt', zorder=20)

        output_path = output_dir / f"RQ2_{category}_allturn.jpeg"
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

        target_width_inches = crop_widths.get(category)

        if target_width_inches is not None:
            img = Image.open(output_path)
            original_width, original_height = img.size

            crop_width = int(target_width_inches * 300)

            if original_width > crop_width:
                cropped_img = img.crop((0, 0, crop_width, original_height))
                cropped_img.save(output_path, quality=95)
                print(f"  Saved and cropped to {output_path} (width: {crop_width}px = {target_width_inches} inches)")
            else:
                print(f"  Saved to {output_path} (no crop needed, width: {original_width}px)")
        else:
            print(f"  Saved to {output_path} (no crop - keeping original width)")

    print(f"\nFigure 5 saved to: {output_dir}")


if __name__ == "__main__":
    main()
