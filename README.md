# Replication Package: Human vs. AI Agents in Code Review

This repository provides the replication package for the paper:
**"Human vs. AI Agents in Code Review: An Empirical Comparison of Review Feedback, Interaction Dynamics, and Suggestion Adoption"**

## Overview

This study empirically compares code review practices across four categories:
- **HRH**: Human Reviews Human-written code
- **HRA**: Human Reviews Agent-generated code
- **ARH**: Agent Reviews Human-written code
- **ARA**: Agent Reviews Agent-generated code

The analysis spans three research questions:
- **RQ1**: What are the similarities and differences between the review comments by AI agents and human reviewers?
- **RQ2**: How do interaction patterns differ between human and AI agent code reviews?
- **RQ3**: What is the impact of code suggestions from human reviewers and AI agents on code quality?

## Repository Structure

```
AI_Vs_Human_Codereview/
├── README.md                          # This file
├── run_all.py                         # Run all scripts in one command
├── requirements.txt                   # Python dependencies
├── requirements-lock.txt              # Pinned Python dependencies
├── install_packages.R                 # R dependencies
├── data/
│   ├── results/                       # Pre-computed aggregated results
│   │   ├── RQ1/                       #   (reproduces exact paper numbers)
│   │   ├── RQ2/
│   │   └── RQ3/
│   └── sample/                        # Raw data sample (100 rows per file)
│       └── README.md                  #   Data file descriptions
├── scripts/
│   ├── config.py                      # Centralized path configuration
│   ├── setup/                         # Experiment setup artifacts
│   │   ├── 1_feedback_taxonomy.py     # Table II: Feedback type taxonomy
│   │   ├── 2_labeling_prompt.py       # Figure 3: LLM labeling prompt
│   │   └── 3_sampling_stats.py        # Table IX: Sampling statistics
│   ├── RQ1/                           # RQ1: Feedback analysis
│   │   ├── 0_dataset_table.py         # Table I: Dataset overview
│   │   ├── 1_feedback_distribution.py # Figure 4: Feedback type chart
│   │   ├── 2_cd_violin.py             # Figure 5: Comment density violin
│   │   ├── 3_sk_fdbtype_turns.py      # Table III: Feedback by rounds
│   │   └── 3_scott_knott_cd.R         # Figure 5: Scott-Knott CD ranking
│   ├── RQ2/                           # RQ2: Interaction dynamics
│   │   ├── 1_avg_duration.py          # Table IV: Avg comment count
│   │   ├── 2_fsm_visualization.py     # Figure 6: FSM diagrams
│   │   └── 3_scott_knott_feedback.R   # Table III: Scott-Knott feedback
│   └── RQ3/                           # RQ3: Suggestion adoption
│       ├── 1_adoption_rates.py        # Table V: Adoption rates
│       ├── 2_code_metrics_analysis.py # Table VI: Code quality impact
│       ├── 3_unadopted_analysis.py    # Figure 8: Unadopted reasons
│       ├── 6_code_metrics_R.R         # Statistical testing (R)
│       └── 7_scott_knott_metrics.R    # Scott-Knott metric ranking
├── prompts/
│   └── feedback_classification.md     # LLM prompts used for labeling
└── results/                           # Output directory
    ├── tables/                        # Generated CSV tables
    └── figures/                       # Generated figures (JPEG)
```

## Reproducibility

This package supports two levels of reproducibility:

### Level 1: Reproduce Tables and Figures (Quick)
All pre-computed aggregated results are included in `data/results/`. Python scripts read
these files and produce the exact tables and figures from the paper. No full dataset needed.

### Level 2: Reproduce Full Analysis (Complete)
Download the full raw dataset from HuggingFace, then R scripts run the statistical
analysis (Scott-Knott ESD, Wilcoxon, Cliff's delta) from scratch.

## Tables and Figures Mapping

| Paper Artifact | Script | Description |
|----------------|--------|-------------|
| Table I | `RQ1/0_dataset_table.py` | Dataset distribution across review categories |
| Table II | `setup/1_feedback_taxonomy.py` | Feedback type taxonomy from Bacchelli & Bird |
| Table III | `RQ1/3_sk_fdbtype_turns.py` | Feedback types by discussion rounds (Scott-Knott) |
| Table IV | `RQ2/1_avg_duration.py` | Average comment count by category and outcome |
| Table V | `RQ3/1_adoption_rates.py` | Suggestion adoption rates by feedback type |
| Table VI | `RQ3/2_code_metrics_analysis.py` | Code quality impact (6 significant metrics) |
| Figure 3 | `setup/2_labeling_prompt.py` | LLM labeling prompt |
| Figure 4 | `RQ1/1_feedback_distribution.py` | Feedback type distribution bar chart |
| Figure 5 | `RQ1/2_cd_violin.py` | Comment-to-Code Density rankings |
| Figure 6 | `RQ2/2_fsm_visualization.py` | FSM interaction patterns |
| Figure 8 | `RQ3/3_unadopted_analysis.py` | Unadopted suggestion distribution |

Figures 1, 2, 7, 9 are static illustrations/examples (not computed from data).

## Setup

### Prerequisites
- Python 3.9+
- R 4.0+ (optional, for full reproducibility only)

### Installation

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows

# Install Python dependencies (exact versions for reproducibility)
pip install -r requirements-lock.txt
# Or use flexible versions:
# pip install -r requirements.txt

# R dependencies (optional)
Rscript install_packages.R
```

### Data

**Pre-computed results** are included in `data/results/` and are sufficient to reproduce
all tables and figures in the paper.

**Sample raw data** (100 rows per file) is included in `data/sample/` for demonstrating
the full analysis pipeline.

**Full raw dataset** is available on HuggingFace:
**[TODO: Add HuggingFace URL]**

To use the full dataset, download and place in `data/full/`, then update `scripts/config.py`:
```python
DATA_DIR = PROJECT_ROOT / "data" / "full"
```

## Running the Analysis

### Run Everything
```bash
python run_all.py              # Run all scripts
python run_all.py --skip-r     # Skip R scripts (Python only)
python run_all.py --rq1        # Run only RQ1 scripts
```

### Individual Scripts

#### Setup: Experiment Artifacts
```bash
python scripts/setup/1_feedback_taxonomy.py    # Table II
python scripts/setup/2_labeling_prompt.py      # Figure 3
python scripts/setup/3_sampling_stats.py       # Table IX
```

#### RQ1: Feedback Analysis
```bash
python scripts/RQ1/0_dataset_table.py          # Table I
python scripts/RQ1/1_feedback_distribution.py  # Figure 4
python scripts/RQ1/2_cd_violin.py              # Figure 5
python scripts/RQ1/3_sk_fdbtype_turns.py       # Table III
Rscript scripts/RQ1/3_scott_knott_cd.R         # Figure 5 (from raw data)
```

#### RQ2: Interaction Dynamics
```bash
python scripts/RQ2/1_avg_duration.py           # Table IV
python scripts/RQ2/2_fsm_visualization.py      # Figure 6
Rscript scripts/RQ2/3_scott_knott_feedback.R   # Table III (from raw data)
```

#### RQ3: Suggestion Adoption & Code Quality
```bash
python scripts/RQ3/1_adoption_rates.py         # Table V
python scripts/RQ3/2_code_metrics_analysis.py  # Table VI
python scripts/RQ3/3_unadopted_analysis.py     # Figure 8
Rscript scripts/RQ3/6_code_metrics_R.R         # Statistical testing (from raw data)
Rscript scripts/RQ3/7_scott_knott_metrics.R    # Scott-Knott ranking (from raw data)
```

## Notes

- **Python scripts** use pre-computed results from `data/results/` and reproduce exact paper outputs.
- **R scripts** run statistical analysis from raw data in `data/sample/` or `data/full/`.
- **Sample data** produces correct output structure but values differ from the paper (only 100 rows).
- **Full dataset** from HuggingFace reproduces exact paper results.
- R scripts require the `ScottKnottESD` package for non-parametric effect size ranking.
- Code metrics extraction uses SciTools Understand (not included; raw metrics are provided).
- LLM-based labeling uses GPT-4.1-mini; prompts are documented in `prompts/`.
