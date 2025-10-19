"""
Segment Tree for range sum queries and point updates.

Easy explanation:
- Think of a tree that stores sums for intervals.
- Leaves store single elements. Parents store sum of their children.
- To query a range, we combine sums from relevant nodes. To update, we change a leaf and update its ancestors.

Time complexity:
- Build: O(n)
- Query: O(log n)
- Update: O(log n)
Space complexity: O(n) — tree array ~ 4n in practice.
"""
from __future__ import annotations
from typing import List


class SegmentTree:
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr: List[int], idx: int, l: int, r: int) -> None:
        if l == r:
            self.tree[idx] = arr[l]
            return
        mid = (l + r) // 2
        self._build(arr, idx * 2, l, mid)
        self._build(arr, idx * 2 + 1, mid + 1, r)
        self.tree[idx] = self.tree[idx * 2] + self.tree[idx * 2 + 1]

    def update(self, pos: int, val: int) -> None:
        def _update(idx: int, l: int, r: int) -> None:
            if l == r:
                self.tree[idx] = val
                return
            mid = (l + r) // 2
            if pos <= mid:
                _update(idx * 2, l, mid)
            else:
                _update(idx * 2 + 1, mid + 1, r)
            self.tree[idx] = self.tree[idx * 2] + self.tree[idx * 2 + 1]
        _update(1, 0, self.n - 1)

    def query(self, ql: int, qr: int) -> int:
        def _query(idx: int, l: int, r: int) -> int:
            if ql <= l and r <= qr:
                return self.tree[idx]
            if r < ql or l > qr:
                return 0
            mid = (l + r) // 2
            return _query(idx * 2, l, mid) + _query(idx * 2 + 1, mid + 1, r)
        return _query(1, 0, self.n - 1)


def demo() -> None:
    arr = [2, 1, 3, 4, 5]
    st = SegmentTree(arr)
    print("Initial array:", arr)
    print("Sum [1..3] =", st.query(1, 3))  # 1+3+4 = 8
    st.update(2, 10)  # arr[2] = 10
    print("After update arr[2]=10, Sum [1..3] =", st.query(1, 3))  # 1+10+4 = 15


if __name__ == "__main__":
    demo()