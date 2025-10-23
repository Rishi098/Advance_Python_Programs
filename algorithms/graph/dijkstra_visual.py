"""
Dijkstra's shortest path on a grid with simple ASCII visualization.

Easy explanation:
- We have a grid with walls (#) and empty cells (.).
- Start (S) and Goal (G) are cells we want to connect with the cheapest path.
- Moving to a neighbor costs 1.
- Dijkstra explores cells in order of their current best known cost, guaranteeing the shortest path when we reach G.

Time complexity:
- Using a priority queue, it runs in O(E log V). On an R x C grid, V = R*C and E ≈ 4*R*C, so ~ O(R*C log(R*C)).
Space complexity:
- O(V) to store distances and visited states.
"""
from __future__ import annotations
from typing import List, Tuple, Optional
import heapq

Grid = List[List[str]]
Point = Tuple[int, int]

DIRS: List[Point] = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def in_bounds(grid: Grid, r: int, c: int) -> bool:
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def is_open(grid: Grid, r: int, c: int) -> bool:
    return grid[r][c] != '#'


def dijkstra(grid: Grid, start: Point, goal: Point) -> Tuple[Optional[int], List[Point]]:
    R, C = len(grid), len(grid[0])
    dist = [[float('inf')] * C for _ in range(R)]
    prev: List[List[Optional[Point]]] = [[None] * C for _ in range(R)]
    pq: List[Tuple[int, Point]] = []
    sr, sc = start
    gr, gc = goal

    dist[sr][sc] = 0
    heapq.heappush(pq, (0, start))

    while pq:
        d, (r, c) = heapq.heappop(pq)
        if (r, c) == (gr, gc):
            break
        if d != dist[r][c]:
            continue
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if not in_bounds(grid, nr, nc) or not is_open(grid, nr, nc):
                continue
            nd = d + 1  # unit cost
            if nd < dist[nr][nc]:
                dist[nr][nc] = nd
                prev[nr][nc] = (r, c)
                heapq.heappush(pq, (nd, (nr, nc)))

    if dist[gr][gc] == float('inf'):
        return None, []

    # reconstruct path
    path: List[Point] = []
    cur: Optional[Point] = goal
    while cur is not None:
        path.append(cur)
        cr, cc = cur
        cur = prev[cr][cc]
    path.reverse()
    return dist[gr][gc], path


def draw_grid_with_path(grid: Grid, path: List[Point]) -> None:
    s = set(path)
    out: List[str] = []
    for r in range(len(grid)):
        row_chars = []
        for c in range(len(grid[0])):
            ch = grid[r][c]
            if (r, c) in s and ch not in ('S', 'G'):
                row_chars.append('*')
            else:
                row_chars.append(ch)
        out.append(''.join(row_chars))
    print('\n'.join(out))


def demo() -> None:
    grid = [
        list("S..#...."),
        list("..##..G."),
        list("....#..."),
        list("#...#...")
    ]
    start = (0, 0)
    goal = (1, 6)
    print("Grid (S=start, G=goal, #=wall):")
    print('\n'.join(''.join(row) for row in grid))
    dist, path = dijkstra(grid, start, goal)
    print(f"\nShortest distance: {dist}")
    print("Path coordinates:", path)
    print("\nGrid with path (*):")
    draw_grid_with_path(grid, path)


if __name__ == "__main__":
    demo()