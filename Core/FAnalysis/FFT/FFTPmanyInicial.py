import copy
from FFTPone import *


class FFTPmanyInicial:
  def __init__(self, *args, **kwargs):
    if args.__len__() == 0:
      return

    self._config = args[0]
    self._config_timeframes = self._config.get('config', None)

    if self._config_timeframes is None:
      return

    del self._config['config']

  def run(self):
    for key, val in self._config_timeframes.items():
      print(f'  -> {key}   {val}')

      _candels = val['candels']
      _nffts = val['nfft']
      _sourse = {}

      for item_nfft in _nffts:
        __config = self._config
        __config['timeframe'] = key
        __config['candels'] = _candels
        __config['nfft'] = item_nfft
        _sourse[f'{key}{str(item_nfft)}'] = FFTPone(copy.deepcopy(__config))

      for key0, val0 in _sourse.items():
        print(f' запуск=> {key0} ')
        val0.start()

      for key0, val0 in _sourse.items():
        print(f' ожидание => {key0} ')
        val0.join()

