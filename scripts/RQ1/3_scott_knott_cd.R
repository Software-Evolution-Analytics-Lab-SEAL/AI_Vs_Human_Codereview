#!/usr/bin/env Rscript
#
# RQ1 - Figure 5: Scott-Knott ESD Rankings for Comment-to-Code Density
# Computes comment-to-code density (CD) per conversation and ranks review
# categories using Scott-Knott ESD (non-parametric).
# Produces: data/results/RQ1/4_2_cd_scottknott.csv
#
# Usage: Rscript 3_scott_knott_cd.R
#

suppressPackageStartupMessages({
  library(ScottKnottESD)
  library(dplyr)
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

# Try sample data first, fall back to full
input_file <- file.path(project_root, "data", "sample", "2_1_detail.csv")
if (!file.exists(input_file)) {
  input_file <- file.path(project_root, "data", "full", "2_1_detail.csv")
}

output_dir <- file.path(project_root, "data", "results", "RQ1")
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

cat("=== Scott-Knott ESD Ranking: Comment-to-Code Density (Figure 5) ===\n\n")

if (!file.exists(input_file)) {
  cat("Input file not found:", input_file, "\n")
  cat("Download the dataset from HuggingFace or run data collection first.\n")
  cat("Note: sample data produces approximate rankings; full data needed for paper results.\n")
  quit(status = 0)
}

df <- read.csv(input_file, stringsAsFactors = FALSE)
cat(sprintf("Loaded %d records from %s\n", nrow(df), basename(input_file)))

# Map review_category to short names
category_map <- c(
  "Human_Review_Human" = "HRH",
  "Human_Review_Agent"  = "HRA",
  "Agent_Review_Human"  = "ARH",
  "Agent_Review_Agent"  = "ARA"
)

df <- df %>%
  filter(review_category %in% names(category_map)) %>%
  mutate(category = category_map[review_category])

# Compute comment-to-code density: token_init_comment / LOC_no_blank
# Filter out rows where LOC_no_blank is missing or zero
df <- df %>%
  filter(!is.na(token_init_comment),
         !is.na(LOC_no_blank),
         LOC_no_blank > 0) %>%
  mutate(CD = token_init_comment / LOC_no_blank)

cat(sprintf("Valid records after filtering: %d\n", nrow(df)))
cat(sprintf("Categories: %s\n", paste(sort(unique(df$category)), collapse = ", ")))

categories <- sort(unique(df$category))
if (length(categories) < 2) {
  cat("Insufficient categories for Scott-Knott analysis (need >= 2).\n")
  quit(status = 0)
}

# Build data list for Scott-Knott ESD
sk_data <- list()
for (cat_name in categories) {
  vals <- df %>% filter(category == cat_name) %>% pull(CD)
  if (length(vals) >= 10) {
    sk_data[[cat_name]] <- vals
    cat(sprintf("  %s: %d conversations, mean CD = %.4f\n",
                cat_name, length(vals), mean(vals)))
  } else {
    cat(sprintf("  %s: only %d conversations (skipped, need >= 10)\n",
                cat_name, length(vals)))
  }
}

if (length(sk_data) < 2) {
  cat("Insufficient data for Scott-Knott (need >= 2 groups with 10+ values).\n")
  quit(status = 0)
}

# Sample to equal sizes for fairness
min_size <- min(sapply(sk_data, length))
set.seed(42)
sk_data_sampled <- lapply(sk_data, function(x) sample(x, min_size))
cat(sprintf("\nSampled each group to %d values for balanced comparison\n", min_size))

# Run Scott-Knott ESD (non-parametric)
wide_df <- as.data.frame(sk_data_sampled, check.names = FALSE)
sk_results <- sk_esd(wide_df, version = "np", plot = FALSE)

# Build output matching expected format
group_letters <- letters[as.numeric(sk_results$groups)]
rankings <- data.frame(
  category = names(sk_results$groups),
  SK_group = group_letters,
  SK_rank  = as.numeric(sk_results$groups),
  mean_val = sapply(names(sk_results$groups), function(g) mean(sk_data[[g]])),
  stringsAsFactors = FALSE
)
rankings <- rankings %>% arrange(SK_rank)

cat("\nScott-Knott ESD Rankings (Figure 5):\n")
print(rankings, row.names = FALSE)

# Save
output_csv <- file.path(output_dir, "4_2_cd_scottknott.csv")
write.csv(rankings, output_csv, row.names = FALSE)
cat(sprintf("\nSaved: %s\n", output_csv))
cat("\nNote: sample data may produce different rankings than full dataset.\n")
