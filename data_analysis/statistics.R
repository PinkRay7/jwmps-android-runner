library(dplyr)
library(ggplot2)
library(tidyr)

# 
# winsorize <- function(x, lower_limit, upper_limit) {
#   x[x < lower_limit] <- lower_limit
#   x[x > upper_limit] <- upper_limit
#   return(x)
# }

df <- read.csv("run_table.csv")

df <- df %>%
  mutate(cpu_time_split = strsplit(as.character(cpu_time), ";"),
         memory_usage_split = strsplit(as.character(memory_usage), ";")) %>%
  mutate(cpu_time_small = as.numeric(sapply(cpu_time_split, `[`, 1)),
         cpu_time_medium = as.numeric(sapply(cpu_time_split, `[`, 2)),
         cpu_time_large = as.numeric(sapply(cpu_time_split, `[`, 3)),
         memory_usage_small = as.numeric(sapply(memory_usage_split, `[`, 1)),
         memory_usage_medium = as.numeric(sapply(memory_usage_split, `[`, 2)),
         memory_usage_large = as.numeric(sapply(memory_usage_split, `[`, 3))) %>%
  select(-cpu_time_split, -memory_usage_split, -cpu_time, -memory_usage)


# ====== mean median sd ======
summary_stats <- df %>%
  group_by(version) %>%
  summarise(
    # CPU time (small input)
    mean_cpu_small = mean(as.numeric(cpu_time_small), na.rm = TRUE),
    median_cpu_small = median(as.numeric(cpu_time_small), na.rm = TRUE),
    sd_cpu_small = sd(as.numeric(cpu_time_small), na.rm = TRUE),
    
    # CPU time (medium input)
    mean_cpu_medium = mean(as.numeric(cpu_time_medium), na.rm = TRUE),
    median_cpu_medium = median(as.numeric(cpu_time_medium), na.rm = TRUE),
    sd_cpu_medium = sd(as.numeric(cpu_time_medium), na.rm = TRUE),
    
    # CPU time (large input)
    mean_cpu_large = mean(as.numeric(cpu_time_large), na.rm = TRUE),
    median_cpu_large = median(as.numeric(cpu_time_large), na.rm = TRUE),
    sd_cpu_large = sd(as.numeric(cpu_time_large), na.rm = TRUE),
    
    # Memory usage (small input)
    mean_memory_small = mean(as.numeric(memory_usage_small), na.rm = TRUE),
    median_memory_small = median(as.numeric(memory_usage_small), na.rm = TRUE),
    sd_memory_small = sd(as.numeric(memory_usage_small), na.rm = TRUE),
    
    # Memory usage (medium input)
    mean_memory_medium = mean(as.numeric(memory_usage_medium), na.rm = TRUE),
    median_memory_medium = median(as.numeric(memory_usage_medium), na.rm = TRUE),
    sd_memory_medium = sd(as.numeric(memory_usage_medium), na.rm = TRUE),
    
    # Memory usage (large input)
    mean_memory_large = mean(as.numeric(memory_usage_large), na.rm = TRUE),
    median_memory_large = median(as.numeric(memory_usage_large), na.rm = TRUE),
    sd_memory_large = sd(as.numeric(memory_usage_large), na.rm = TRUE),
    
    # Energy usage (total)
    mean_energy = mean(as.numeric(total_energy), na.rm = TRUE),
    median_energy = median(as.numeric(total_energy), na.rm = TRUE),
    sd_energy = sd(as.numeric(total_energy), na.rm = TRUE),
    
    .groups = 'drop'
  )

print(summary_stats)

result <- df %>%
  group_by(function_name) %>%
  summarize(
    cpu_time_effect_small = (cpu_time_small[version == "normal"] - cpu_time_small[version == "memoized"]) /
      cpu_time_small[version == "normal"],
    cpu_time_effect_medium = (cpu_time_medium[version == "normal"] - cpu_time_medium[version == "memoized"]) /
      cpu_time_medium[version == "normal"],
    cpu_time_effect_large = (cpu_time_large[version == "normal"] - cpu_time_large[version == "memoized"]) /
      cpu_time_large[version == "normal"],
    
    memory_usage_effect_small = (memory_usage_small[version == "normal"] - memory_usage_small[version == "memoized"]) /
      memory_usage_small[version == "normal"],
    memory_usage_effect_medium = (memory_usage_medium[version == "normal"] - memory_usage_medium[version == "memoized"]) /
      memory_usage_medium[version == "normal"],
    memory_usage_effect_large = (memory_usage_large[version == "normal"] - memory_usage_large[version == "memoized"]) /
      memory_usage_large[version == "normal"],
    
    energy_effect = (total_energy[version == "normal"]-total_energy[version == "memoized"]) /
      total_energy[version == "normal"],
    
    .groups = 'drop'
  )

print(result)

# ===== effects stat =====
summary_effects <- result %>%
  summarise(
    # CPU time effect statistics
    mean_cpu_time_effect_small = mean(cpu_time_effect_small, na.rm = TRUE),
    median_cpu_time_effect_small = median(cpu_time_effect_small, na.rm = TRUE),
    sd_cpu_time_effect_small = sd(cpu_time_effect_small, na.rm = TRUE),
    
    mean_cpu_time_effect_medium = mean(cpu_time_effect_medium, na.rm = TRUE),
    median_cpu_time_effect_medium = median(cpu_time_effect_medium, na.rm = TRUE),
    sd_cpu_time_effect_medium = sd(cpu_time_effect_medium, na.rm = TRUE),
    
    mean_cpu_time_effect_large = mean(cpu_time_effect_large, na.rm = TRUE),
    median_cpu_time_effect_large = median(cpu_time_effect_large, na.rm = TRUE),
    sd_cpu_time_effect_large = sd(cpu_time_effect_large, na.rm = TRUE),
    
    # Memory usage effect statistics
    mean_memory_usage_effect_small = mean(memory_usage_effect_small, na.rm = TRUE),
    median_memory_usage_effect_small = median(memory_usage_effect_small, na.rm = TRUE),
    sd_memory_usage_effect_small = sd(memory_usage_effect_small, na.rm = TRUE),
    
    mean_memory_usage_effect_medium = mean(memory_usage_effect_medium, na.rm = TRUE),
    median_memory_usage_effect_medium = median(memory_usage_effect_medium, na.rm = TRUE),
    sd_memory_usage_effect_medium = sd(memory_usage_effect_medium, na.rm = TRUE),
    
    mean_memory_usage_effect_large = mean(memory_usage_effect_large, na.rm = TRUE),
    median_memory_usage_effect_large = median(memory_usage_effect_large, na.rm = TRUE),
    sd_memory_usage_effect_large = sd(memory_usage_effect_large, na.rm = TRUE),

    mean_energy_effect = mean(energy_effect, na.rm = TRUE),
    median_energy_effect = median(energy_effect, na.rm = TRUE),
    sd_energy_effect = sd(energy_effect, na.rm = TRUE),
    
  )

print(summary_effects)

summary_stats <- data %>%
  group_by(version) %>%
  summarise(across(all_of(numeric_cols), 
                   list(mean = ~mean(.), median = ~median(.), sd = ~sd(.)), 
                   .names = "{col}_{fn}"))
print(summary_stats)







