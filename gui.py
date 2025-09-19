import tkinter as tk
from tkinter import ttk, messagebox
from maze import generate_maze
from search_algorithms import bfs, dfs, a_star, compare_algorithms
import time

class MazeSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")
        self.root.configure(bg="#f5f5f5")
        self.edit_mode = False
        
        # Configure styles
        self.style = ttk.Style()
        
        # Modern color scheme
        self.style.theme_use("clam")
        self.style.configure(".", 
                           background="#f5f5f5",
                           foreground="#333333",
                           font=('Segoe UI', 9))
        
        # Button styles
        self.style.configure("TButton", 
                           padding=8, 
                           relief="flat",
                           font=('Segoe UI', 9, 'bold'))
        self.style.map("TButton",
                      background=[('active', '#e0e0e0')])
        
        # Accent buttons
        self.style.configure("Primary.TButton", 
                           background="#4285F4", 
                           foreground="white")
        self.style.configure("Success.TButton", 
                           background="#34A853", 
                           foreground="white")
        self.style.configure("Danger.TButton", 
                           background="#EA4335", 
                           foreground="white")
        
        # Entry/Combobox styles
        self.style.configure("TCombobox",
                           fieldbackground="white",
                           padding=5)
        
        # Stats panel style
        self.style.configure("Stats.TFrame",
                           background="white",
                           relief="solid",
                           borderwidth=1)
        
        # Maze settings
        self.rows, self.cols = 15, 15
        self.cell_size = 30
        self.difficulty = "medium"
        self.maze = generate_maze(self.rows, self.cols, self.difficulty)
        
        # UI Elements
        self.create_widgets()
        self.draw_maze()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main frame with improved spacing
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        ttk.Label(title_frame, 
                text="Maze Solver", 
                font=('Segoe UI', 16, 'bold'),
                foreground="#4285F4").pack()
        
        # Maze canvas with shadow effect
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.grid(row=1, column=0, padx=(0, 15), sticky="nsew")
        
        # Shadow effect
        shadow = ttk.Frame(canvas_frame, style="Stats.TFrame")
        shadow.pack(padx=3, pady=3)
        
        self.canvas = tk.Canvas(shadow, 
                              width=self.cols * self.cell_size, 
                              height=self.rows * self.cell_size,
                              bg="white", highlightthickness=0)
        self.canvas.bind("<Button-1>", self.handle_cell_click)
        self.canvas.pack()
        
        # Control panel with card styling
        control_frame = ttk.Frame(main_frame, style="Stats.TFrame", padding=10)
        control_frame.grid(row=1, column=1, sticky="nsew")
        
        # Algorithm and difficulty selection
        ttk.Label(control_frame, 
                 text="Algorithm:").grid(row=0, column=0, sticky="w", padx=(0,5))
        self.algorithm_var = tk.StringVar(value="BFS")
        self.algorithm_menu = ttk.Combobox(control_frame,
                                         textvariable=self.algorithm_var,
                                         values=["BFS", "DFS", "A*"],
                                         state="readonly",
                                         width=8)
        self.algorithm_menu.grid(row=0, column=1, padx=(0,10))

        ttk.Label(control_frame,
                 text="Difficulty:").grid(row=0, column=2, sticky="w", padx=(0,5))
        self.difficulty_var = tk.StringVar(value="Medium")
        self.difficulty_menu = ttk.Combobox(control_frame,
                                          textvariable=self.difficulty_var,
                                          values=["Easy", "Medium", "Hard"],
                                          state="readonly",
                                          width=8)
        self.difficulty_menu.grid(row=0, column=3, padx=(0,10))

        # Buttons with improved styling
        ttk.Button(control_frame, 
                  text="Solve", 
                  command=self.solve_maze,
                  style="Primary.TButton").grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(control_frame,
                  text="New Maze",
                  command=self.regenerate_maze,
                  style="Success.TButton").grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(control_frame,
                  text="Compare All",
                  command=self.compare_algorithms,
                  style="Primary.TButton").grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(control_frame,
                  text="Edit Mode",
                  command=self.toggle_edit_mode,
                  name="edit_btn",
                  style="Danger.TButton").grid(row=0, column=7, padx=5, pady=5)
        
        # Stats panel with card styling
        stats_frame = ttk.Frame(main_frame, style="Stats.TFrame", padding=10)
        stats_frame.grid(row=2, column=0, columnspan=2, pady=(15, 0), sticky="ew")
        
        self.stats_text = tk.Text(stats_frame, 
                                height=6, 
                                width=50, 
                                state="disabled",
                                font=('Segoe UI', 9),
                                padx=5, pady=5)
        self.stats_text.pack(fill="both", expand=True)

    def toggle_edit_mode(self):
        """Toggles edit mode for adding/removing walls."""
        self.edit_mode = not self.edit_mode
        btn = self.root.nametowidget("edit_btn")
        if self.edit_mode:
            btn.config(style="Danger.TButton")
            self.update_stats("✏️ EDIT MODE ACTIVE\nClick cells to add/remove walls")
            self.canvas.config(cursor="hand2")
        else:
            btn.config(style="TButton")
            self.update_stats("Edit mode inactive")
            self.canvas.config(cursor="")

    def handle_cell_click(self, event):
        """Handles cell clicks when in edit mode."""
        if not self.edit_mode:
            return
            
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        # Don't allow editing start/end points
        if (row, col) in [(0, 0), (self.rows-1, self.cols-1)]:
            return
            
        # Toggle wall/path
        self.maze[row][col] = 1 - self.maze[row][col]
        self.draw_maze()

    def draw_maze(self):
        """Draws the maze grid with improved visuals."""
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                
                if self.maze[r][c] == 1:  # Wall
                    self.canvas.create_rectangle(x1, y1, x2, y2, 
                                               fill="#333333", 
                                               outline="#555555",
                                               width=2)
                else:  # Path
        
                    self.canvas.create_rectangle(x1, y1, x2, y2, 
                                               fill="#f8f8f8", 
                                               outline="#dddddd",
                                               width=2)
        
        # Draw start and end points
        self.canvas.create_rectangle(0, 0, self.cell_size, self.cell_size, 
                                   fill="#4CAF50", outline="#388E3C")  # Start (green)
        self.canvas.create_rectangle((self.cols-1)*self.cell_size, (self.rows-1)*self.cell_size, 
                                   self.cols*self.cell_size, self.rows*self.cell_size,
                                   fill="#F44336", outline="#D32F2F")  # End (red)

    def solve_maze(self):
        """Solves the maze with animation and stats."""
        start, end = (0, 0), (self.rows - 1, self.cols - 1)
        algorithm = self.algorithm_var.get()
        self.difficulty = self.difficulty_var.get().lower()
        
        # Clear previous solution
        self.draw_maze()
        self.update_stats("Solving maze...")
        
        # Solve with selected algorithm
        if algorithm == "BFS":
            path, nodes, time_taken = bfs(self.maze, start, end)
        elif algorithm == "DFS":
            path, nodes, time_taken = dfs(self.maze, start, end)
        else:  # A*
            path, nodes, time_taken = a_star(self.maze, start, end)
        
        # Display results
        if path:
            self.animate_solution(path)
            stats = (f"Algorithm: {algorithm}\n"
                    f"Path Length: {len(path)}\n"
                    f"Nodes Expanded: {nodes}\n"
                    f"Time Taken: {time_taken*1000:.2f} ms\n"
                    f"Difficulty: {self.difficulty.capitalize()}")
            self.update_stats(stats)
        else:
            messagebox.showwarning("No Solution", "No path found!")
            self.update_stats("No solution found!")

    def animate_solution(self, path, color="#2196F3"):
        """Animates the solution path with customizable color."""
        for i, (r, c) in enumerate(path):
            x1, y1 = c * self.cell_size, r * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            
            # Skip coloring start and end points
            if (r, c) not in [(0, 0), (self.rows-1, self.cols-1)]:
                self.canvas.create_rectangle(x1, y1, x2, y2, 
                                           fill=color, outline=color)
                
            # Update display every 10 steps for performance
            if i % 10 == 0:
                self.root.update()
                time.sleep(0.01)
        
        self.root.update()

    def update_stats(self, text):
        """Updates the statistics display."""
        self.stats_text.config(state="normal")
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, text)
        self.stats_text.config(state="disabled")

    def regenerate_maze(self):
        """Generates a new random maze with selected difficulty."""
        self.difficulty = self.difficulty_var.get().lower()
        self.maze = generate_maze(self.rows, self.cols, self.difficulty)
        self.draw_maze()
        self.update_stats("New maze generated!")

    def compare_algorithms(self):
        """Compares all three algorithms and displays results in the GUI."""
        start, end = (0, 0), (self.rows - 1, self.cols - 1)
        self.draw_maze()
        self.update_stats("Running comparison...")
        self.root.update()
        
        # Run all algorithms
        bfs_path, bfs_nodes, bfs_time = bfs(self.maze, start, end)
        dfs_path, dfs_nodes, dfs_time = dfs(self.maze, start, end)
        astar_path, astar_nodes, astar_time = a_star(self.maze, start, end)
        
        # Format comparison results with visual indicators
        max_nodes = max(bfs_nodes, dfs_nodes, astar_nodes)
        max_time = max(bfs_time, dfs_time, astar_time)
        
        def get_bar(value, max_value, width=20):
            filled = int((value / max_value) * width) if max_value > 0 else 0
            return '█' * filled + ' ' * (width - filled)
        
        results = (
            
            
            "Nodes Expanded:\n"
            f"BFS: {bfs_nodes:<6} {get_bar(bfs_nodes, max_nodes)}\n"
            f"DFS: {dfs_nodes:<6} {get_bar(dfs_nodes, max_nodes)}\n"
            f"A*:  {astar_nodes:<6} {get_bar(astar_nodes, max_nodes)}\n\n"
            
            "Time Taken (ms):\n"
            f"BFS: {bfs_time*1000:.2f} {get_bar(bfs_time, max_time)}\n"
            f"DFS: {dfs_time*1000:.2f} {get_bar(dfs_time, max_time)}\n"
            f"A*:  {astar_time*1000:.2f} {get_bar(astar_time, max_time)}\n\n"
            
            
        )
        
        # Show best path from each algorithm
        if bfs_path:
            self.animate_solution(bfs_path, color="#4CAF50")  # Green for BFS
            time.sleep(0.5)
        if dfs_path:
            self.animate_solution(dfs_path, color="#FFC107")  # Amber for DFS
            time.sleep(0.5)
        if astar_path:
            self.animate_solution(astar_path, color="#2196F3")  # Blue for A*
            
        self.update_stats(results)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.style = ttk.Style()
    root.style.theme_use("clam")
    app = MazeSolverGUI(root)
    root.mainloop()
