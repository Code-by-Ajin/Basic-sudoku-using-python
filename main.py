import tkinter as tk
from tkinter import messagebox
import time

class SudokuSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("450x550")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.cells = {}
        self.delay = 0.02  # Speed of the visualization (seconds)
        
        self.setup_ui()
        self.load_demo_board() # Loads a default puzzle to test immediately

    def setup_ui(self):
        # Header
        header = tk.Label(self.root, text="Recursive Sudoku Solver", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="#00e676")
        header.pack(pady=15)

        # 9x9 Grid Frame
        self.grid_frame = tk.Frame(self.root, bg="#333333", bd=2)
        self.grid_frame.pack(pady=10)

        # Create 9x9 Entry widgets with 3x3 block styling
        for row in range(9):
            for col in range(9):
                # Determine padding to create visual 3x3 boxes
                pady = (3, 0) if row % 3 == 0 and row != 0 else (1, 1)
                padx = (3, 0) if col % 3 == 0 and col != 0 else (1, 1)

                cell = tk.Entry(
                    self.grid_frame, width=3, font=("Arial", 18, "bold"),
                    justify="center", bg="#2b2b2b", fg="#ffffff", 
                    insertbackground="white", bd=1, relief="solid"
                )
                cell.grid(row=row, column=col, padx=padx, pady=pady, ipady=5)
                self.cells[(row, col)] = cell

        # Control Panel
        controls = tk.Frame(self.root, bg="#1e1e1e")
        controls.pack(pady=20)

        tk.Button(controls, text="Solve", font=("Arial", 12, "bold"), bg="#00e676", fg="black", command=self.start_solving, width=10).grid(row=0, column=0, padx=10)
        tk.Button(controls, text="Clear", font=("Arial", 12, "bold"), bg="#ff5252", fg="white", command=self.clear_board, width=10).grid(row=0, column=1, padx=10)
        tk.Button(controls, text="Demo", font=("Arial", 12, "bold"), bg="#4fc3f7", fg="black", command=self.load_demo_board, width=10).grid(row=0, column=2, padx=10)

    def get_board(self):
        """Extracts the current numbers from the Tkinter grid."""
        board = []
        for row in range(9):
            row_data = []
            for col in range(9):
                val = self.cells[(row, col)].get()
                if val.isdigit() and 1 <= int(val) <= 9:
                    row_data.append(int(val))
                    # Lock original numbers visually
                    self.cells[(row, col)].config(fg="#4fc3f7")
                else:
                    row_data.append(0)
                    self.cells[(row, col)].config(fg="#ffffff")
            board.append(row_data)
        return board

    def start_solving(self):
        board = self.get_board()
        if self.solve_sudoku(board):
            messagebox.showinfo("Success", "Sudoku Solved! ⭐⭐⭐⭐⭐")
            # Set all final numbers to solid white
            for row in range(9):
                for col in range(9):
                    self.cells[(row, col)].config(fg="#ffffff")
        else:
            messagebox.showerror("Error", "No solution exists for this board!")

    def solve_sudoku(self, board):
        """The recursive backtracking algorithm."""
        empty = self.find_empty(board)
        if not empty:
            return True  # Puzzle is solved!
        
        row, col = empty

        for num in range(1, 10):
            if self.is_valid(board, num, (row, col)):
                # Trial (Visualized in Green)
                board[row][col] = num
                self.update_gui_cell(row, col, num, "#00e676")
                
                # Recursive Step
                if self.solve_sudoku(board):
                    return True
                
                # Backtrack (Visualized in Red)
                board[row][col] = 0
                self.update_gui_cell(row, col, "", "#ff5252")
                
        return False

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, board, num, pos):
        # Check Row
        for i in range(9):
            if board[pos[0]][i] == num and pos[1] != i:
                return False
        # Check Column
        for i in range(9):
            if board[i][pos[1]] == num and pos[0] != i:
                return False
        # Check 3x3 Box
        box_x, box_y = pos[1] // 3, pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False
        return True

    def update_gui_cell(self, row, col, value, color):
        """Updates the Tkinter UI dynamically during recursion."""
        self.cells[(row, col)].delete(0, tk.END)
        if value != "":
            self.cells[(row, col)].insert(0, str(value))
        self.cells[(row, col)].config(fg=color)
        self.root.update()  # Force GUI to refresh
        time.sleep(self.delay)

    def clear_board(self):
        for row in range(9):
            for col in range(9):
                self.cells[(row, col)].delete(0, tk.END)
                self.cells[(row, col)].config(fg="#ffffff")

    def load_demo_board(self):
        self.clear_board()
        demo = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        for row in range(9):
            for col in range(9):
                if demo[row][col] != 0:
                    self.cells[(row, col)].insert(0, str(demo[row][col]))
                    self.cells[(row, col)].config(fg="#4fc3f7") # Highlight original numbers

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverApp(root)
    root.mainloop()
