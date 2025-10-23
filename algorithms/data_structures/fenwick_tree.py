"""
Fenwick Tree (Binary Indexed Tree) for efficient prefix sums and point updates.

Easy explanation:
- Stores partial sums in a clever way using least significant bit (LSB).
- Prefix sum (0..i) and point updates work in O(log n) by jumping through indices using LSB.

Time complexity:
- Update: O(log n)
- Prefix sum: O(log n)
- Range sum [l..r]: prefix(r) - prefix(l-1)
Space complexity: O(n)
"""
from __future__ import annotations
from typing import List


class FenwickTree:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)  # 1-indexed

    def add(self, idx: int, delta: int) -> None:
        idx += 1  # shift to 1-indexed
        while idx <= self.n:
            self.bit[idx] += delta
            idx += idx & -idx

    def prefix_sum(self, idx: int) -> int:
        idx += 1
        s = 0
        while idx > 0:
            s += self.bit[idx]
            idx -= idx & -idx
        return s

    def range_sum(self, l: int, r: int) -> int:
        return self.prefix_sum(r) - (self.prefix_sum(l - 1) if l > 0 else 0)


def demo() -> None:
    arr = [2, 1, 3, 4, 5]
    ft = FenwickTree(len(arr))
    for i, v in enumerate(arr):
        ft.add(i, v)
    print("Initial array:", arr)
    print("Prefix sum up to 3:", ft.prefix_sum(3))  # 2+1+3+4 = 10
    print("Range sum [1..3]:", ft.range_sum(1, 3))  # 1+3+4 = 8
    ft.add(2, 7)  # arr[2] += 7 (3 -> 10)
    print("After add +7 at index 2, Range sum [1..3]:", ft.range_sum(1, 3))  # 1+10+4 = 15


if __name__ == "__main__":
    demo()