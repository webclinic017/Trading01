
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

class AILstm002(nn.Module ):
  def __init__(self,  *args, **kwargs):
    super(AILstm002, self).__init__()
    self.device = kwargs.get("device", "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")
    n_hidden = 51
    self.n_hidden = n_hidden
    self.lstm1 = nn.LSTMCell(1, self.n_hidden, dtype=torch.float64)
    self.lstm2 = nn.LSTMCell(self.n_hidden, self.n_hidden, dtype=torch.float64)
    self.linear = nn.Linear(self.n_hidden, 1, dtype=torch.float64)
    # self.tanh = nn.Tanh(self.n_hidden, 1, dtype=torch.float64)

  def forward(self, x, future=0):
    output ={}
    outputs = []
    n_samples = x.size(0)

    h_t = torch.zeros(n_samples, self.n_hidden, dtype=torch.float64)
    c_t = torch.zeros(n_samples, self.n_hidden, dtype=torch.float64)
    h_t2 = torch.zeros(n_samples, self.n_hidden, dtype=torch.float64)
    c_t2 = torch.zeros(n_samples, self.n_hidden, dtype=torch.float64)

    for input_t in x.split(1, dim=1):
      # N, 1
      h_t, c_t = self.lstm1(input_t, (h_t, c_t))
      h_t2, c_t2 = self.lstm2(h_t, (h_t, c_t))
      output = self.linear(h_t2)
      # output = self.tanh(h_t2)
      outputs.append(output)

    for i in range(future):
      h_t, c_t = self.lstm1(output, (h_t, c_t))
      h_t2, c_t2 = self.lstm2(h_t, (h_t, c_t))
      output = self.linear(h_t2)
      outputs.append(output)

    outputs = torch.cat(outputs, dim=1)
    return outputs


'''
device=""

class LSTMPredictor(nn.Module):
  def __init__(self, n_hidden=51):
    super(LSTMPredictor, self).__init__()
    self.n_hidden = n_hidden
    self.lstm1 = nn.LSTMCell(1, self.n_hidden, dtype=torch.float64)
    self.lstm2 = nn.LSTMCell(self.n_hidden, self.n_hidden, dtype=torch.float64)
    self.linear = nn.Linear(self.n_hidden, 1, dtype=torch.float64)
    # self.tanh = nn.Tanh(self.n_hidden, 1, dtype=torch.float64)
    
  def forward(self, x, future=0):
    outputs = []
    n_samples = x.size(0)

    h_t = torch.zeros(n_samples, self.n_hidden, dtype=torch.float64)
    c_t = torch.zeros(n_samples, self.n_hidden, dtype=torch.float64)
    h_t2 = torch.zeros(n_samples, self.n_hidden, dtype=torch.float64)
    c_t2 = torch.zeros(n_samples, self.n_hidden, dtype=torch.float64)

    for input_t in x.split(1, dim=1):
      # N, 1
      h_t, c_t = self.lstm1(input_t, (h_t, c_t))
      h_t2, c_t2 = self.lstm2(h_t, (h_t, c_t))
      output = self.linear(h_t2)
      # output = self.tanh(h_t2)
      outputs.append(output)

    for i in range(future):
      h_t, c_t = self.lstm1(output, (h_t, c_t))
      h_t2, c_t2 = self.lstm2(h_t, (h_t, c_t))
      output = self.linear(h_t2)
      outputs.append(output)

    outputs = torch.cat(outputs, dim=1)
    return outputs



'''