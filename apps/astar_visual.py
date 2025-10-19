import matplotlib.pyplot as plt
import numpy as np
from heapq import heappush, heappop
import time

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start
        self.h = 0  # Heuristic cost to goal
        self.f = 0  # Total cost

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    # Manhattan Distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_visual(grid, start, end):
    open_list = []
    closed_list = set()

    start_node = Node(start)
    goal_node = Node(end)
    heappush(open_list, start_node)

    fig, ax = plt.subplots()
    grid_display = np.array(grid)
    
    while open_list:
        current_node = heappop(open_list)
        closed_list.add(current_node.position)

        # Visualize current state
        grid_display[current_node.position] = 3  # Visited nodes
        plt.imshow(grid_display, cmap='viridis')
        plt.title("A* Pathfinding Visualization")
        plt.pause(0.2)
        plt.cla()

        # Goal check
        if current_node.position == goal_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent

            # Mark final path
            for p in path:
                grid_display[p] = 2
            plt.imshow(grid_display, cmap='viridis')
            plt.title("✅ Path Found!")
            plt.show()
            return path[::-1]

        # Explore neighbors
        for move in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_pos = (current_node.position[0] + move[0],
                       current_node.position[1] + move[1])

            # Check boundaries and obstacles
            if (0 <= new_pos[0] < len(grid) and
                0 <= new_pos[1] < len(grid[0]) and
                grid[new_pos[0]][new_pos[1]] == 0 and
                new_pos not in closed_list):

                new_node = Node(new_pos, current_node)
                new_node.g = current_node.g + 1
                new_node.h = heuristic(new_node.position, goal_node.position)
                new_node.f = new_node.g + new_node.h

                if any(open_node.position == new_node.position and open_node.f <= new_node.f for open_node in open_list):
                    continue

                heappush(open_list, new_node)

    plt.title("❌ No Path Found")
    plt.show()
    return None


grid = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

start = (0, 0)
end = (4, 5)

print("🧭 Starting A* visualization...")
path = astar_visual(grid, start, end)

if path:
    print("✅ Shortest Path Found:", path)
else:
    print("❌ No path found.")
