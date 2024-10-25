from typing import List

def coinChange(coins: List[int], amount: int) -> int:
        def dfs(memo, n):
            if memo[n]: # it's already calculated, simply return it
                return memo[n]
            if n == 0:
                return 0
            memo[n] = float("inf")
            for coin in coins:
                if n - coin >= 0:
                    memo[n] = min(memo[n], dfs(memo, n-coin)+1)
            return memo[n]
        
        memo = dict(int)
        tmp = dfs(memo, amount)
        return tmp if tmp != float("inf") else -1