import tkinter as tk

class SudokuSolver:
    def __init__(self):
        self.board = [[0]*9 for _ in range(9)]

    def set_board(self, board):
        self.board = [row[:] for row in board]

    def get_board(self):
        return [row[:] for row in self.board]

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return r, c
        return None

    def valid(self, num, pos):
        r, c = pos
        if any(self.board[r][i] == num for i in range(9)):
            return False
        if any(self.board[i][c] == num for i in range(9)):
            return False
        br = (r // 3) * 3
        bc = (c // 3) * 3
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if self.board[i][j] == num:
                    return False
        return True

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        r, c = empty
        for num in range(1, 10):
            if self.valid(num, (r, c)):
                self.board[r][c] = num
                if self.solve():
                    return True
                self.board[r][c] = 0
        return False

    # ---------------- GUI ----------------

    def start_gui(self):
        self.root = tk.Tk()
        self.root.title("Sudoku Solver")

        self.cells = []
        for r in range(9):
            row = []
            for c in range(9):

                # Rahmen für 3×3 Blöcke
                top = 2 if r % 3 != 0 else 5
                left = 2 if c % 3 != 0 else 5

                e = tk.Entry(
                    self.root,
                    width=2,
                    font=("Arial", 24),
                    justify="center",
                    relief="solid",
                    bd=1
                )
                e.grid(row=r, column=c, padx=(left,2), pady=(top,2))

                # Pfeiltasten binden
                e.bind("<Up>", lambda ev, rr=r, cc=c: self.move(rr, cc, -1, 0))
                e.bind("<Down>", lambda ev, rr=r, cc=c: self.move(rr, cc, 1, 0))
                e.bind("<Left>", lambda ev, rr=r, cc=c: self.move(rr, cc, 0, -1))
                e.bind("<Right>", lambda ev, rr=r, cc=c: self.move(rr, cc, 0, 1))

                row.append(e)
            self.cells.append(row)

        solve_btn = tk.Button(self.root, text="Lösen", font=("Arial", 16), command=self.gui_solve)
        solve_btn.grid(row=9, column=0, columnspan=9, pady=10)

        self.root.mainloop()

    def move(self, r, c, dr, dc):
        nr = (r + dr) % 9
        nc = (c + dc) % 9
        self.cells[nr][nc].focus_set()

    def gui_read(self):
        board = []
        for r in range(9):
            row = []
            for c in range(9):
                val = self.cells[r][c].get()
                row.append(int(val) if val.isdigit() else 0)
            board.append(row)
        return board

    def gui_write(self, board):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].delete(0, tk.END)
                if board[r][c] != 0:
                    self.cells[r][c].insert(0, str(board[r][c]))

    def gui_solve(self):
        self.set_board(self.gui_read())
        if self.solve():
            self.gui_write(self.board)
        else:
            print("Keine Lösung gefunden")




solver = SudokuSolver()
solver.start_gui()
