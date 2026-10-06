"""
Centralized path configuration for the replication package.

Two data sources:
  1. data/results/  - Pre-computed aggregated results (exact paper numbers, included in repo)
  2. data/sample/   - Raw data sample (100 rows, for demonstrating the full pipeline)

To reproduce from scratch with the full raw dataset:
  - Download from HuggingFace and place in data/full/
  - Set DATA_DIR = PROJECT_ROOT / "data" / "full"
"""

from pathlib import Path

# Root of the replication package
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ============================================================================
# Pre-computed aggregated results (produce IDENTICAL paper tables/figures)
# ============================================================================
AGG_DIR = PROJECT_ROOT / "data" / "results"
AGG_RQ1 = AGG_DIR / "RQ1"
AGG_RQ2 = AGG_DIR / "RQ2"
AGG_RQ3 = AGG_DIR / "RQ3"

# ============================================================================
# Raw data directory (sample included; full dataset from HuggingFace)
# ============================================================================
# For sample data (included in repo, 100 rows):
DATA_DIR = PROJECT_ROOT / "data" / "sample"
# For full dataset (download from HuggingFace):
# DATA_DIR = PROJECT_ROOT / "data" / "full"

# ============================================================================
# Output directories
# ============================================================================
RESULTS_DIR = PROJECT_ROOT / "results"
TABLES_DIR = RESULTS_DIR / "tables"
FIGURES_DIR = RESULTS_DIR / "figures"

# Ensure output directories exist
TABLES_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# RQ1 Aggregated Results
# ============================================================================
RQ1_DATASET_SUMMARY = AGG_RQ1 / "1_1sum_dataset.csv"
RQ1_FEEDBACK_SUMMARY = AGG_RQ1 / "3_2_summary_feedtype.csv"
RQ1_FEEDBACK_BY_REVIEW = AGG_RQ1 / "3_2_sum_review.csv"
RQ1_CD_SUMMARY = AGG_RQ1 / "4_1_cd_summary.csv"
RQ1_CD_DETAIL_SLIM = AGG_RQ1 / "4_1_cd_detail_slim.csv"
RQ1_CD_SCOTTKNOTT = AGG_RQ1 / "4_2_cd_scottknott.csv"
RQ1_SK_FDBTYPE_TURNS = AGG_RQ1 / "5_1_sk_fdbtype_turns.csv"

# ============================================================================
# RQ2 Aggregated Results
# ============================================================================
RQ2_TABLE_IV = AGG_RQ2 / "8_1_table_iv_format.csv"
RQ2_AVG_DURATION = AGG_RQ2 / "8_1_avg_duration_metrics.csv"
RQ2_FDBTYPE_COMPARE = AGG_RQ2 / "3_0fdbtype_compare.csv"
RQ2_FDBTYPE_DISTRI = AGG_RQ2 / "3_0fdbtype_distri.csv"
RQ2_TRANSIT_FROM_AC = AGG_RQ2 / "4_0_transit_fromAC.csv"
RQ2_TRANSIT_FROM_HC = AGG_RQ2 / "4_0_transit_fromHC.csv"
RQ2_SK_RANK_HRH = AGG_RQ2 / "3_1Taxonomy_Rank_HRH.csv"
RQ2_SK_RANK_HRA = AGG_RQ2 / "3_1Taxonomy_Rank_HRA.csv"
RQ2_SK_RANK_ARH = AGG_RQ2 / "3_1Taxonomy_Rank_ARH.csv"
RQ2_SK_RANK_ARA = AGG_RQ2 / "3_1Taxonomy_Rank_ARA.csv"
RQ2_FDBTYPE_TURNS_PER_CAT = AGG_RQ2 / "RQ2_fdbtype_turns_per_category.csv"

# ============================================================================
# RQ3 Aggregated Results
# ============================================================================
RQ3_SIGDIFF_METRICS = AGG_RQ3 / "2_sigdiff_metrics.csv"
RQ3_METRICS_BY_REVIEWER = AGG_RQ3 / "6_metrics_by_reviewer.csv"
RQ3_SK_RANKING = AGG_RQ3 / "sk_reviewer_metric_ranking.csv"
RQ3_SAMPLING_STATS = AGG_RQ3 / "sampling_stats.csv"
RQ3_ADOPTION_BY_FEEDTYPE = AGG_RQ3 / "1_3_resolution_by_feedtype.csv"
RQ3_CLASSIFIED_REASONS = AGG_RQ3 / "classified_reasons.csv"

# ============================================================================
# Raw Data Files (for full pipeline rerun with HuggingFace data)
# ============================================================================
RAW_CONVO_ROLES = DATA_DIR / "1_convo_roles.csv"
RAW_DETAIL = DATA_DIR / "2_1_detail.csv"
RAW_FDBTYPES = DATA_DIR / "3_1_fdbtypes.csv"
RAW_RQ2_ALL_TURNS = DATA_DIR / "rq2_all_turn_detail.csv"
RAW_RQ2_FDBTYPE_DETAIL = DATA_DIR / "rq2_fdbtype_detail.csv"
RAW_RQ3_SIM_FINAL = DATA_DIR / "rq3_sim_final.csv"
RAW_RQ3_RAW_METRICS = DATA_DIR / "rq3_raw_metrics.csv"
RAW_RQ3_JOINED_DATA = DATA_DIR / "rq3_joined_data.csv"

# ============================================================================
# Review Category Mappings
# ============================================================================
CATEGORY_FULL_TO_SHORT = {
    "Human_Review_Human": "HRH",
    "Human_Review_Agent": "HRA",
    "Agent_Review_Human": "ARH",
    "Agent_Review_Agent": "ARA",
}

CATEGORY_SHORT_TO_FULL = {v: k for k, v in CATEGORY_FULL_TO_SHORT.items()}

REVIEW_CATEGORIES = ["HRH", "HRA", "ARH", "ARA"]
