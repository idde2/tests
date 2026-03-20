from fastapi import FastAPI
from pydantic import BaseModel
import torch
import numpy as np

from game import Connect4
from model import AZNet, board_to_tensor
from mcts import Node, run_mcts
from selfplay import generate_selfplay_data
from train import train_model

app = FastAPI()

device = "cuda" if torch.cuda.is_available() else "cpu"
model_path = "models/latest.pt"

model = AZNet()
model.load_state_dict(torch.load(model_path, map_location=device))
model.to(device)
model.eval()

class MoveRequest(BaseModel):
    board: list
    player: int

@app.post("/move")
def move(req: MoveRequest):
    g = Connect4()
    g.board = np.array(req.board, dtype=np.int8)
    g.current_player = req.player

    root = Node(g)
    probs = run_mcts(root, model, simulations=200, device=device)
    legal = g.legal_moves()
    mask = np.zeros_like(probs)
    mask[legal] = 1
    probs = probs * mask
    if probs.sum() == 0:
        col = np.random.choice(legal)
    else:
        probs = probs / probs.sum()
        col = int(np.argmax(probs))

    return {"column": col}

@app.post("/train")
def train():
    data_path = "selfplay_data.npz"
    generate_selfplay_data(model_path, data_path, games=20, simulations=200)
    train_model(data_path, model_path, model_path, epochs=5)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return {"status": "training complete"}
