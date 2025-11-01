from collections import deque

def bfsOfGraph(n, edges, src):

    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = [False] * n
    queue = deque([src])
    visited[src] = True
    lis = []

    while queue:
        node = queue.popleft()
        lis.append(node)

        for nei in adj[node]:
            if not visited[nei]:
                visited[nei] = True
                queue.append(nei)

    return lis
