import heapq
from collections import deque
import time

def bfs(maze, start, end):
    """
    Breadth-First Search Algorithm.
    Explores nodes level by level, ensuring the shortest path in an unweighted grid.
    Returns: (path, nodes_expanded, time_taken)
    """
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start, [start])])
    visited = set()
    visited.add(start)
    nodes_expanded = 0
    start_time = time.perf_counter()

    while queue:
        (x, y), path = queue.popleft()
        nodes_expanded += 1
        if (x, y) == end:
            return path, nodes_expanded, time.perf_counter() - start_time  # Solution found

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))

    return None, nodes_expanded, time.perf_counter() - start_time  # No solution found


def dfs(maze, start, end):
    """
    Depth-First Search Algorithm.
    Explores paths deeply before backtracking.
    Returns: (path, nodes_expanded, time_taken)
    """
    rows, cols = len(maze), len(maze[0])
    stack = [(start, [start])]
    visited = set()
    visited.add(start)
    nodes_expanded = 0
    start_time = time.perf_counter()

    while stack:
        (x, y), path = stack.pop()
        nodes_expanded += 1
        if (x, y) == end:
            return path, nodes_expanded, time.perf_counter() - start_time  # Solution found

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and (nx, ny) not in visited:
                stack.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))

    return None, nodes_expanded, time.perf_counter() - start_time  # No solution found


def heuristic(a, b):
    """
    Heuristic function for A* (Manhattan distance).
    Used to estimate the cost from current node to goal.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(maze, start, end):
    """
    A* Search Algorithm.
    Uses a priority queue (min-heap) to expand the most promising node based on cost.
    Returns: (path, nodes_expanded, time_taken)
    """
    rows, cols = len(maze), len(maze[0])
    pq = [(0, start, [start])]  # (cost, position, path)
    visited = set()
    nodes_expanded = 0
    start_time = time.perf_counter()

    while pq:
        cost, (x, y), path = heapq.heappop(pq)
        nodes_expanded += 1
        if (x, y) == end:
            return path, nodes_expanded, time.perf_counter() - start_time  # Solution found

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and (nx, ny) not in visited:
                new_cost = cost + 1 + heuristic((nx, ny), end)
                heapq.heappush(pq, (new_cost, (nx, ny), path + [(nx, ny)]))

    return None, nodes_expanded, time.perf_counter() - start_time  # No solution found


def compare_algorithms(maze, start, end):
    """
    Runs all three algorithms on the same maze and prints comparison results.
    """
    print("\n=== Algorithm Comparison ===")
    print(f"Maze Size: {len(maze)}x{len(maze[0])}")
    print(f"Start: {start}, End: {end}\n")
    
    # Run all algorithms
    bfs_path, bfs_nodes, bfs_time = bfs(maze, start, end)
    dfs_path, dfs_nodes, dfs_time = dfs(maze, start, end)
    astar_path, astar_nodes, astar_time = a_star(maze, start, end)
    
    # Print comparison table
    print(f"{'Algorithm':<10}{'Path Length':<15}{'Nodes Expanded':<15}{'Time (ms)':<10}")
    print("-" * 50)
    print(f"{'BFS':<10}{len(bfs_path) if bfs_path else 'N/A':<15}{bfs_nodes:<15}{bfs_time*1000:.2f}")
    print(f"{'DFS':<10}{len(dfs_path) if dfs_path else 'N/A':<15}{dfs_nodes:<15}{dfs_time*1000:.2f}")
    print(f"{'A*':<10}{len(astar_path) if astar_path else 'N/A':<15}{astar_nodes:<15}{astar_time*1000:.2f}")

# Example Usage
if __name__ == "__main__":
    sample_maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    start = (0, 0)
    end = (4, 4)

    compare_algorithms(sample_maze, start, end)
