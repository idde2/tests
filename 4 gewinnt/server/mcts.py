import math
import numpy as np
import torch
from game import Connect4
from model import board_to_tensor

class Node:
    def __init__(self, game, parent=None, prior=0.0):
        self.game = game
        self.parent = parent
        self.prior = prior
        self.children = {}
        self.visit_count = 0
        self.value_sum = 0.0

    @property
    def value(self):
        return 0 if self.visit_count == 0 else self.value_sum / self.visit_count

def ucb_score(parent, child, c_puct=1.4):
    return child.value + c_puct * child.prior * math.sqrt(parent.visit_count) / (1 + child.visit_count)

def select_child(node):
    return max(node.children.items(), key=lambda kv: ucb_score(node, kv[1]))

def expand(node, policy, legal_moves):
    for a in legal_moves:
        if a not in node.children:
            prior = float(policy[a].item())
            g = node.game.clone()
            g.play(a)
            node.children[a] = Node(g, parent=node, prior=prior)

def backpropagate(path, value):
    for node in reversed(path):
        node.visit_count += 1
        node.value_sum += value
        value = -value

def run_mcts(root, model, simulations=200, device="cpu", temperature=1.0):
    for _ in range(simulations):
        node = root
        path = [node]

        while node.children:
            action, node = select_child(node)
            path.append(node)

        winner = node.game.winner()
        if winner is None:
            x = board_to_tensor(node.game.board, node.game.current_player).unsqueeze(0).to(device)
            with torch.no_grad():
                logp, v = model(x)
            p = logp.exp().squeeze(0)
            legal = node.game.legal_moves()
            mask = np.zeros_like(p.cpu().numpy())
            mask[legal] = 1
            p = p * torch.from_numpy(mask).to(p.device)
            if p.sum() > 0:
                p = p / p.sum()
            expand(node, p, legal)
            value = float(v.item())
        else:
            value = 0 if winner == 0 else (1 if winner == node.game.current_player else -1)

        backpropagate(path, value)

    visits = np.zeros(7, dtype=np.float32)
    for a, child in root.children.items():
        visits[a] = child.visit_count
    if temperature == 0:
        probs = np.zeros_like(visits)
        best = np.argmax(visits)
        probs[best] = 1.0
        return probs
    visits = visits ** (1.0 / temperature)
    visits = visits / (visits.sum() + 1e-8)
    return visits
