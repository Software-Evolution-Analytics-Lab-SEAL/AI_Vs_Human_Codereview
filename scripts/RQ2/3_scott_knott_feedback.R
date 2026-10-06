#!/usr/bin/env Rscript
#
# RQ2 - Scott-Knott ESD Ranking of Feedback Types by Discussion Rounds
# Ranks feedback types by average comment count (discussion length) for each
# review category (HRH, HRA, ARH, ARA).
# Produces: 3_1Taxonomy_Rank_{HRH,HRA,ARH,ARA}.csv and
#           RQ2_fdbtype_turns_per_category.csv
#
# Usage: Rscript 3_scott_knott_feedback.R
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
input_file <- file.path(project_root, "data", "sample", "rq2_fdbtype_detail.csv")
output_dir <- file.path(project_root, "data", "results", "RQ2")

if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

cat("=== Scott-Knott ESD Ranking: Feedback Types by Discussion Rounds ===\n\n")

if (!file.exists(input_file)) {
  cat("Input file not found. Download full dataset from HuggingFace.\n")
  quit(status = 0)
}

df <- read.csv(input_file, stringsAsFactors = FALSE)
cat(sprintf("Loaded %d records\n", nrow(df)))

# Map review_category labels to short names
category_map <- c(
  "Human_Review_Human" = "HRH",
  "Human_Review_Agent" = "HRA",
  "Agent_Review_Human" = "ARH",
  "Agent_Review_Agent" = "ARA"
)

df <- df %>%
  mutate(category = ifelse(review_category %in% names(category_map),
                           category_map[review_category],
                           review_category))

categories <- c("HRH", "HRA", "ARH", "ARA")
all_rankings <- list()

for (cat_name in categories) {
  cat(sprintf("\n--- Processing %s ---\n", cat_name))

  df_cat <- df %>% filter(category == cat_name)
  cat(sprintf("Records: %d\n", nrow(df_cat)))

  if (nrow(df_cat) == 0) {
    cat(sprintf("No data for %s, skipping.\n", cat_name))
    next
  }

  # Summarise per feed_type
  summary_cat <- df_cat %>%
    group_by(feed_type) %>%
    summarise(
      Mean_ATC = mean(comment_count, na.rm = TRUE),
      Median_ATC = median(comment_count, na.rm = TRUE),
      N = n(),
      .groups = "drop"
    )

  # Build data list for Scott-Knott ESD
  feed_types <- unique(df_cat$feed_type)
  sk_data <- list()
  for (ft in feed_types) {
    vals <- df_cat %>% filter(feed_type == ft) %>% pull(comment_count)
    if (length(vals) >= 10) {
      sk_data[[ft]] <- vals
    } else {
      cat(sprintf("  Skipping '%s' (n=%d < 10)\n", ft, length(vals)))
    }
  }

  if (length(sk_data) < 2) {
    cat(sprintf("Insufficient groups for Scott-Knott in %s.\n", cat_name))
    # Save summary without ranks
    result <- summary_cat %>%
      mutate(Rank = NA_integer_) %>%
      select(feed_type, Rank, Mean_ATC, Median_ATC, N) %>%
      arrange(desc(Mean_ATC))
    output_csv <- file.path(output_dir, paste0("3_1Taxonomy_Rank_", cat_name, ".csv"))
    write.csv(result, output_csv, row.names = FALSE)
    cat(sprintf("Saved: %s\n", output_csv))
    all_rankings[[cat_name]] <- result
    next
  }

  # Sample to equal sizes for Scott-Knott ESD
  min_size <- min(sapply(sk_data, length))
  set.seed(42)
  sk_data_sampled <- lapply(sk_data, function(x) sample(x, min_size))

  wide_df <- as.data.frame(sk_data_sampled, check.names = FALSE)
  sk_results <- sk_esd(wide_df, version = "np", plot = FALSE)

  # Build ranking table
  ranking_df <- data.frame(
    feed_type = names(sk_results$groups),
    Rank = as.numeric(sk_results$groups),
    stringsAsFactors = FALSE
  )

  result <- ranking_df %>%
    left_join(summary_cat, by = "feed_type") %>%
    select(feed_type, Rank, Mean_ATC, Median_ATC, N) %>%
    arrange(Rank, desc(Mean_ATC))

  cat(sprintf("Scott-Knott Rankings for %s:\n", cat_name))
  print(result)

  output_csv <- file.path(output_dir, paste0("3_1Taxonomy_Rank_", cat_name, ".csv"))
  write.csv(result, output_csv, row.names = FALSE)
  cat(sprintf("Saved: %s\n", output_csv))

  all_rankings[[cat_name]] <- result
}

# Build combined table: RQ2_fdbtype_turns_per_category.csv
# Format: Taxonomy, then for each category: R, AvgC, >1C
cat("\n--- Building combined table ---\n")

all_feed_types <- unique(unlist(lapply(all_rankings, function(r) r$feed_type)))

combined <- data.frame(Taxonomy = all_feed_types, stringsAsFactors = FALSE)

for (cat_name in categories) {
  if (!is.null(all_rankings[[cat_name]])) {
    rank_df <- all_rankings[[cat_name]]

    # Compute >1C percentage from raw data
    df_cat <- df %>% filter(category == cat_name)
    multi_pct <- df_cat %>%
      group_by(feed_type) %>%
      summarise(
        pct_multi = round(100 * mean(comment_count > 1, na.rm = TRUE), 1),
        .groups = "drop"
      )

    cat_info <- rank_df %>%
      left_join(multi_pct, by = "feed_type") %>%
      mutate(
        AvgC = round(Mean_ATC, 1)
      ) %>%
      select(feed_type, R = Rank, AvgC, pct_multi)

    names(cat_info)[2:4] <- paste0(cat_name, c("_R", "_AvgC", "_>1C"))
    combined <- combined %>%
      left_join(cat_info, by = c("Taxonomy" = "feed_type"))
  }
}

# Reformat column names to match expected output
header_row1 <- c("Taxonomy", rep(categories, each = 3))
header_row2 <- c("", rep(c("R", "AvgC", ">1C"), length(categories)))

# Write combined CSV with multi-row header
combined_file <- file.path(output_dir, "RQ2_fdbtype_turns_per_category.csv")
con <- file(combined_file, open = "wt")
writeLines(paste(header_row1, collapse = ","), con)
writeLines(paste(header_row2, collapse = ","), con)
for (i in seq_len(nrow(combined))) {
  row_vals <- as.character(unlist(combined[i, ]))
  row_vals[is.na(row_vals)] <- ""
  writeLines(paste(row_vals, collapse = ","), con)
}
close(con)

cat(sprintf("\nSaved combined table: %s\n", combined_file))
cat("\nDone.\n")
