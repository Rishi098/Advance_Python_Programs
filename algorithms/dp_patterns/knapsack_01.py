"""
0/1 Knapsack — maximize value with weight limit.

Easy explanation:
- You have items with (weight, value). Each item can be taken once (0/1).
- Goal: maximize value without exceeding capacity.
- DP builds a table: dp[i][w] = best value using first i items with capacity w.

Time complexity: O(n * W) where n = items, W = capacity.
Space complexity: O(n * W) for table (can be optimized to O(W)).
"""
from __future__ import annotations
from typing import List, Tuple


def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w_i, v_i = weights[i - 1], values[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if w_i <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - w_i] + v_i)
    return dp[n][capacity]


def demo() -> None:
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 8]
    capacity = 5
    print("Items (w,v):", list(zip(weights, values)))
    print("Capacity:", capacity)
    print("Max value:", knapsack(weights, values, capacity))  # Expected 8 (item weight 5)


if __name__ == "__main__":
    demo()