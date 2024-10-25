library(tidyverse)
library(ggplot2)
library(readr)
library(effsize)

# Load data
df <- read_csv("run_table.csv")

# Extract data for target function
function_data <- df %>%
  filter(function_name == "All Possible Full Binary Trees")

# Convert total energy to numeric
function_data <- function_data %>%
  mutate(total_energy = as.numeric(total_energy))

# 1. Normality check
# 1.1 Calculate the difference between normal and memoized
energy_diff <- with(function_data, total_energy[version == "normal"] - total_energy[version == "memoized"])

# 1.2 Plot Q-Q plots for normality check
qqnorm(energy_diff); qqline(energy_diff, col = "red")

# 1.3 Shapiro-Wilk test for normality
shapiro.test(energy_diff)

# 2. Paired t-test
t_test_energy <- t.test(function_data$total_energy[function_data$version == "normal"],
                        function_data$total_energy[function_data$version == "memoized"],
                        paired = TRUE)

t_test_energy

# 3. Calculate Cohen's d
cohen_d_energy <- cohen.d(function_data$total_energy[function_data$version == "normal"],
                          function_data$total_energy[function_data$version == "memoized"])

cohen_d_energy