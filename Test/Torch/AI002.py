'''
Обратить вниманте!!!
ПЕРЕДЕЛАТЬ
--- пытаюсь скрестить lstm и обычную сеть

'''

import torch
from torch import nn, optim

from AILstm002 import AILstm002
from ConfigDbSing import ConfigDbSing
from DataSetAI002 import DataSetAI002
from TPlot import TPlot
from TPlot import PltShow
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn import linear_model
from LoadSavePickle import LoadSavePickle

import matplotlib.pyplot as plt

# device = "cpu" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

if __name__ == '__main__':
  print(" ===> AI-002 <===")
  _tPlot = TPlot()
  _connect_db = ConfigDbSing().get_config()
  _path_forLSTMdcfk = ConfigDbSing().path_files("Trading01\\NotGit\\Data\\forLSTMdcfk.pkl")

  _dsAi02 = DataSetAI002(_path_forLSTMdcfk, step_count= {'interval_train':200, 'interval_test':5, 'step':5})

  _aILstm002 = AILstm002(device="cpu")
  device = _aILstm002.device
  print(f"Using ->  {device}  device")

  model = _aILstm002.to(device)
  print(model)
  batch_size = 20
  loss_fn = nn.MSELoss()
  optimizer = optim.LBFGS(model.parameters(), lr=0.8)
  epochs = 10

  for _train, _test in _dsAi02.RunLSTM():
    (_train_x, _train_y) = _train
    (_test_x, _test_y) = _test

    for t in range(epochs):
      print(f"Epoch {t + 1}\n-------------------------------")
      size = len(_train_x)
      model.train()
      for batch in range(batch_size, size, batch_size):
        if (isinstance(batch, int)):
          pass
        else:
          break
        print(f"--> Batch = {batch}")
        X = _train_x[batch - batch_size:batch]
        y = _train_y[batch - batch_size:batch]

        model.train()
        def closure():
          optimizer.zero_grad()
          output = model(X)
          loss = loss_fn(output, y)
          loss.backward()
          return loss

        optimizer.step(closure)

        model.eval()
        with torch.no_grad():
          future = 0
          pred = model(_test_x, future=future)
          # loss = loss_fn(pred[:, :-future], _test_y)
          loss = loss_fn(pred, _test_y)
          print("test Loss-", loss.item())
          y0 = pred.detach().numpy()

        kkk = 1

      hhhhh=1
  k=1


'''

'''