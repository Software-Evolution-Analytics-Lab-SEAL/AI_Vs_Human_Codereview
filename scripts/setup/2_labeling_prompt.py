#!/usr/bin/env python3
"""
Experiment Setup - Fig. 3: LLM Labeling Prompt
The prompt used for LLM-based automated labeling of feedback types.
Produces: results/tables/Setup_LabelingPrompt.txt
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import TABLES_DIR

# Fig. 3: Prompt for labelling feedback types
LABELING_PROMPT = (
    "Based on the feedback type definitions from Table II, "
    "classify the following code review comment into the most appropriate "
    "feedback type. Return the feedback type with a confidence score (1-10). "
    "Code review comment: {comment_body}"
)


def main():
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Fig. 3: Prompt for Labelling Feedback Types")
    print("=" * 70)
    print()
    print("Prompt:")
    print(f"  {LABELING_PROMPT}")

    # Save prompt
    output_path = TABLES_DIR / "Setup_LabelingPrompt.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("Fig. 3: Prompt for labelling feedback types.\n\n")
        f.write(f"Prompt: {LABELING_PROMPT}\n")

    print(f"\nPrompt saved as {output_path}")


if __name__ == "__main__":
    main()
