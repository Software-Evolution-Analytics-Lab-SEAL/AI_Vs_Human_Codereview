# Sample Data

This directory contains sample data (first 100 rows) from each dataset used in the analysis.
The sample data demonstrates the data format and allows running the scripts for verification.

## Full Dataset

The full dataset is available on HuggingFace:
**[TODO: Add HuggingFace URL here]**

To use the full dataset:
1. Download from HuggingFace
2. Place files in `data/full/`
3. Update `scripts/config.py` to point to `data/full/`

## File Descriptions

### RQ1 Input Data
| File | Rows (full) | Description |
|------|-------------|-------------|
| `1_convo_roles.csv` | 278,790 | Conversation roles with review categories (HRH/HRA/ARH/ARA) |
| `2_1_detail.csv` | 278,790 | LOC and token metrics per conversation |
| `3_1_fdbtypes.csv` | 278,790 | LLM-labeled feedback types per conversation |
| `4_1_cd_detail.csv` | ~270K | Comment-to-Code Density per conversation |
| `4_1_cd_summary.csv` | 4 | Summary statistics per review category |

### RQ2 Input Data
| File | Rows (full) | Description |
|------|-------------|-------------|
| `rq2_all_turn_detail.csv` | 278,790 | All conversation turns with sequences and outcomes |
| `rq2_fdbtype_detail.csv` | ~228K | Feedback types linked to review conversations |
| `rq2_fdbtype_compare.csv` | 16 | Feedback type comparison (AvgC, >1C%) |
| `rq2_transit_fromAC.csv` | ~11 | Agent Code starter transition edges |
| `rq2_transit_fromHC.csv` | ~9 | Human Code starter transition edges |
| `rq2_avg_duration_metrics.csv` | 12 | Average duration by category and outcome |
| `rq2_table_iv_format.csv` | 4 | Table IV format (AvgC with delta vs HRH) |

### RQ3 Input Data
| File | Rows (full) | Description |
|------|-------------|-------------|
| `rq3_suggestion_feedtype.csv` | ~50K | Suggestions with feedback types |
| `rq3_sim_final.csv` | ~50K | Similarity detection results (adopted/unadopted) |
| `rq3_joined_data.csv` | ~3.5K | Filtered data for code metrics analysis |
| `rq3_raw_metrics.csv` | ~3.5K | Raw code metrics (before/after/delta for 13 metrics) |
| `rq3_sigdiff_metrics.csv` | ~111 | Statistically significant metric differences |
| `rq3_sampling_stats.csv` | 3 | Sampling statistics (AccSug, Files) |
| `rq3_sk_reviewer_metric_ranking.csv` | ~18 | Scott-Knott rankings by metric and reviewer |
| `rq3_metrics_by_reviewer.csv` | 6 | Aggregated metrics by reviewer type |
| `rq3_classified_reasons.csv` | 383 | Classified reasons for unadopted suggestions |

## Column Descriptions

### Review Categories
- **HRH**: Human Reviews Human-written code
- **HRA**: Human Reviews Agent-generated code
- **ARH**: Agent Reviews Human-written code
- **ARA**: Agent Reviews Agent-generated code

### Key Columns
- `convo_start_id` / `thread_id`: Unique conversation identifier
- `review_category`: One of Human_Review_Human, Human_Review_Agent, Agent_Review_Human, Agent_Review_Agent
- `feed_type`: Feedback type classification (Code Improvement, Defects, Understanding, etc.)
- `comment_count`: Number of comments in a conversation
- `pr_merged`: Whether the PR was merged (True/False)
- `reviewer_type`: Human or Agent
- `final_is_applied`: Whether a suggestion was adopted (True/False)
