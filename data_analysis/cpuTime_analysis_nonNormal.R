library(tidyverse)
library(ggplot2)
library(readr)
library(effsize)

# Load data
df <- read_csv("run_table.csv")

# Split 'cpu_time' column into small, medium, large
df <- df %>%
  mutate(cpu_times = strsplit(as.character(cpu_time), ";")) %>%
  unnest_wider(cpu_times, names_sep = "_") %>%
  rename(small_input = cpu_times_1, medium_input = cpu_times_2, large_input = cpu_times_3)

# Convert cpu times to numeric
df <- df %>%
  mutate(across(starts_with("small_input"), as.numeric),
         across(starts_with("medium_input"), as.numeric),
         across(starts_with("large_input"), as.numeric))

# Extract data for target function
function_data <- df %>%
  filter(function_name == "K-equal Sum Partitions")

# 1. Normality check
# 1.1 Calculate the difference between normal and memoized for each input size
diff_small <- with(function_data, small_input[version == "normal"] - small_input[version == "memoized"])
diff_medium <- with(function_data, medium_input[version == "normal"] - medium_input[version == "memoized"])
diff_large <- with(function_data, large_input[version == "normal"] - large_input[version == "memoized"])

# 1.2 Plot Q-Q plots for normality check
qqnorm(diff_small); qqline(diff_small, col = "red")
qqnorm(diff_medium); qqline(diff_medium, col = "red")
qqnorm(diff_large); qqline(diff_large, col = "red")

# 1.3 Shapiro-Wilk test for normality
shapiro.test(diff_small)
shapiro.test(diff_medium)
shapiro.test(diff_large)

# 2. Wilcoxon Rank-Sum test
# 2.1 Wilcoxon test for small input
wilcox_test_small <- wilcox.test(function_data$small_input[function_data$version == "normal"],
                                 function_data$small_input[function_data$version == "memoized"],
                                 paired = TRUE)

# 2.2 Wilcoxon test for medium input
wilcox_test_medium <- wilcox.test(function_data$medium_input[function_data$version == "normal"],
                                  function_data$medium_input[function_data$version == "memoized"],
                                  paired = TRUE)

# 2.3 Wilcoxon test for large input
wilcox_test_large <- wilcox.test(function_data$large_input[function_data$version == "normal"],
                                 function_data$large_input[function_data$version == "memoized"],
                                 paired = TRUE)

wilcox_test_small
wilcox_test_medium
wilcox_test_large

# 3. Effect size using Cliff's delta
# 3.1 Cliff's delta for small input
cliff_delta_small <- cliff.delta(function_data$small_input[function_data$version == "normal"],
                                 function_data$small_input[function_data$version == "memoized"])

# 3.2 Cliff's delta for medium input
cliff_delta_medium <- cliff.delta(function_data$medium_input[function_data$version == "normal"],
                                  function_data$medium_input[function_data$version == "memoized"])

# 3.3 Cliff's delta for large input
cliff_delta_large <- cliff.delta(function_data$large_input[function_data$version == "normal"],
                                 function_data$large_input[function_data$version == "memoized"])

cliff_delta_small
cliff_delta_medium
cliff_delta_large