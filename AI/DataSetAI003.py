import torch
from sklearn.preprocessing import MinMaxScaler

from DataSetBasa import DataSetBasa
from LoadSavePickle import LoadSavePickle
import os.path
import numpy as np

class DataSetAI003(DataSetBasa):
  def __init__(self, *args, **kwargs):
    # DataSetBasa.__init__(self, *args, **kwargs)
    # Pасчета тип ==> Min -- Max
    kwargs['func'] = self.fMinMaxLSTM
    super().__init__(*args, **kwargs)
    self._path = ""
    if args.__len__() == 0:
      raise "Нет значений в => DataSetAI003 -> args==0"
    else:
      self._path = args[0]
      if os.path.exists(self._path):
        pass
      else:
        raise "Путь к файлу c данными не существует"

    step_count = kwargs.get("step_count", {})
    if len(step_count) == 0:
      self._interval_train = -1
      self._interval_test = 250
      self._step = 5
      self._count_min = -1
      self._count_max = -1
      self._delta = 5

    else:
      self._interval_train = step_count.get('interval_train', -1)
      self._interval_test = step_count.get('interval_test', 250)
      self._step = step_count.get('step', 5)
      self._count_min = step_count.get('count_min', -1)
      self._count_max = step_count.get('count_max', -1)
      self._delta = step_count.get("delta", 5 )

    self._train_input_sklear = MinMaxScaler(feature_range=(-1, 1))
    self._train_target_sklear = MinMaxScaler(feature_range=(-1, 1))
    self._iniciall_data()
    k = 1

  def _iniciall_data(self):
    _lPickle = LoadSavePickle()
    _loadFKaufman = _lPickle.load_path(self._path)
    if (self._count_min >= 0) & (self._count_max > 0):
      __input = np.array(_loadFKaufman.close)
      self._input = __input[self._count_min : self._count_max]
    else:
      self._input = np.array(_loadFKaufman.close)

    self._input = np.expand_dims(self._input, axis=1)
    self._input_count = len(self._input)
    if self._interval_train <=0:
      self._interval_train = self._input_count-self._interval_test # -self._delta-2
      self.train = self._input[:self._interval_train,:]
      self.test = self._input[-self._interval_test:,:]
    else:
      pass

  def get_input(self):
    return self._input
  def get_traid_count(self):
    return self._interval_train
  def func02(self):
    return ({}, {}), ({}, {})

  def ___fFormData(self, istart, iend):
    X, y = [], []
    for i in range(istart, iend):
      if (i-self._step)<0:
        feature = np.zeros((self._step, 1))
        target = np.zeros((self._step, 1))
        for j in range(i):
          feature[j]=self._input[j]
          target[j]=self._input[j+1]
      else:
        feature = self._input[i-self._step:i, :]
        target = self._input[i+1 - self._step :i+1 , :] # + self._delta
      X.append(feature)
      y.append(target)

    xx=np.array(X)
    yy=np.array(y)
      # print(yy.shape)
    return  torch.tensor(xx, dtype=torch.float64), \
            torch.tensor(yy, dtype=torch.float64)

  def ___fFormData0(self, istart, iend):
    X, y = [], []
    for i in range(istart, iend):
      if (i-self._step)<0:
        feature = np.zeros((self._step, 1))
        target = np.zeros((self._step, 1))
        for j in range(i):
          feature[j]=self._input[j]
          target[j]=self._input[j]
      else:
        feature = self._input[i-self._step:i, :]
        target = self._input[i - self._step :i, :]
      X.append(feature)
      y.append(target)
    return  torch.tensor(np.array(X), dtype=torch.float64), \
            torch.tensor(np.array(y), dtype=torch.float64)

  def fMinMaxLSTM(self):
    return self.___fFormData(0, self._interval_train), self.___fFormData0(self._input_count-self._interval_test, self._input_count)


    # # ----  train   ----
    # _ = self._train_input_sklear.fit(self._train_input.reshape(self._interval_train, -1))
    # norm_train_input = self._train_input_sklear.transform(self._train_input.reshape(self._interval_train, -1))
    # _ = self._train_target_sklear.fit(self._train_target.reshape(self._interval_train, -1))
    # norm_train_target = self._train_target_sklear.transform(self._train_target.reshape(self._interval_train, -1))
    #
    # # ----  test   ----
    # _ = self._test_input_sklear.fit(self._test_input.reshape(self._step, -1))
    # norm_test_input = self._test_input_sklear.transform(self._test_input.reshape(self._step, -1))
    # _ = self._test_target_sklear.fit(self._test_target.reshape(self._step, -1))
    # norm_test_target = self._test_target_sklear.transform(self._test_target.reshape(self._step, -1))
    #
    # return (torch.from_numpy(norm_train_input), torch.from_numpy(norm_train_target)), \
    #   (torch.from_numpy(norm_test_input), torch.from_numpy(norm_test_target))

  def fMinMax(self):
    # ----  train   ----
    _ = self._train_input_sklear.fit(self._train_input.reshape(self._interval_train, -1))
    norm_train_input = self._train_input_sklear.transform(self._train_input.reshape(self._interval_train, -1))
    _ = self._train_target_sklear.fit(self._train_target.reshape(self._interval_train, -1))
    norm_train_target = self._train_target_sklear.transform(self._train_target.reshape(self._interval_train, -1))

    # ----  test   ----
    _ = self._test_input_sklear.fit(self._test_input.reshape(self._step, -1))
    norm_test_input = self._test_input_sklear.transform(self._test_input.reshape(self._step, -1))
    _ = self._test_target_sklear.fit(self._test_target.reshape(self._step, -1))
    norm_test_target = self._test_target_sklear.transform(self._test_target.reshape(self._step, -1))

    return (torch.from_numpy(norm_train_input), torch.from_numpy(norm_train_target)), \
      (torch.from_numpy(norm_test_input), torch.from_numpy(norm_test_target))
