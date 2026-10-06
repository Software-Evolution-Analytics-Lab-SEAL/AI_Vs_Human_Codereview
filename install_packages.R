# R packages required for statistical analysis
# Install with: Rscript install_packages.R

packages <- c(
  "ScottKnottESD",  # Scott-Knott Effect Size Difference test
  "dplyr",          # Data manipulation
  "tidyr",          # Data reshaping
  "ggplot2",        # Plotting
  "effsize"         # Effect size calculations (Cliff's Delta)
)

for (pkg in packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg, repos = "https://cloud.r-project.org/")
  }
  cat(sprintf("  %s: OK\n", pkg))
}

cat("\nAll R packages installed successfully.\n")
