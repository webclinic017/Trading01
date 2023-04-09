
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class AILstm003(nn.Module ):
  def __init__(self,  *args, **kwargs):
    super(AILstm003, self).__init__()
    self.device = kwargs.get("device", "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    self.lstm = nn.LSTM(input_size=1, hidden_size=50, num_layers=1, batch_first=True,  dtype=torch.float64)
    self.linear = nn.Linear(50, 1,  dtype=torch.float64)

  def forward(self, x):
    x, _ = self.lstm(x)
    x = self.linear(x)
    return x

