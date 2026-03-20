import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from model import AZNet, board_to_tensor

def train_model(data_path, model_in_path, model_out_path, epochs=5, batch_size=64, lr=1e-3):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    data = np.load(data_path)
    states = data["states"]
    policies = data["policies"]
    values = data["values"]

    model = AZNet()
    if model_in_path is not None:
        model.load_state_dict(torch.load(model_in_path, map_location=device))
    model.to(device)

    opt = optim.Adam(model.parameters(), lr=lr)
    mse = nn.MSELoss()

    idx = np.arange(len(states))
    for epoch in range(epochs):
        np.random.shuffle(idx)
        for i in range(0, len(idx), batch_size):
            batch_idx = idx[i:i+batch_size]
            b_states = states[batch_idx]
            b_policies = torch.from_numpy(policies[batch_idx]).float().to(device)
            b_values = torch.from_numpy(values[batch_idx]).float().to(device)

            x = []
            for s in b_states:
                x.append(board_to_tensor(s, 1).numpy())
            x = torch.from_numpy(np.stack(x, axis=0)).float().to(device)

            logp, v = model(x)
            value_loss = mse(v.squeeze(-1), b_values)
            policy_loss = -(b_policies * logp).sum(dim=1).mean()
            loss = value_loss + policy_loss

            opt.zero_grad()
            loss.backward()
            opt.step()

    torch.save(model.state_dict(), model_out_path)
