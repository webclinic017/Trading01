
import torch
from torch import nn, optim
import torch.utils.data as data

from AILstm003 import AILstm003
from ConfigDbSing import ConfigDbSing
from DataSetAI003 import DataSetAI003
from TPlot import TPlot
import numpy as np
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
  _step_lstm = 5
  _dsAi03 = DataSetAI003(_path_forLSTMdcfk, step_count= {'interval_train':-1, 'interval_test':250, 'step':_step_lstm})
  _train, _test = _dsAi03.RunLSTM()
  X_train, Y_train, X_test, Y_test  = _train[0], _train[1], _test[0], _test[1]
  print(X_train.shape, Y_train.shape)
  print(X_test.shape, Y_test.shape)
  _close = _dsAi03.get_input()
  train_size =_dsAi03.get_traid_count()
  _aILstm003 = AILstm003(device="cpu")
  device = _aILstm003.device
  print(f"Using ->  {device}  device")

  model = _aILstm003.to(device)
  print(model)
  batch_size = 25
  optimizer = optim.Adam(model.parameters())
  loss_fn = nn.MSELoss()
  loader = data.DataLoader(data.TensorDataset(X_train, Y_train), shuffle=True, batch_size=batch_size)

  n_epochs = 2000

  for epoch in range(n_epochs):
    model.train()
    for X_batch, y_batch in loader:
      y_pred = model(X_batch)
      loss = loss_fn(y_pred, y_batch)
      optimizer.zero_grad()
      loss.backward()
      optimizer.step()
    # Validation
    if epoch % 10 != 0:
      continue
    model.eval()
    with torch.no_grad():
      y_pred = model(X_train)
      train_rmse = np.sqrt(loss_fn(y_pred, Y_train))
      y_pred = model(X_test)
      test_rmse = np.sqrt(loss_fn(y_pred, Y_test))
    print("Epoch %d: train RMSE %.4f, test RMSE %.4f" % (epoch, train_rmse, test_rmse))

  with torch.no_grad():
    # shift train predictions for plotting
    train_plot = np.ones_like(_close) * np.nan
    y_pred = model(X_train)
    y_pred = y_pred[:, -1, :]
    train_plot[_step_lstm:train_size] = model(X_train)[:, -1, :]
    # shift test predictions for plotting
    test_plot = np.ones_like(_close) * np.nan
    test_plot[train_size + _step_lstm:len(_close)] = model(X_test)[:, -1, :]
  # plot
  plt.plot(_close)
  plt.plot(train_plot, c='r')
  plt.plot(test_plot, c='g')
  plt.show()


'''  
  for _train, _test in _dsAi03.RunLSTM():
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

