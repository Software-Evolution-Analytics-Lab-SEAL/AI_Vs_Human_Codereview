#!/usr/bin/env Rscript
#
# RQ3 - Table 10: Scott-Knott ESD Ranking by Reviewer and Metric
# Ranks metric-reviewer combinations to identify largest quality differences.
# Produces: Table 10 in the paper.
#
# Usage: Rscript 7_scott_knott_metrics.R
#

suppressPackageStartupMessages({
  library(ScottKnottESD)
  library(dplyr)
  library(tidyr)
})

# Resolve paths
args_full <- commandArgs(trailingOnly = FALSE)
script_idx <- grep("^--file=", args_full)
if (length(script_idx) > 0) {
  script_path <- normalizePath(sub("^--file=", "", args_full[script_idx][1]))
  script_dir <- dirname(script_path)
} else {
  script_dir <- getwd()
}

project_root <- normalizePath(file.path(script_dir, "..", ".."))
metrics_file <- file.path(project_root, "data", "sample", "rq3_raw_metrics.csv")
metadata_file <- file.path(project_root, "data", "sample", "rq3_joined_data.csv")
output_dir <- file.path(project_root, "results", "RQ3")

if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

cat("=== Scott-Knott ESD Ranking: Metrics by Reviewer ===\n\n")

if (!file.exists(metrics_file)) {
  cat("Metrics file not found. Download full dataset from HuggingFace.\n")
  quit(status = 0)
}

df <- read.csv(metrics_file, stringsAsFactors = FALSE)
cat(sprintf("Loaded %d records\n", nrow(df)))

# Load metadata
if (file.exists(metadata_file)) {
  meta <- read.csv(metadata_file, stringsAsFactors = FALSE)
  meta <- meta %>% select(thread_id, reviewer_type, feed_type) %>% distinct()
  df <- df %>% mutate(thread_id = as.character(thread_id))
  meta <- meta %>% mutate(thread_id = as.character(thread_id))
  df <- df %>% left_join(meta, by = "thread_id")
}

# Selected metrics (top 9 with largest gaps)
selected_metrics <- c(
  "SumCyclomaticComplexity_Delta",
  "Lines_Delta",
  "Statements_Delta",
  "ClassVariables_Delta",
  "CoupledClasses_Delta"
)

# Filter to available metrics
available <- selected_metrics[selected_metrics %in% names(df)]
cat(sprintf("Available metrics: %d of %d\n", length(available), length(selected_metrics)))

if (length(available) < 2) {
  cat("Insufficient metrics for Scott-Knott analysis.\n")
  cat("With full dataset, this produces Table 10.\n")
  quit(status = 0)
}

if (!"reviewer_type" %in% names(df)) {
  cat("No reviewer_type column.\n")
  quit(status = 0)
}

# Reshape to long format
df_long <- df %>%
  select(thread_id, reviewer_type, all_of(available)) %>%
  pivot_longer(cols = all_of(available), names_to = "metric", values_to = "value") %>%
  filter(!is.na(value)) %>%
  mutate(group = paste0(gsub("_Delta", "", metric), " (", substr(reviewer_type, 1, 1), ")"))

# Create matrix for Scott-Knott
groups <- unique(df_long$group)
cat(sprintf("\nScott-Knott groups: %d\n", length(groups)))

if (length(groups) < 2) {
  cat("Insufficient groups for Scott-Knott.\n")
  quit(status = 0)
}

sk_data <- list()
for (g in groups) {
  vals <- df_long %>% filter(group == g) %>% pull(value)
  if (length(vals) >= 10) {
    sk_data[[g]] <- vals
  }
}

if (length(sk_data) < 2) {
  cat("Insufficient data for Scott-Knott (need >= 2 groups with 10+ values).\n")
  quit(status = 0)
}

# Pad and run
max_len <- max(sapply(sk_data, length))
# Sample to equal sizes for fairness
min_size <- min(sapply(sk_data, length))
set.seed(42)
sk_data_sampled <- lapply(sk_data, function(x) sample(x, min_size))

wide_df <- as.data.frame(sk_data_sampled, check.names = FALSE)
sk_results <- sk_esd(wide_df, version = "np", plot = FALSE)

cat("\nScott-Knott Rankings (Table 10):\n")
rankings <- data.frame(
  Group = names(sk_results$groups),
  Rank = as.numeric(sk_results$groups),
  Mean = sapply(sk_data, mean)
)
rankings <- rankings %>% arrange(Rank)
print(rankings)

# Save
output_csv <- file.path(output_dir, "sk_reviewer_metric_ranking.csv")
write.csv(rankings, output_csv, row.names = FALSE)
cat(sprintf("\nSaved: %s\n", output_csv))
