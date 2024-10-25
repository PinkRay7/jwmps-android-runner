# import functools

# # general memoize decorator
# def memoize(func):
#     cache = {}
#     @functools.wraps(func)
#     def memoized_func(*args):
#         if args in cache:
#             return cache[args]
#         else:
#             result = func(*args)
#             cache[args] = result
#             return result
#     memoized_func.cache = cache
#     return memoized_func

# # unhashable 
# def memoize_unhashable(func):
#     cache = {}
#     @functools.wraps(func)
#     def memoized_func(*args):
#         key = tuple((tuple(arg) if isinstance(arg, list) else arg) for arg in args)
#         if key in cache:
#             return cache[key]
#         else:
#             result = func(*args)
#             cache[key] = result
#             return result
#     return memoized_func

# # 1. Fibonacci sequence
# def fibonacci(n):
#     if n == 0:
#         return 0
#     if n == 1 or n == 2:
#         return 1
#     return fibonacci(n - 1) + fibonacci(n - 2)
# # def fibonacci(n):
# #     if n == 0:
# #         return 0
# #     elif n == 1:
# #         return 1
# #     prev, curr = 0, 1
# #     for _ in range(2, n + 1):
# #         prev, curr = curr, prev + curr
# #     return curr

# fibonacci_memo = memoize(fibonacci)
# # test
# def test_fibonacci():
#     n = 10
#     print("Fibonacci without memoization:", fibonacci(n))
#     print("Fibonacci with memoization:", fibonacci_memo(n))


# # 2. 0-1 Knapsack problem
# def knapsack(W, weights, values, n):
#     if n == 0 or W == 0:
#         return 0
    
#     if weights[n-1] > W:
#         return knapsack(W, weights, values, n-1)

#     else:
#         include_item = values[n-1] + knapsack(W - weights[n-1], weights, values, n-1)
#         exclude_item = knapsack(W, weights, values, n-1)
#         return max(include_item, exclude_item)

# knapsack_memo = memoize_unhashable(knapsack)
# # test
# def test_knapsack():
#     weights = (10, 20, 30)
#     values = (60, 100, 120)
#     W = 50
#     n = len(weights)
#     print("Knapsack without memoization:", knapsack(W, n, weights, values))
#     print("Knapsack with memoization:", knapsack_memo(W, n, weights, values))



# # 3. Coin Change problem
# def coin_change(coins, amount):
#     if amount == 0:
#         return 0

#     if amount < 0:
#         return -1
    
#     min_coins = float('inf')
    
#     for coin in coins:
#         result = coin_change(coins, amount - coin)

#         if result != -1:
#             min_coins = min(min_coins, result + 1)

#     return min_coins if min_coins != float('inf') else -1

# coin_change_memo = memoize_unhashable(coin_change)
# #test
# def test_coin_change():
#     coins = (1, 2, 3)
#     m = len(coins)
#     n = 4  
#     print("Coin Change without memoization:", coin_change(m, n, coins))
#     print("Coin Change with memoization:", coin_change_memo(m, n, coins))



# # 4. Levenshtein Distance
# def levenshtein_distance(s1, s2):
#     if len(s1) == 0:
#         return len(s2)
#     if len(s2) == 0:
#         return len(s1)

#     if s1[-1] == s2[-1]:
#         return levenshtein_distance(s1[:-1], s2[:-1])
    
#     return 1 + min(
#         levenshtein_distance(s1, s2[:-1]),    # Insert
#         levenshtein_distance(s1[:-1], s2),    # Remove
#         levenshtein_distance(s1[:-1], s2[:-1]) # Replace
#     )

# levenshtein_distance_memo = memoize(levenshtein_distance)
# #test
# def test_levenshtein_distance():
#     s1 = "kitten"
#     s2 = "sitting"
#     print("Levenshtein Distance without memoization:", levenshtein_distance(s1, s2))
#     print("Levenshtein Distance with memoization:", levenshtein_distance_memo(s1, s2))



# # 5. Factorial calculation
# def factorial(n):
#     if n == 0:
#         return 1
#     else:
#         return n * factorial(n - 1)
# # def factorial(n):
# #     result = 1
# #     for i in range(2, n + 1):
# #         result *= i
# #     return result

# factorial_memo = memoize(factorial)
# #test
# def test_factorial():
#     n = 5
#     print("Factorial without memoization:", factorial(n))
#     print("Factorial with memoization:", factorial_memo(n))



# # 6. Matrix Chain Multiplication
# def matrix_chain_order(i, j, dimensions):
#     if i == j:
#         return 0
#     min_count = float('inf')
#     for k in range(i, j):
#         count = (
#             matrix_chain_order(i, k, dimensions)
#             + matrix_chain_order(k + 1, j, dimensions)
#             + dimensions[i - 1] * dimensions[k] * dimensions[j]
#         )
#         if count < min_count:
#             min_count = count
#     return min_count

# matrix_chain_order_memo = memoize(matrix_chain_order)
# #test
# def test_matrix_chain_order():
#     dimensions = (1, 2, 3, 4)
#     n = len(dimensions) - 1
#     print("Matrix Chain Order without memoization:", matrix_chain_order(1, n, dimensions))
#     print("Matrix Chain Order with memoization:", matrix_chain_order_memo(1, n, dimensions))




# # # 7. Can I Win game
# # def can_win(remaining, chosen, maxChoosableInteger, desiredTotal):
# #     if remaining >= desiredTotal:
# #         return False

# #     for i in range(1, maxChoosableInteger + 1):
# #         if i not in chosen:
# #             if not can_win(remaining + i, chosen + [i], maxChoosableInteger, desiredTotal):
# #                 return True

# #     return False

# # def can_i_win(maxChoosableInteger, desiredTotal):
# #     total_sum = (maxChoosableInteger * (maxChoosableInteger + 1)) // 2
# #     if total_sum < desiredTotal:
# #         return False
    
# #     return can_win(0, [], maxChoosableInteger, desiredTotal)

# # def can_i_win_memo(maxChoosableInteger, desiredTotal):
# #     total_sum = (maxChoosableInteger * (maxChoosableInteger + 1)) // 2
# #     if total_sum < desiredTotal:
# #         return False

# #     # Start the game with a total of 0 and no chosen numbers
# #     return memoize(can_win(0, [], maxChoosableInteger, desiredTotal))
# # #test
# # def test_can_i_win():
# #     max_int = 10
# #     desired_total = 11
# #     print("Can I Win:", can_i_win(max_int, desired_total))
# def can_i_win(max_int, desired_total):
#     if desired_total <= 0:
#         return True
#     if (max_int * (max_int + 1)) // 2 < desired_total:
#         return False

#     memo = {}
#     def can_win(used, total):
#         if used in memo:
#             return memo[used]
#         for i in range(max_int):
#             curr = 1 << i
#             if not used & curr:
#                 if total + i + 1 >= desired_total:
#                     memo[used] = True
#                     return True
#                 if not can_win(used | curr, total + i + 1):
#                     memo[used] = True
#                     return True
#         memo[used] = False
#         return False

#     return can_win(0, 0)

# # 7. Can I Win game no memo
# def can_i_win_non_memo(max_int, desired_total):
#     if desired_total <= 0:
#         return True
#     if (max_int * (max_int + 1)) // 2 < desired_total:
#         return False

#     def can_win(used, total):
#         for i in range(max_int):
#             curr = 1 << i
#             if not used & curr:
#                 if total + i + 1 >= desired_total:
#                     return True
#                 if not can_win(used | curr, total + i + 1):
#                     return True
#         return False

#     return can_win(0, 0)


# # 8. K-equal sum array partitions
# def can_partition_k_subsets(nums, k):
#     total_sum = sum(nums)
    
#     if total_sum % k != 0:
#         return False

#     target = total_sum // k
#     nums.sort(reverse=True)
#     subsets = [0] * k

#     def backtrack(index):
#         if index == len(nums):
#             return all(subset == target for subset in subsets)
        
#         for i in range(k):
#             if subsets[i] + nums[index] <= target:
#                 subsets[i] += nums[index]
#                 if backtrack(index + 1):
#                     return True
#                 subsets[i] -= nums[index]

#             if subsets[i] == 0:
#                 break
        
#         return False

#     return backtrack(0)

# def can_partition_k_subsets_memo(nums, k):
#     total_sum = sum(nums)
    
#     if total_sum % k != 0:
#         return False

#     target = total_sum // k
#     nums.sort(reverse=True)
#     n = len(nums)
#     subsets = [0] * k 

#     @memoize
#     def backtrack(index):
#         if index == n:
#             return all(subset == target for subset in subsets)
        
#         for i in range(k):
#             if subsets[i] + nums[index] <= target:
#                 subsets[i] += nums[index] 
#                 if backtrack(index + 1):
#                     return True
#                 subsets[i] -= nums[index]
            
#             if subsets[i] == 0:
#                 break
#         return False

#     return backtrack(0)
# def test_can_partition_k_subsets():
#     nums = [4, 3, 2, 3, 5, 2, 1]
#     k = 4
#     print("Can Partition K Subsets:", can_partition_k_subsets(nums, k))



# # 9. All Possible Full Binary Trees
# class TreeNode:
#     def __init__(self, val=0):
#         self.val = val
#         self.left = None
#         self.right = None

# def all_possible_fbt(N):
#     if N % 2 == 0:
#         return []
#     if N == 1:
#         return [TreeNode(0)]
#     result = []
#     for left_nodes in range(1, N, 2):
#         right_nodes = N - 1 - left_nodes
#         left_trees = all_possible_fbt_memo(left_nodes)
#         right_trees = all_possible_fbt_memo(right_nodes)
#         for left in left_trees:
#             for right in right_trees:
#                 node = TreeNode(0)
#                 node.left = left
#                 node.right = right
#                 result.append(node)
#     return result

# all_possible_fbt_memo = memoize(all_possible_fbt)
# #test
# def test_all_possible_fbt():
#     N = 7
#     trees = all_possible_fbt(N)
#     print("Number of Full Binary Trees without memoization:", len(trees))
#     memo_trees = all_possible_fbt_memo(N)
#     print("Number of Full Binary Trees with memoization:", len(memo_trees))

# 1. 
def fibonacci(n):
    if n == 0:
        return 0
    if n == 1 or n == 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

def fibonacci_memo(n, cache=None):
    if cache is None:
        cache = {}
    if n in cache:
        return cache[n]
    if n == 0:
        cache[0] = 0
        return 0
    if n == 1 or n == 2:
        cache[n] = 1
        return 1
    cache[n] = fibonacci_memo(n - 1, cache) + fibonacci_memo(n - 2, cache)
    return cache[n]

# 2. 
def knapsack(W, weights, values, n):
    if n == 0 or W == 0:
        return 0
    if weights[n - 1] > W:
        return knapsack(W, weights, values, n - 1)
    else:
        include_item = values[n - 1] + knapsack(W - weights[n - 1], weights, values, n - 1)
        exclude_item = knapsack(W, weights, values, n - 1)
        return max(include_item, exclude_item)

def knapsack_memo(W, weights, values, n, cache=None):
    if cache is None:
        cache = {}
    key = (W, n)
    if key in cache:
        return cache[key]
    if n == 0 or W == 0:
        cache[key] = 0
        return 0
    if weights[n - 1] > W:
        result = knapsack_memo(W, weights, values, n - 1, cache)
    else:
        include_item = values[n - 1] + knapsack_memo(W - weights[n - 1], weights, values, n - 1, cache)
        exclude_item = knapsack_memo(W, weights, values, n - 1, cache)
        result = max(include_item, exclude_item)
    cache[key] = result
    return result


# 3. 
def coin_change(coins, amount):
    if amount == 0:
        return 0
    if amount < 0:
        return -1
    min_coins = float('inf')
    for coin in coins:
        result = coin_change(coins, amount - coin)
        if result != -1:
            min_coins = min(min_coins, result + 1)
    return min_coins if min_coins != float('inf') else -1

def coin_change_memo(coins, amount, cache=None):
    if cache is None:
        cache = {}
    if amount in cache:
        return cache[amount]
    if amount == 0:
        cache[amount] = 0
        return 0
    if amount < 0:
        return -1
    min_coins = float('inf')
    for coin in coins:
        result = coin_change_memo(coins, amount - coin, cache)
        if result != -1:
            min_coins = min(min_coins, result + 1)
    cache[amount] = min_coins if min_coins != float('inf') else -1
    return cache[amount]

# 4.
def levenshtein_distance(s1, s2):
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)
    if s1[-1] == s2[-1]:
        return levenshtein_distance(s1[:-1], s2[:-1])
    return 1 + min(
        levenshtein_distance(s1, s2[:-1]),    
        levenshtein_distance(s1[:-1], s2),   
        levenshtein_distance(s1[:-1], s2[:-1]) 
    )

def levenshtein_distance_memo(s1, s2):
    cache = {}
    def helper(i, j):
        if (i, j) in cache:
            return cache[(i, j)]
        if i == 0:
            cache[(i, j)] = j
            return j
        if j == 0:
            cache[(i, j)] = i
            return i
        if s1[i - 1] == s2[j - 1]:
            cache[(i, j)] = helper(i - 1, j - 1)
        else:
            cache[(i, j)] = 1 + min(
                helper(i, j - 1),    
                helper(i - 1, j),    
                helper(i - 1, j - 1) 
            )
        return cache[(i, j)]
    return helper(len(s1), len(s2))


# 5.
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def factorial_memo(n, cache={}):
    if n in cache:
        return cache[n]
    if n == 0:
        cache[0] = 1
        return 1
    cache[n] = n * factorial_memo(n - 1, cache)
    return cache[n]


# 6. 
def matrix_chain_order(i, j, dimensions):
    if i == j:
        return 0
    min_count = float('inf')
    for k in range(i, j):
        count = (
            matrix_chain_order(i, k, dimensions)
            + matrix_chain_order(k + 1, j, dimensions)
            + dimensions[i - 1] * dimensions[k] * dimensions[j]
        )
        if count < min_count:
            min_count = count
    return min_count

def matrix_chain_order_memo(i, j, dimensions, cache={}):
    key = (i, j)
    if key in cache:
        return cache[key]
    if i == j:
        cache[key] = 0
        return 0
    min_count = float('inf')
    for k in range(i, j):
        count = (
            matrix_chain_order_memo(i, k, dimensions, cache)
            + matrix_chain_order_memo(k + 1, j, dimensions, cache)
            + dimensions[i - 1] * dimensions[k] * dimensions[j]
        )
        if count < min_count:
            min_count = count
    cache[key] = min_count
    return min_count


# 7. 
def can_i_win(max_int, desired_total):
    if desired_total <= 0:
        return True
    def can_win(used, total):
        for i in range(max_int):
            curr = 1 << i
            if not used & curr:
                if total + i + 1 >= desired_total:
                    return True
                if not can_win(used | curr, total + i + 1):
                    return True
        return False
    return can_win(0, 0)

def can_i_win_memo(max_int, desired_total):
    if desired_total <= 0:
        return True
    memo = {}
    def can_win(used, total):
        if used in memo:
            return memo[used]
        for i in range(max_int):
            curr = 1 << i
            if not used & curr:
                if total + i + 1 >= desired_total:
                    memo[used] = True
                    return True
                if not can_win(used | curr, total + i + 1):
                    memo[used] = True
                    return True
        memo[used] = False
        return False
    return can_win(0, 0)

# 8. 
def can_partition_k_subsets(nums, k):
    total_sum = sum(nums)
    if total_sum % k != 0:
        return False
    target = total_sum // k
    nums.sort(reverse=True)
    subsets = [0] * k
    def backtrack(index):
        if index == len(nums):
            return all(subset == target for subset in subsets)
        for i in range(k):
            if subsets[i] + nums[index] <= target:
                subsets[i] += nums[index]
                if backtrack(index + 1):
                    return True
                subsets[i] -= nums[index]
            if subsets[i] == 0:
                break
        return False
    return backtrack(0)

def can_partition_k_subsets_memo(nums, k):
    total_sum = sum(nums)
    if total_sum % k != 0:
        return False
    target = total_sum // k
    nums.sort(reverse=True)
    n = len(nums)
    memo = {}
    def backtrack(index, used, current_sum, k_remaining):
        if k_remaining == 1:
            return True
        if current_sum == target:
            result = backtrack(0, used, 0, k_remaining - 1)
            memo[(used, k_remaining)] = result
            return result
        if (used, k_remaining) in memo:
            return memo[(used, k_remaining)]
        for i in range(index, n):
            if not used & (1 << i):
                if current_sum + nums[i] <= target:
                    if backtrack(i + 1, used | (1 << i), current_sum + nums[i], k_remaining):
                        memo[(used, k_remaining)] = True
                        return True
        memo[(used, k_remaining)] = False
        return False
    return backtrack(0, 0, 0, k)

# 9. 
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

def all_possible_fbt(N):
    if N % 2 == 0:
        return []
    if N == 1:
        return [TreeNode(0)]
    result = []
    for left_nodes in range(1, N, 2):
        right_nodes = N - 1 - left_nodes
        left_trees = all_possible_fbt(left_nodes)
        right_trees = all_possible_fbt(right_nodes)
        for left in left_trees:
            for right in right_trees:
                node = TreeNode(0)
                node.left = left
                node.right = right
                result.append(node)
    return result

def all_possible_fbt_memo(N, cache={}):
    if N in cache:
        return cache[N]
    if N % 2 == 0:
        return []
    if N == 1:
        cache[1] = [TreeNode(0)]
        return cache[1]
    result = []
    for left_nodes in range(1, N, 2):
        right_nodes = N - 1 - left_nodes
        left_trees = all_possible_fbt_memo(left_nodes, cache)
        right_trees = all_possible_fbt_memo(right_nodes, cache)
        for left in left_trees:
            for right in right_trees:
                node = TreeNode(0)
                node.left = left
                node.right = right
                result.append(node)
    cache[N] = result
    return result


