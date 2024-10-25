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
  filter(function_name == "All Possible Full Binary Trees")

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

# 2. Paired t-test
# 2.1 Paired t-test for small input
t_test_small <- t.test(function_data$small_input[function_data$version == "normal"],
                       function_data$small_input[function_data$version == "memoized"],
                       paired = TRUE)

# 2.2 Paired t-test for medium input
t_test_medium <- t.test(function_data$medium_input[function_data$version == "normal"],
                        function_data$medium_input[function_data$version == "memoized"],
                        paired = TRUE)

# 2.3 Paired t-test for large input
t_test_large <- t.test(function_data$large_input[function_data$version == "normal"],
                       function_data$large_input[function_data$version == "memoized"],
                       paired = TRUE)

t_test_small
t_test_medium
t_test_large

# 3. Effect size
# 3.1 Calculate Cohen's d for small input
cohen_d_small <- cohen.d(function_data$small_input[function_data$version == "normal"],
                         function_data$small_input[function_data$version == "memoized"])

# 3.2 Calculate Cohen's d for medium input
cohen_d_medium <- cohen.d(function_data$medium_input[function_data$version == "normal"],
                          function_data$medium_input[function_data$version == "memoized"])

# 3.3 Calculate Cohen's d for large input
cohen_d_large <- cohen.d(function_data$large_input[function_data$version == "normal"],
                         function_data$large_input[function_data$version == "memoized"])

cohen_d_small
cohen_d_medium
cohen_d_large