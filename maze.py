import random

def generate_maze(rows, cols, difficulty='medium'):
    """
    Generates a random maze with guaranteed path from start to end.
    0 -> Open path
    1 -> Wall
    The start position is (0,0) and the end position is (rows-1, cols-1).
    Difficulty options: 'easy', 'medium', 'hard'
    """
    wall_prob = {
        'easy': 0.2,
        'medium': 0.3,
        'hard': 0.4
    }.get(difficulty, 0.3)
    
    # Generate maze with guaranteed path
    while True:
        maze = [[0 if random.random() > wall_prob else 1 for _ in range(cols)] for _ in range(rows)]
        maze[0][0] = 0  # Ensure start is open
        maze[rows-1][cols-1] = 0  # Ensure end is open
        
        # Check if there's a path from start to end
        if is_solvable(maze, (0,0), (rows-1, cols-1)):
            return maze

def is_solvable(maze, start, end):
    """Check if there's a path from start to end using BFS."""
    rows, cols = len(maze), len(maze[0])
    queue = [start]
    visited = set([start])
    
    while queue:
        x, y = queue.pop(0)
        if (x, y) == end:
            return True
            
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < rows and 0 <= ny < cols and 
                maze[nx][ny] == 0 and (nx, ny) not in visited):
                visited.add((nx, ny))
                queue.append((nx, ny))
    return False

def print_maze(maze):
    """
    Prints the maze in a readable format.
    """
    for row in maze:
        print("".join(["█" if cell == 1 else " " for cell in row]))

# Example Usage
if __name__ == "__main__":
    rows, cols = 10, 10
    maze = generate_maze(rows, cols)
    print_maze(maze)
