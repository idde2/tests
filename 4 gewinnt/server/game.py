import numpy as np

ROWS, COLS = 6, 7

class Connect4:
    def __init__(self):
        self.board = np.zeros((ROWS, COLS), dtype=np.int8)
        self.current_player = 1

    def clone(self):
        g = Connect4()
        g.board = self.board.copy()
        g.current_player = self.current_player
        return g

    def legal_moves(self):
        return [c for c in range(COLS) if self.board[0, c] == 0]

    def play(self, col):
        for r in range(ROWS - 1, -1, -1):
            if self.board[r, col] == 0:
                self.board[r, col] = self.current_player
                self.current_player *= -1
                return True
        return False

    def winner(self):
        b = self.board
        for r in range(ROWS):
            for c in range(COLS):
                if b[r, c] == 0:
                    continue
                p = b[r, c]
                if c <= COLS - 4 and all(b[r, c + i] == p for i in range(4)):
                    return p
                if r <= ROWS - 4 and all(b[r + i, c] == p for i in range(4)):
                    return p
                if c <= COLS - 4 and r <= ROWS - 4 and all(b[r + i, c + i] == p for i in range(4)):
                    return p
                if c >= 3 and r <= ROWS - 4 and all(b[r + i, c - i] == p for i in range(4)):
                    return p
        if not self.legal_moves():
            return 0
        return None
