"""
Strongly Connected Components (SCC) using Tarjan's algorithm.

Easy explanation:
- In a directed graph, nodes in the same SCC can reach each other.
- Tarjan's algorithm performs one DFS and tracks discovery order and a "low-link" value.
- When we close a DFS root whose index == low-link, we pop a whole SCC from the stack.

Time complexity: O(V + E) — single DFS over the graph.
Space complexity: O(V) — stacks and arrays for indices/low-links.
"""
from __future__ import annotations
from typing import Dict, List

Graph = Dict[int, List[int]]


def tarjan_scc(graph: Graph) -> List[List[int]]:
    n = len(graph)
    index = 0
    indices = {v: -1 for v in graph}
    low = {v: 0 for v in graph}
    on_stack = {v: False for v in graph}
    stack: List[int] = []
    result: List[List[int]] = []

    def strongconnect(v: int) -> None:
        nonlocal index
        indices[v] = index
        low[v] = index
        index += 1
        stack.append(v)
        on_stack[v] = True

        for w in graph[v]:
            if indices[w] == -1:
                strongconnect(w)
                low[v] = min(low[v], low[w])
            elif on_stack[w]:
                low[v] = min(low[v], indices[w])

        # If v is a root node, pop the stack and generate an SCC
        if low[v] == indices[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                scc.append(w)
                if w == v:
                    break
            result.append(scc)

    for v in graph:
        if indices[v] == -1:
            strongconnect(v)

    return result


def demo() -> None:
    graph: Graph = {
        0: [1],
        1: [2, 3],
        2: [0],  # 0->1->2->0 forms an SCC
        3: [4],
        4: [5],
        5: [3],  # 3->4->5->3 forms another SCC
        6: []     # single node SCC
    }
    print("Graph adjacency:")
    for v in graph:
        print(f"  {v}: {graph[v]}")
    comps = tarjan_scc(graph)
    print("\nStrongly Connected Components:")
    for i, comp in enumerate(comps, 1):
        print(f"  SCC {i}: {sorted(comp)}")


if __name__ == "__main__":
    demo()