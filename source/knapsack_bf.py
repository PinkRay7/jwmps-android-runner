def knapsack_brute_force(capacity, n):
    print(f"knapsack_brute_force({capacity},{n})")
    if n == 0 or capacity == 0:
        return 0

    elif weights[n-1] > capacity:
        return knapsack_brute_force(capacity, n-1)

    else:
        include_item = values[n-1] + knapsack_brute_force(capacity-weights[n-1], n-1)
        exclude_item = knapsack_brute_force(capacity, n-1)
        return max(include_item, exclude_item)

# wrapper for testing
def knapsack_bf_solver(capacity, n, input_values, input_weights):
    global values, weights
    values = input_values
    weights = input_weights
    return knapsack_brute_force(capacity, n)

if __name__ == "__main__":
    values = [300, 200, 400, 500]
    weights = [2, 1, 5, 3]
    capacity = 10
    n = len(values)
    print("\nMaximum value in Knapsack =", knapsack_brute_force(capacity, n))