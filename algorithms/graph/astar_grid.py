"""
A* shortest path on a grid with Manhattan heuristic and ASCII visualization.

Easy explanation:
- Like Dijkstra, A* finds the cheapest path.
- It uses a smart guess (heuristic) of distance to goal to explore faster.
- Here we use Manhattan distance (|dr| + |dc|) for a 4-direction grid.

Time complexity:
- Depends on heuristic quality. In worst-case (poor heuristic), similar to Dijkstra: O(E log V).
- With a good admissible heuristic, often explores much less.
Space complexity:
- O(V) for distances/visited/parents.
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


def manhattan(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid: Grid, start: Point, goal: Point) -> Tuple[Optional[int], List[Point]]:
    R, C = len(grid), len(grid[0])
    g = [[float('inf')] * C for _ in range(R)]  # cost so far
    prev: List[List[Optional[Point]]] = [[None] * C for _ in range(R)]
    pq: List[Tuple[float, Point]] = []
    sr, sc = start
    gr, gc = goal

    g[sr][sc] = 0
    heapq.heappush(pq, (manhattan(start, goal), start))

    while pq:
        f, (r, c) = heapq.heappop(pq)
        if (r, c) == (gr, gc):
            break
        if f - manhattan((r, c), goal) != g[r][c]:
            # outdated entry in pq
            continue
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if not in_bounds(grid, nr, nc) or not is_open(grid, nr, nc):
                continue
            ng = g[r][c] + 1
            if ng < g[nr][nc]:
                g[nr][nc] = ng
                prev[nr][nc] = (r, c)
                nf = ng + manhattan((nr, nc), goal)
                heapq.heappush(pq, (nf, (nr, nc)))

    if g[gr][gc] == float('inf'):
        return None, []

    # reconstruct path
    path: List[Point] = []
    cur: Optional[Point] = goal
    while cur is not None:
        path.append(cur)
        cr, cc = cur
        cur = prev[cr][cc]
    path.reverse()
    return g[gr][gc], path


def draw_grid_with_path(grid: Grid, path: List[Point]) -> None:
    s = set(path)
    for r in range(len(grid)):
        row = []
        for c in range(len(grid[0])):
            ch = grid[r][c]
            row.append('*' if (r, c) in s and ch not in ('S', 'G') else ch)
        print(''.join(row))


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
    dist, path = astar(grid, start, goal)
    print(f"\nShortest distance: {dist}")
    print("Path coordinates:", path)
    print("\nGrid with path (*):")
    draw_grid_with_path(grid, path)


if __name__ == "__main__":
    demo()