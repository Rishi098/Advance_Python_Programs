# Tarjan’s Algorithm in Python
# ------------------------------------------------------
# Author: Jatin Vishwakarma
# Description: Implementation of Tarjan’s Algorithm for finding
# Strongly Connected Components (SCCs) in a directed graph.
# This algorithm uses DFS and low-link values to efficiently
# detect all SCCs in O(V + E) time complexity.

from collections import defaultdict

class TarjanSCC:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
        self.time = 0
        self.disc = [-1] * vertices
        self.low = [-1] * vertices
        self.stack_member = [False] * vertices
        self.stack = []

    def add_edge(self, u, v):
        self.graph[u].append(v)
      
    def SCC_util(self, u):
        self.disc[u] = self.low[u] = self.time
        self.time += 1
        self.stack.append(u)
        self.stack_member[u] = True

        for v in self.graph[u]:
            if self.disc[v] == -1:
                self.SCC_util(v)
                self.low[u] = min(self.low[u], self.low[v])
            elif self.stack_member[v]:
                self.low[u] = min(self.low[u], self.disc[v])


        if self.low[u] == self.disc[u]:
            print("SCC:", end=" ")
            while True:
                v = self.stack.pop()
                self.stack_member[v] = False
                print(v, end=" ")
                if v == u:
                    break
            print()


    def find_SCCs(self):
        for i in range(self.V):
            if self.disc[i] == -1:
                self.SCC_util(i)


if __name__ == "__main__":
    g = TarjanSCC(7)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(1, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 3)
    g.add_edge(5, 6)

    print("Strongly Connected Components in the given graph:")
    g.find_SCCs()
