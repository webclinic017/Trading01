'''
-- Работает но не правильно
    переделка -> AI002
'''


from TPlot import TPlot
from TPlot import PltShow
from Ticker import *
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn import linear_model
from LoadSavePickle import LoadSavePickle

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt


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



if __name__ == '__main__':
  print(" ===> AI-001 <===")
  _tPlot = TPlot()

  # _path_forLSTMdcfk = "E:\\MLserver\\Trading01\\NotGit\\Data\\forLSTMdcfk.pkl"
  _path_forLSTMdcfk = "E:\\Trading01\\NotGit\\Data\\forLSTMdcfk.pkl"
  _lPickle = LoadSavePickle()
  _loadFKaufman = _lPickle.load_path(_path_forLSTMdcfk)
  _close =  _loadFKaufman.close
  _dcfk = _loadFKaufman.dcfk

  _count_close = len(_close)
  _n_count = 200
  _n_step = 25
  train_sclose_min_max = MinMaxScaler(feature_range=(-1, 1))
  train_sdkc_min_max = MinMaxScaler(feature_range=(-1, 1))
  test_sclose_min_max = MinMaxScaler(feature_range=(-1, 1))
  test_sdkc_min_max = MinMaxScaler(feature_range=(-1, 1))
  for i in range(_n_count, _count_close-_n_step, _n_step):
    print(_count_close -i)
    # ----  train   ---
    _train_input = (np.array(_close[i-_n_count:i])).transpose()
    _train_target = (np.array(_dcfk[i-_n_count:i])).transpose()
    train_sclose_close__ = train_sclose_min_max.fit(_train_input.reshape(_n_count, -1))
    norm_train_input = train_sclose_min_max.transform(_train_input.reshape(_n_count, -1 ))
    train_sclose_dcfk__ = train_sdkc_min_max.fit(_train_target.reshape(_n_count, -1))
    norm_train_target = train_sdkc_min_max.transform(_train_target.reshape(_n_count, -1 ))
    # ----  test   ----
    j=i+_n_step
    _test_input = (np.array(_close[i:j])).transpose()
    _test_target = (np.array(_dcfk[i:j])).transpose()
    test_sclose_close__ = test_sclose_min_max.fit(_test_input.reshape(_n_step, -1))
    norm_test_input = test_sclose_min_max.transform(_test_input.reshape(_n_step, -1 ))
    test_sclose_dcfk__ = test_sdkc_min_max.fit(_test_target.reshape(_n_step, -1))
    norm_test_target = test_sdkc_min_max.transform(_test_target.reshape(_n_step, -1 ))

    # train_input = torch.from_numpy(norm_train_input[1:, :-1])
    # train_target = torch.from_numpy(norm_train_target[1:, 1:])
    # test_input = torch.from_numpy(norm_test_input[:1, :-1])
    # test_target = torch.from_numpy(norm_test_target[:1, 1:])
    train_input = torch.from_numpy(norm_train_input)
    train_target = torch.from_numpy(norm_train_target)
    test_input = torch.from_numpy(norm_test_input)
    test_target = torch.from_numpy(norm_test_target)

    print(train_input.shape, train_target.shape)
    print(test_input.shape, test_target.shape)

    batch_size = 8
    # device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    device = "cpu" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using {device} device")

    model = LSTMPredictor().to(device)
    print(model)

    # loss_fn = nn.CrossEntropyLoss()
    # optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

    loss_fn = nn.MSELoss()
    optimizer = optim.LBFGS(model.parameters(), lr=0.8)


    epochs = 10
    loss = {}

    for t in range(epochs):
      print(f"Epoch {t + 1}\n-------------------------------")
      size = len(train_input)
      model.train()
      # train_input_yx = [(train_input[i],train_target[i]) for i in range(len(train_input)) ]
      for batch in range(batch_size, len(train_input), batch_size):
        print(f"--> Batch = {batch}")
        X = train_input[batch-batch_size:batch]
        y = train_target[batch-batch_size:batch]
        def closure():
          optimizer.zero_grad()
          output = model(X)
          loss = loss_fn(output, y)
          loss.backward()
          return loss

        optimizer.step(closure)

        with torch.no_grad():
          future = 25
          pred = model(test_input, future=future)
          loss = loss_fn(pred[:, :-future], test_target)
          print("test Loss-", loss.item())
          y0 = pred.detach().numpy()

        kkk=1

      # test(test_dataloader, model, loss_fn)
    print("Done!")

    kkk=1
  k=1




  k=1


'''
    print(_count_close -i)
    _mclose = np.array(_close[i-_n_count:i])
    _mtclose = _mclose.transpose()
    _mdcfk = np.array(_dcfk[i-_n_count:i])
    _mtdcfk = _mdcfk.transpose()

    sclose_close = sclose_min_max.fit(_mtclose.reshape(_n_count, -1))
    norm_close_train = sclose_min_max.transform(_mtclose.reshape(_n_count, -1 ))

    sclose_dcfk = sclose_min_max.fit(_mtdcfk.reshape(_n_count, -1))
    norm_dcfk_train = sclose_min_max.transform(_mtdcfk.reshape(_n_count, -1 ))


    train_input = torch.from_numpy(norm_close[1:, :-1])
    train_target = torch.from_numpy(norm_dcfk[1:, 1:])
    test_input = torch.from_numpy(y[:1, :-1])
    test_target = torch.from_numpy(y[:1, 1:])

    print(train_input.shape, train_target.shape)
    print(test_input.shape, test_target.shape)

    model = LSTMPredictor()
    criterion = nn.MSELoss()
    optimizer = optim.LBFGS(model.parameters(), lr=0.8)

    n_steps = 10


----------------------------------
N = 2
L = 1000
T = 30

x = np.empty((N, L), np.float32)
x[:] = np.array(range(L))+np.random.randint(-4*T, 4*T, N).reshape(N, 1)
y = np.sin(x/1.0/T).astype(np.float32)

plt.figure(figsize=(10, 8))
plt.title("Sin wave")
plt.xlabel("x")
plt.xlabel("y")
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
#plt.plot(np.arange(x.shape[1]), y[0,:], 'r', linewidth=2.0 )
plt.plot(np.arange(x.shape[1]), y[0,:],  np.arange(x.shape[1]), y[1,:], 'r', 'b', linewidth=2.0)
plt.show()

jjj=1

if __name__ == '__main__':
    # y = 100, 1000
    train_input = torch.from_numpy(y[1:, :-1])
    train_target = torch.from_numpy(y[1:, 1:])
    test_input = torch.from_numpy(y[:1, :-1])
    test_target = torch.from_numpy(y[:1, 1:])

    print(train_input.shape, train_target.shape)
    print(test_input.shape, test_target.shape)

    model = LSTMPredictor()
    criterion = nn.MSELoss()

    optimizer = optim.LBFGS(model.parameters(), lr=0.8)

    n_steps = 10
    for i in range(n_steps):
        print("Step-",i)

        def closure():
            optimizer.zero_grad()
            out = model(train_input)
            loss = criterion(out, train_target)
            print("Loss-", loss.item())
            loss.backward()
            return loss
        optimizer.step(closure)

        with torch.no_grad():
            future = 1000
            pred = model(test_input, future=future)
            loss = criterion(pred[:, :-future], test_target)
            print("test Loss-", loss.item())
            y = pred.detach().numpy()

        plt.figure(figsize=(12, 6))
        plt.title(f"Strp {i+1} ")
        plt.xlabel("x")
        plt.xlabel("y")
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        n = train_input.shape[1]    #999
        def draw(y_i, color):
            plt.plot(np.arange(n), y_i[:n], color, linewidth=2.0)
            plt.plot(np.arange(n, n+future), y_i[n:], color+":", linewidth=2.0)
        draw(y[0], 'r')
        # draw(y[1], 'b')
        # draw(y[2], 'g')

        # plt.savefig("predict%d.pdf"%i)
        # plt.close()
plt.show()
k=1



'''