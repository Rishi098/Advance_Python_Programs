"""
Coin Change — minimum coins to make an amount.

Easy explanation:
- Given coin denominations, find the least number of coins to make a target amount.
- DP: dp[x] = fewest coins to make x. For each coin, dp[x] = min(dp[x], dp[x-coin] + 1).

Time complexity: O(n * amount) where n = number of coins.
Space complexity: O(amount).
"""
from __future__ import annotations
from typing import List


def min_coins(coins: List[int], amount: int) -> int:
    INF = 10**9
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] < INF else -1


def demo() -> None:
    coins = [1, 3, 4]
    amount = 6
    print("Coins:", coins, "Amount:", amount)
    print("Min coins:", min_coins(coins, amount))  # Expected 2 (3+3 or 2+4 if 2 exists)


if __name__ == "__main__":
    demo()