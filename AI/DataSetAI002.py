import torch
from sklearn.preprocessing import MinMaxScaler

from DataSetBasa import DataSetBasa
from LoadSavePickle import LoadSavePickle
import os.path


class DataSetAI002(DataSetBasa):
  def __init__(self, *args, **kwargs):
    # DataSetBasa.__init__(self, *args, **kwargs)
    # Pасчета тип ==> Min -- Max
    kwargs['func'] = self.fMinMax
    super().__init__(*args, **kwargs)
    self._path = ""
    if args.__len__() == 0:
      raise "Нет значений в => DataSetAI002 -> args==0"
    else:
      self._path = args[0]
      if os.path.exists(self._path):
        pass
      else:
        raise "Путь к файлу c данными не существует"

    step_count = kwargs.get("step_count", {})
    if len(step_count) == 0:
      self._interval_train = 200
      self._interval_test = 25
      self._step = 25
    else:
      self._interval_train = step_count.get('interval_train', 200)
      self._interval_test = step_count.get('interval_test', 25)
      self._step = step_count.get('step', 25)

    self._train_input_sklear = MinMaxScaler(feature_range=(-1, 1))
    self._train_target_sklear = MinMaxScaler(feature_range=(-1, 1))
    self._test_input_sklear = MinMaxScaler(feature_range=(-1, 1))
    self._test_target_sklear = MinMaxScaler(feature_range=(-1, 1))
    self._iniciall_data()
    k = 1

  def _iniciall_data(self):
    _lPickle = LoadSavePickle()
    _loadFKaufman = _lPickle.load_path(self._path)
    self._input = _loadFKaufman.close
    self._target = _loadFKaufman.dcfk
    self._input_count = len(self._input)
    self._target_count = len(self._target)

  def func02(self):
    return ({}, {}), ({}, {})

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
