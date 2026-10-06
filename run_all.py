#!/usr/bin/env python3
"""Run all analysis scripts in order and report success/failure."""

import argparse
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

SETUP_SCRIPTS = [
    ("Setup: Feedback Taxonomy", "python scripts/setup/1_feedback_taxonomy.py"),
    ("Setup: Labeling Prompt", "python scripts/setup/2_labeling_prompt.py"),
    ("Setup: Sampling Stats", "python scripts/setup/3_sampling_stats.py"),
]

RQ1_SCRIPTS = [
    ("RQ1: Dataset Table", "python scripts/RQ1/0_dataset_table.py"),
    ("RQ1: Feedback Distribution", "python scripts/RQ1/1_feedback_distribution.py"),
    ("RQ1: CD Violin Plot", "python scripts/RQ1/2_cd_violin.py"),
    ("RQ1: SK Feedback Type Turns", "python scripts/RQ1/3_sk_fdbtype_turns.py"),
    ("RQ1: Scott-Knott CD (R)", "Rscript scripts/RQ1/3_scott_knott_cd.R"),
]

RQ2_SCRIPTS = [
    ("RQ2: Avg Duration", "python scripts/RQ2/1_avg_duration.py"),
    ("RQ2: FSM Visualization", "python scripts/RQ2/2_fsm_visualization.py"),
    ("RQ2: Scott-Knott Feedback (R)", "Rscript scripts/RQ2/3_scott_knott_feedback.R"),
]

RQ3_SCRIPTS = [
    ("RQ3: Adoption Rates", "python scripts/RQ3/1_adoption_rates.py"),
    ("RQ3: Code Metrics Analysis", "python scripts/RQ3/2_code_metrics_analysis.py"),
    ("RQ3: Unadopted Analysis", "python scripts/RQ3/3_unadopted_analysis.py"),
    ("RQ3: Code Metrics (R)", "Rscript scripts/RQ3/6_code_metrics_R.R"),
    ("RQ3: Scott-Knott Metrics (R)", "Rscript scripts/RQ3/7_scott_knott_metrics.R"),
]


def run_script(name, command, skip_r=False):
    """Run a single script and return (name, passed, duration)."""
    is_r = command.startswith("Rscript")
    if is_r and skip_r:
        return name, None, 0.0  # None means skipped

    print(f"\n{'=' * 60}")
    print(f"  {name}")
    print(f"  > {command}")
    print(f"{'=' * 60}")

    start = time.time()
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=PROJECT_ROOT,
            timeout=600,
        )
        duration = time.time() - start
        passed = result.returncode == 0
        status = "PASS" if passed else "FAIL"
        print(f"\n  [{status}] {name} ({duration:.1f}s)")
        return name, passed, duration
    except subprocess.TimeoutExpired:
        duration = time.time() - start
        print(f"\n  [TIMEOUT] {name} ({duration:.1f}s)")
        return name, False, duration
    except Exception as e:
        duration = time.time() - start
        print(f"\n  [ERROR] {name}: {e}")
        return name, False, duration


def print_summary(results):
    """Print a summary table of all results."""
    print(f"\n\n{'=' * 60}")
    print("  SUMMARY")
    print(f"{'=' * 60}")
    print(f"  {'Script':<40} {'Status':<10} {'Time':>6}")
    print(f"  {'-' * 40} {'-' * 10} {'-' * 6}")

    passed = 0
    failed = 0
    skipped = 0

    for name, success, duration in results:
        if success is None:
            status = "SKIPPED"
            skipped += 1
        elif success:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed += 1
        print(f"  {name:<40} {status:<10} {duration:>5.1f}s")

    print(f"  {'-' * 40} {'-' * 10} {'-' * 6}")
    print(f"  Passed: {passed}  Failed: {failed}  Skipped: {skipped}")
    print()

    return failed == 0


def main():
    parser = argparse.ArgumentParser(description="Run all analysis scripts.")
    parser.add_argument("--skip-r", action="store_true", help="Skip R scripts")
    parser.add_argument("--rq1", action="store_true", help="Run only RQ1 scripts")
    parser.add_argument("--rq2", action="store_true", help="Run only RQ2 scripts")
    parser.add_argument("--rq3", action="store_true", help="Run only RQ3 scripts")
    parser.add_argument("--skip-setup", action="store_true", help="Skip setup scripts")
    args = parser.parse_args()

    # If no specific RQ is selected, run all
    run_all = not (args.rq1 or args.rq2 or args.rq3)

    scripts = []
    if not args.skip_setup and run_all:
        scripts.extend(SETUP_SCRIPTS)
    if run_all or args.rq1:
        scripts.extend(RQ1_SCRIPTS)
    if run_all or args.rq2:
        scripts.extend(RQ2_SCRIPTS)
    if run_all or args.rq3:
        scripts.extend(RQ3_SCRIPTS)

    print(f"Running {len(scripts)} scripts from: {PROJECT_ROOT}")

    results = []
    for name, command in scripts:
        result = run_script(name, command, skip_r=args.skip_r)
        results.append(result)

    success = print_summary(results)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
