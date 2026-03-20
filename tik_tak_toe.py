import tkinter as tk

xo = False
values = [""] * 9
ai_mode = False
game_over = False

root = tk.Tk()
root.title("tik tak toe")

class AI:
    def __init__(self):
        self.values = [""] * 9

    def test_for_2(self, board, symbol):
        wins = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6)
        ]
        for a, b, c in wins:
            line = [board[a], board[b], board[c]]
            if line[0] == line[1] == symbol and line[2] == "":
                return c
            if line[1] == line[2] == symbol and line[0] == "":
                return a
            if line[0] == line[2] == symbol and line[1] == "":
                return b
        return None

    def test(self, board):
        move = self.test_for_2(board, "O")
        if move is not None:
            return move

        move = self.test_for_2(board, "X")
        if move is not None:
            return move
        if board[4] == "":
            return 4
        for i in [0, 2, 6, 8]:
            if board[i] == "":
                return i
        for i in [1, 3, 5, 7]:
            if board[i] == "":
                return i
        return None

    def move(self, value):
        global values, xo
        if value is None:
            return
        values[value] = "O"
        text(value, values[value])



def test_win(X = ""):
    global game_over
    global xo
    if game_over:
        return
    if values[0] == values[1] == values[2] == X != "" or values[3] == values[4] == values[5] == X != "" or values[6] == values[7] == values[8] == X != "":
        game_over = True
        root.destroy()
        print(f"{X} win")
        return
    if values[0] == values[3] == values[6] == X != "" or values[1] == values[4] == values[7] == X != "" or values[2] == values[5] == values[8] == X != "":
        game_over = True
        root.destroy()
        print(f"{X} win")
        return
    if values[0] == values[4] == values[8] == X != "" or values[2] == values[4] == values[6] == X != "":
        game_over = True
        root.destroy()
        print(f"{X} win")
        return
    if all(v != "" for v in values):
        game_over = True
        root.destroy()
        print("keiner gewinnt!")



def text(index, text_):
    buttons[index]["text"] = text_

def on_click(index):
    global xo, game_over
    if game_over:
        return
    if values[index] != "":
        return

    if ai_mode:
        values[index] = "X"
        text(index, values[index])
        if game_over:
            return
        xo = not xo
        move = ai_obj.test(values)
        ai_obj.move(move)
        test_win("X")
        test_win("O")
    else:
        values[index] = "X" if xo else "O"
        xo = not xo
        text(index, values[index])
        test_win("X")
        test_win("O")

for r in range(3):
    root.rowconfigure(r, weight=1)
for c in range(3):
    root.columnconfigure(c, weight=1)

buttons = []

for i in range(9):
    btn = tk.Button(root,
                    text="   ",
                    font=("Arial", 32),
                    command=lambda idx=i: on_click(idx))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
    buttons.append(btn)

ai_mode = False if input("ai mode [y/n]?: ") == "n" else True
ai_obj = AI() if ai_mode else None

if ai_mode:
    print("ai mode")
else:
    print("no ai, 2 player mode")

def main():
    root.lift()
    root.attributes("-topmost", True)
    root.after(100, lambda: root.attributes("-topmost", False))
    root.mainloop()


if __name__ == "__main__":
    main()