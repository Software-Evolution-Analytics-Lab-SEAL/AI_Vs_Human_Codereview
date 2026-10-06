#!/usr/bin/env Rscript
#
# RQ3 - Table 10: Scott-Knott ESD Rankings by Feedback Type
# and Table 12: Code Metrics Comparison (Human vs Agent)
#
# Produces: Tables 10 and 12 in the paper.
#
# Usage: Rscript 6_code_metrics_R.R
#

suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(effsize)
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
input_file <- file.path(project_root, "data", "sample", "rq3_raw_metrics.csv")
metadata_file <- file.path(project_root, "data", "sample", "rq3_joined_data.csv")
output_dir <- file.path(project_root, "results", "RQ3")
tables_dir <- file.path(project_root, "results", "tables")

if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
if (!dir.exists(tables_dir)) dir.create(tables_dir, recursive = TRUE)

cat("=== RQ3 Code Metrics Analysis (R) ===\n\n")

# Load data
if (!file.exists(input_file)) {
  cat(sprintf("Input file not found: %s\n", input_file))
  cat("Download full dataset from HuggingFace for complete results.\n")
  quit(status = 0)
}

df <- read.csv(input_file, stringsAsFactors = FALSE)
cat(sprintf("Loaded %d metric records\n", nrow(df)))

# Load metadata for reviewer type
if (file.exists(metadata_file)) {
  meta <- read.csv(metadata_file, stringsAsFactors = FALSE)
  meta <- meta %>% select(thread_id, reviewer_type) %>% distinct()
  df <- df %>% mutate(thread_id = as.character(thread_id))
  meta <- meta %>% mutate(thread_id = as.character(thread_id))
  df <- df %>% left_join(meta, by = "thread_id")
}

if (!"reviewer_type" %in% names(df)) {
  cat("No reviewer_type column. Cannot compare Human vs Agent.\n")
  quit(status = 0)
}

# Find delta columns
delta_cols <- grep("_Delta$", names(df), value = TRUE)
cat(sprintf("Found %d delta metrics\n", length(delta_cols)))

if (length(delta_cols) == 0) {
  cat("No delta columns found.\n")
  quit(status = 0)
}

# Metric categories
complexity_metrics <- delta_cols[grepl("Cyclomatic|Complexity", delta_cols, ignore.case = TRUE)]
coupling_metrics <- delta_cols[grepl("Coupled|Input|Output|Base|Derived", delta_cols, ignore.case = TRUE)]
cohesion_metrics <- delta_cols[grepl("Cohesion|LackOf", delta_cols, ignore.case = TRUE)]

# Table 12: Summary by reviewer type
cat("\n=== Table 12: Code Metrics Comparison ===\n")

results <- data.frame()
for (col in delta_cols) {
  human_vals <- df %>% filter(reviewer_type == "Human") %>% pull(!!sym(col)) %>% na.omit()
  agent_vals <- df %>% filter(reviewer_type == "Agent") %>% pull(!!sym(col)) %>% na.omit()

  if (length(human_vals) < 5 || length(agent_vals) < 5) next

  # Wilcoxon test
  test_result <- tryCatch(
    wilcox.test(human_vals, agent_vals),
    error = function(e) list(p.value = NA)
  )

  # Cliff's delta
  cd <- tryCatch(
    cliff.delta(human_vals, agent_vals),
    error = function(e) list(estimate = NA, magnitude = "NA")
  )

  results <- rbind(results, data.frame(
    Metric = gsub("_Delta$", "", col),
    Mean_Human = round(mean(human_vals), 4),
    Mean_Agent = round(mean(agent_vals), 4),
    Median_Human = round(median(human_vals), 4),
    Median_Agent = round(median(agent_vals), 4),
    P_Value = test_result$p.value,
    Cliffs_Delta = round(cd$estimate, 4),
    Effect = as.character(cd$magnitude),
    stringsAsFactors = FALSE
  ))
}

results <- results %>% arrange(P_Value)
print(results)

# Save
output_csv <- file.path(output_dir, "metrics_by_reviewer.csv")
write.csv(results, output_csv, row.names = FALSE)
cat(sprintf("\nSaved: %s\n", output_csv))

cat("\n=== Analysis Complete ===\n")
cat("With sample data, results may not reach statistical significance.\n")
cat("Use the full dataset from HuggingFace for paper-ready results.\n")
