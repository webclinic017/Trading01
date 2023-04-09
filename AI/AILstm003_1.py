
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class AILstm003_1(nn.Module ):
  def __init__(self,  *args, **kwargs):
    super(AILstm003_1, self).__init__()
    self.device = kwargs.get("device", "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    self.lstm = nn.LSTM(input_size=1, hidden_size=50, num_layers=1, batch_first=True,  dtype=torch.float64)
    self.selu = nn.SELU()
    self.linear0 = nn.Linear(50, 100,  dtype=torch.float64)
    self.linear1 = nn.Linear(100, 50,  dtype=torch.float64)
    self.linear = nn.Linear(50, 1,  dtype=torch.float64)
    self.drop20 = nn.Dropout(p=0.2)
    self.drop30 = nn.Dropout(p=0.3)

  def forward(self, x):
    x, _ = self.lstm(x)
    x = self.selu(x)
    x = self.linear0(x)
    x = self.selu(x)
    # x = self.drop20(x)
    x = self.linear1(x)
    x = self.selu(x)
    # x = self.drop30(x)
    x = self.linear(x)
    return x
