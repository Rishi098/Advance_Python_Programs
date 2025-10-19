import unittest

from algorithms.dp_patterns.knapsack_01 import knapsack
from algorithms.dp_patterns.longest_common_subsequence import lcs
from algorithms.dp_patterns.coin_change_min_coins import min_coins


class TestDPPatterns(unittest.TestCase):
    def test_knapsack_small(self):
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 8]
        capacity = 5
        self.assertEqual(knapsack(weights, values, capacity), 8)

    def test_lcs_basic(self):
        self.assertEqual(lcs("ABCBDAB", "BDCABC"), 4)
        self.assertEqual(lcs("abc", "abc"), 3)
        self.assertEqual(lcs("abc", "def"), 0)

    def test_min_coins(self):
        coins = [1, 3, 4]
        self.assertEqual(min_coins(coins, 6), 2)  # 3+3
        self.assertEqual(min_coins(coins, 7), 2)  # 3+4
        self.assertEqual(min_coins(coins, 2), 2)  # 1+1
        self.assertEqual(min_coins(coins, 0), 0)


if __name__ == "__main__":
    unittest.main()