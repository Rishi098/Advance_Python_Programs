"""
Union-Find (Disjoint Set Union, DSU) with path compression and union by size.

Easy explanation:
- Keeps track of groups (sets) of elements.
- find(x) returns the representative (root) of x's set.
- union(a, b) merges the sets of a and b.
- Path compression: flatten the tree during find for speed.
- Union by size: attach smaller tree under larger one.

Time complexity:
- Amortized ~ O(alpha(n)) per operation, where alpha is inverse Ackermann (very slow-growing, practically constant).
Space complexity:
- O(n) for parent and size arrays.
"""
from __future__ import annotations
from typing import List


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.sets = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        # union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.sets -= 1
        return True

    def same(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)


def demo() -> None:
    uf = UnionFind(7)
    edges = [(0, 1), (1, 2), (3, 4), (5, 6), (2, 3)]
    print("Union operations:", edges)
    for a, b in edges:
        uf.union(a, b)
    print("Groups remaining:", uf.sets)
    print("0 and 4 connected?", uf.same(0, 4))
    print("5 and 6 connected?", uf.same(5, 6))


if __name__ == "__main__":
    demo()