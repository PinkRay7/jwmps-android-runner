library(dplyr)
library(ggplot2)
library(tidyr)

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

result <- df %>%
  group_by(function_name) %>%
  summarize(
    execution_time_effect_small = (cpu_time_small[version == "normal"] - cpu_time_small[version == "memoized"]) /
      cpu_time_small[version == "normal"],
    execution_time_effect_medium = (cpu_time_medium[version == "normal"] - cpu_time_medium[version == "memoized"]) /
      cpu_time_medium[version == "normal"],
    execution_time_effect_large = (cpu_time_large[version == "normal"] - cpu_time_large[version == "memoized"]) /
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

result_long_cpu <- result %>%
  pivot_longer(cols = starts_with("execution_time_effect"),
               names_to = "input_size",
               values_to = "execution_time_effect")

result_long_memory <- result %>%
  pivot_longer(cols = starts_with("memory_usage_effect"),
               names_to = "input_size",
               values_to = "memory_usage_effect")

# === execution time effect bar chart ===
ggplot(result_long_cpu, aes(x = function_name, y = execution_time_effect, fill = input_size)) +
  geom_bar(stat = "identity", position = position_dodge()) +
  labs(x = "Function",
       y = "Execution Time Effect",
       fill = "Input Size") +
  theme_minimal() + theme(axis.text.x = element_text(angle = 65, hjust = 1))

# === memory usage effect bar chart ===
ggplot(result_long_memory, aes(x = function_name, y = memory_usage_effect, fill = input_size)) +
  geom_bar(stat = "identity", position = position_dodge()) +
  labs(x = "Function",
       y = "Memory Usage Effect",
       fill = "Input Size") +
  theme_minimal() + theme(axis.text.x = element_text(angle = 65, hjust = 1))

# === energy effect bar chart ===
ggplot(result, aes(x = function_name, y = energy_effect, fill = function_name)) +
  geom_bar(stat = "identity") +
  labs(x = NULL,  
       y = "Energy Effect") +
  theme_minimal() +
  theme(axis.text.x = element_blank(),
        legend.position = "right") + 
  guides(fill = guide_legend(title = "Function Names"))

# === execution time box plot ===
par(mfrow = c(1, 3)) 
boxplot(as.numeric(cpu_time_small) ~ version, data = df, 
        main = "Execution Time (Small)", 
        xlab = "Version", ylab = "Execution Time (seconds)", 
        col = c("skyblue", "orange"))

boxplot(as.numeric(cpu_time_medium) ~ version, data = df, 
        main = "Execution Time (Medium)", 
        xlab = "Version", ylab = "Execution Time (seconds)", 
        col = c("skyblue", "orange"))

boxplot(as.numeric(cpu_time_large) ~ version, data = df, 
        main = "Execution Time (Large)", 
        xlab = "Version", ylab = "Execution Time (seconds)", 
        col = c("skyblue", "orange"))

# === memory usage box plot
par(mfrow = c(1, 3)) 
boxplot(as.numeric(memory_usage_small) ~ version, data = df, 
        main = "Memory Usage (Small)", 
        xlab = "Version", ylab = "Memory Usage (MB)", 
        col = c("skyblue", "orange"), outline = FALSE)

boxplot(as.numeric(memory_usage_medium) ~ version, data = df, 
        main = "Memory Usage (Medium)", 
        xlab = "Version", ylab = "Memory Usage (MB)", 
        col = c("skyblue", "orange"), outline = FALSE)

boxplot(as.numeric(memory_usage_large) ~ version, data = df, 
        main = "Memory Usage (Large)", 
        xlab = "Version", ylab = "Memory Usage (MB)", 
        col = c("skyblue", "orange"), outline = FALSE)

boxplot(as.numeric(total_energy) ~ version, data = df, 
        main = "Total Energy Usage", 
        xlab = "Version", ylab = "Energy Usage (Joules)", 
        col = c("skyblue", "orange"))

# === scatter plot ===
par(mfrow = c(1, 1)) 
colors <- rainbow(length(unique(df$function_name)))
function_colors <- as.factor(df$function_name)

# Distinguish version with solid and hollow pch values (1 = normal, 2 = memoized)
input_size_shapes <- list(
  small = c(16, 1),    # Circle (solid, hollow)
  medium = c(17, 2),   # Triangle
  large = c(18, 5)     # Square
)

plot(NA, NA, xlim = c(0, max(as.numeric(df$memory_usage_large), na.rm = TRUE)), 
     ylim = c(0, max(as.numeric(df$cpu_time_large), na.rm = TRUE)), 
     xlab = "Memory Usage (MB)", ylab = "Execution Time (seconds)",  pch = 19)

# small input
points(as.numeric(df$memory_usage_small), as.numeric(df$cpu_time_small), 
       col = colors[as.numeric(function_colors)], 
       pch = ifelse(df$version == "normal", input_size_shapes$small[1], input_size_shapes$small[2]))

# medium input
points(as.numeric(df$memory_usage_medium), as.numeric(df$cpu_time_medium), 
       col = colors[as.numeric(function_colors)], 
       pch = ifelse(df$version == "normal", input_size_shapes$medium[1], input_size_shapes$medium[2]))

# large input
points(as.numeric(df$memory_usage_large), as.numeric(df$cpu_time_large), 
       col = colors[as.numeric(function_colors)], 
       pch = ifelse(df$version == "normal", input_size_shapes$large[1], input_size_shapes$large[2]))

legend("topright", 
       legend = levels(function_colors), 
       col = colors, 
       pch = 16, 
       title = "Function Name",
       cex = 0.8,             
       y.intersp = 0.7,   
       x.intersp = 0.5   
       
)

legend("bottomright", 
       legend = c("Small (Normal)", "Small (Memoized)", 
                  "Medium (Normal)", "Medium (Memoized)", 
                  "Large (Normal)", "Large (Memoized)"), 
       pch = c(input_size_shapes$small[1], input_size_shapes$small[2], 
               input_size_shapes$medium[1], input_size_shapes$medium[2], 
               input_size_shapes$large[1], input_size_shapes$large[2]),
       title = "Input Size",
       cex = 0.8,           
       y.intersp = 0.7,  
       x.intersp = 0.5
)

# ===== density =====
par(mfrow = c(1, 2)) 

# === density cpu time ===
df_long_cpu <- df %>%
  pivot_longer(cols = c(cpu_time_small, cpu_time_medium, cpu_time_large), 
               names_to = "input_size", values_to = "execution_time")

ggplot(df_long_cpu, aes(x=as.numeric(execution_time), fill=version)) + 
  geom_density(alpha=0.5) +
  labs( x="Execution Time (seconds)", y="Density") +
  facet_wrap(~input_size, scales = "free") +
  theme_minimal() +
  theme(legend.position = "top")

# === density memory ===
df_long_mem <- df %>%
  pivot_longer(cols = c(memory_usage_small, memory_usage_medium, memory_usage_large), 
               names_to = "input_size", values_to = "memory_usage")

ggplot(df_long_mem, aes(x=as.numeric(log(memory_usage)), fill=version)) + 
  geom_density(alpha=0.5) +
  labs( x="Memory Usage (log(MB))", y="Density") +
  facet_wrap(~input_size, scales = "free") +
  theme_minimal() +
  theme(legend.position = "top")


