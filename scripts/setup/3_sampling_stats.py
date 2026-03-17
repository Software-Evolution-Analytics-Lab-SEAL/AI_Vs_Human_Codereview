#!/usr/bin/env python3
"""
RQ3 - Table 9: Sampling Statistics for Code Metrics Analysis
Reads pre-computed sampling statistics from aggregated results.
Produces: Table 9 in the paper (identical numbers).
"""

import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import RQ3_SAMPLING_STATS, RESULTS_DIR


def main():
    input_path = RQ3_SAMPLING_STATS
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    df = pd.read_csv(input_path)

    print("=" * 50)
    print("Table 9: Code Metrics Sampling Statistics")
    print("=" * 50)
    print(df.to_string(index=False))
    print(f"\nSource: {input_path}")


if __name__ == "__main__":
    main()
