"""
Longest Common Subsequence (LCS)

Easy explanation:
- Given two strings, find the longest sequence of characters appearing in both in the same order (not necessarily contiguous).
- DP: dp[i][j] = LCS length for s1[:i] and s2[:j]. If s1[i-1] == s2[j-1], take 1 + dp[i-1][j-1], else max of dp[i-1][j], dp[i][j-1].

Time complexity: O(n * m)
Space complexity: O(n * m) (can be reduced to O(min(n, m))).
"""
from __future__ import annotations
from typing import List


def lcs(a: str, b: str) -> int:
    n, m = len(a), len(b)
    dp: List[List[int]] = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]


def demo() -> None:
    a = "ABCBDAB"
    b = "BDCABC"
    print("Strings:", a, "and", b)
    print("LCS length:", lcs(a, b))  # Expected 4


if __name__ == "__main__":
    demo()