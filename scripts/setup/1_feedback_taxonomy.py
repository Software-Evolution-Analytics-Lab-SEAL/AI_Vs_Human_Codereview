#!/usr/bin/env python3
"""
Experiment Setup - TABLE II: Feedback Type Taxonomy
Feedback types from Bacchelli and Bird [6] with rephrased descriptions.
Produces: results/tables/Setup_FeedbackTaxonomy.csv
"""

import csv
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import TABLES_DIR

# TABLE II: Feedback types from Bacchelli and Bird with rephrased descriptions
FEEDBACK_TYPES = [
    ('Code Improvement',
     'Suggestions to enhance code clarity, style, structure, or maintainability without fixing defects.'),
    ('Defect Detection',
     'Identification of functional, logical, or correctness issues in the proposed changes.'),
    ('External Impact',
     'Comments about broader system-level consequences beyond the local code diff.'),
    ('Knowledge Transfer',
     'Reviewer explains concepts, conventions, best practices, or provides learning resources.'),
    ('Misc',
     'Comments that do not fit any defined category or are context-irrelevant.'),
    ('No Feedback',
     'Conversations where the reviewer provides no substantive technical feedback.'),
    ('Social',
     'Interpersonal statements not directly tied to technical content (e.g., appreciation, encouragement).'),
    ('Testing',
     'Comments about adding, updating, or fixing tests and test coverage.'),
    ('Understanding',
     'Clarification questions to understand context, rationale, design decisions, or implementation intent.'),
]


def main():
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    # Print table
    print("=" * 80)
    print("TABLE II: Feedback Types from Bacchelli and Bird with Rephrased Descriptions")
    print("=" * 80)
    print(f"\n{'Feedback Type':<22} Description")
    print("-" * 80)
    for ft, desc in FEEDBACK_TYPES:
        print(f"  {ft:<20} {desc}")

    # Save CSV
    output_path = TABLES_DIR / "Setup_FeedbackTaxonomy.csv"
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Feedback_Type', 'Description'])
        for ft, desc in FEEDBACK_TYPES:
            writer.writerow([ft, desc])

    print(f"\nTable saved as {output_path}")


if __name__ == "__main__":
    main()
