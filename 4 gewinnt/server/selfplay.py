import numpy as np
import torch
from game import Connect4
from model import AZNet, board_to_tensor
from mcts import Node, run_mcts

def play_game(model, device="cpu", simulations=200):
    g = Connect4()
    states = []
    policies = []
    players = []

    while True:
        root = Node(g.clone())
        probs = run_mcts(root, model, simulations=simulations, device=device, temperature=1.0)
        states.append(g.board.copy())
        policies.append(probs.copy())
        players.append(g.current_player)
        legal = g.legal_moves()
        mask = np.zeros_like(probs)
        mask[legal] = 1
        probs = probs * mask
        if probs.sum() == 0:
            a = np.random.choice(legal)
        else:
            probs = probs / probs.sum()
            a = np.random.choice(len(probs), p=probs)
        g.play(a)
        w = g.winner()
        if w is not None:
            if w == 0:
                values = [0] * len(players)
            else:
                values = [1 if p == w else -1 for p in players]
            return states, policies, values

def generate_selfplay_data(model_path, out_path, games=50, simulations=200):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AZNet()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    all_states = []
    all_policies = []
    all_values = []

    for _ in range(games):
        s, p, v = play_game(model, device=device, simulations=simulations)
        all_states.extend(s)
        all_policies.extend(p)
        all_values.extend(v)

    states_arr = np.stack(all_states, axis=0)
    policies_arr = np.stack(all_policies, axis=0)
    values_arr = np.array(all_values, dtype=np.float32)
    np.savez_compressed(out_path, states=states_arr, policies=policies_arr, values=values_arr)
