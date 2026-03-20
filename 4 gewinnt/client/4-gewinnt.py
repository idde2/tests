import tkinter as tk
import requests
from config import SERVER

values = [None] * 42
root = tk.Tk()
root.title("4 gewinnt")
xo = False

for r in range(6):
    root.rowconfigure(r, weight=1)
for c in range(7):
    root.columnconfigure(c, weight=1)

buttons = []

def text(index, color):
    buttons[index]["bg"] = color

def get_xy(index):
    return index % 7, index // 7

def drop_piece(column):
    for row in range(5, -1, -1):
        idx = column + row * 7
        if values[idx] is None:
            return idx
    return None

def test_win(v):
    for y in range(6):
        for x in range(4):
            i = x + y * 7
            if v[i] is not None and v[i] == v[i+1] == v[i+2] == v[i+3]:
                return True
    for x in range(7):
        for y in range(3):
            i = x + y * 7
            if v[i] is not None and v[i] == v[i+7] == v[i+14] == v[i+21]:
                return True
    for y in range(3):
        for x in range(4):
            i = x + y * 7
            if v[i] is not None and v[i] == v[i+8] == v[i+16] == v[i+24]:
                return True
    for y in range(3, 6):
        for x in range(4):
            i = x + y * 7
            if v[i] is not None and v[i] == v[i-6] == v[i-12] == v[i-18]:
                return True
    return False

def board_to_matrix(values):
    m = [[None]*7 for _ in range(6)]
    for i,v in enumerate(values):
        m[i//7][i%7] = 1 if v else (-1 if v is not None else 0)
    return m

def ai_move():
    board = board_to_matrix(values)
    player = 1 if xo else -1

    r = requests.post(f"{SERVER}/move", json={
        "board": board,
        "player": player
    })
    col = r.json()["column"]

    idx = drop_piece(col)
    if idx is None:
        return
    values[idx] = xo
    text(idx, "red" if xo else "yellow")

    if test_win(values):
        print("KI gewinnt!")
        root.destroy()
        return

    toggle_player()

def toggle_player():
    global xo
    xo = not xo
    label.config(text="red" if xo else "yellow")

def on_click(index):
    global xo
    x, _ = get_xy(index)
    idx = drop_piece(x)
    if idx is None:
        return

    values[idx] = xo
    text(idx, "red" if xo else "yellow")

    if test_win(values):
        print("Du gewinnst!")
        root.destroy()
        return

    toggle_player()
    #ai_move()

for i in range(42):
    btn = tk.Button(
        root,
        text="   ",
        font=("Arial", 32),
        command=lambda idx=i: on_click(idx),
        bg="white"
    )
    btn.grid(row=i // 7, column=i % 7, padx=5, pady=5, sticky="nsew")
    buttons.append(btn)

label = tk.Label(root, text="red" if xo else "yellow")
label.grid(padx=5, pady=5)

mode = input("Modus wählen: [t]raining oder [s]pielen? ").strip().lower()
if mode.startswith("t"):
    print("Training wird auf dem Server gestartet...")
    r = requests.post(f"{SERVER}/train")
    print(r.json())
else:
    root.mainloop()
