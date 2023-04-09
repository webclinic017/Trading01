from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn import linear_model
import numpy as np


class DataSetBasa():
  def __init__(self, *args, **kwargs):
    # self._callDS = args[0]
    #
    # if args.__len__() > 1:
    #   self._args = args[1:args.__len__()]
    # else:
    #   self._args = {}
    self._args = args
    self._kwargs = kwargs
    self._train_input_sklear = {}
    self._train_target_sklear = {}
    self._test_input_sklear = {}
    self._test_target_sklear = {}
    self._train_input = {}
    self._train_target = {}
    self._test_input = {}
    self._test_target = {}

    self._interval_train = 0
    self._interval_test = 0
    self._step = 0

    self._input = {}
    self._target = {}
    self._input_count = 0
    self._target_count = 0

    self._funcXX = kwargs.get('func', self.func01x )
    k=1
  def Run(self):
    pass
    kkk = 1

    # self._input = {}
    # self._target = {}
    # self._input_count = 0
    # self._target_count = 0

  def func01x(self):
    return ({}, {}), ({}, {})

  def RunAI(self):
    for i in range(self._interval_train, self._input_count-self._step, self._step):
      self._train_input  = (np.array(self._input[i - self._interval_train:i])).transpose()
      self._train_target = (np.array(self._target[i - self._interval_train:i])).transpose()
      self._test_input = (np.array(self._input[i:i+self._step])).transpose()
      self._test_target = (np.array(self._target[i:i+self._step])).transpose()
      yield self._funcXX()
      # yield self.func01()

  def RunLSTM(self):
    return  self._funcXX()

    # for i in range(self._interval_train, self._input_count-self._step, self._step):
    #   self._train_input  = (np.array(self._input[i - self._interval_train:i])).transpose()
    #   self._train_target = (np.array(self._input[i:i+self._step])).transpose()
    #   yield self._funcXX()
    #   # yield self.func01()
