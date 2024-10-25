library(dplyr)

df <- read.csv("run_table.csv")

# Split 'memory_usage' column into small, medium, large
df <- df %>%
  mutate(memory_usages = strsplit(as.character(memory_usage), ";")) %>%
  unnest_wider(memory_usages, names_sep = "_") %>%
  rename(small_input = memory_usages_1, medium_input = memory_usages_2, large_input = memory_usages_3)

# Convert memory usages to numeric
df <- df %>%
  mutate(across(starts_with("small_input"), as.numeric),
         across(starts_with("medium_input"), as.numeric),
         across(starts_with("large_input"), as.numeric))

# Extract data for target function
function_data <- df %>%
  filter(function_name == "All Possible Full Binary Trees")

# Separate the data into normal and memoized versions
normal_data <- filter(function_data, version == "normal")
memoized_data <- filter(function_data, version == "memoized")

# Calculate mean memory usage for small, medium, and large inputs for normal version
mean_normal_small <- mean(normal_data$small_input)
mean_normal_medium <- mean(normal_data$medium_input)
mean_normal_large <- mean(normal_data$large_input)

# Calculate mean memory usage for small, medium, and large inputs for memoized version
mean_memoized_small <- mean(memoized_data$small_input)
mean_memoized_medium <- mean(memoized_data$medium_input)
mean_memoized_large <- mean(memoized_data$large_input)

# Calculate the effect size
effect_size_small <- mean_memoized_small - mean_normal_small
effect_size_medium <- mean_memoized_medium - mean_normal_medium
effect_size_large <- mean_memoized_large - mean_normal_large

# Print the results
cat("Mean Memory Usage (Normal Version):\n")
mean_normal_small
mean_normal_medium
mean_normal_large

cat("Mean Memory Usage (Memoized Version):\n")
mean_memoized_small
mean_memoized_medium
mean_memoized_large

cat("Effect Size:\n")
effect_size_small
effect_size_medium
effect_size_large
