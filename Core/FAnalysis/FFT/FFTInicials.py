
import copy
from FFTOneTimeInicial import FFTOneTimeInicial

class FFTInicials:
    def __init__(self, *args, **kwargs):
        self._config = args[0].get('config', None)
        if self._config is None:
            return
        del args[0]['config']
        self._args = args
        k=1

    def run(self):
        _calc_fft = {}
        for key, val in self._config.items():
            self._args[0]['nametime'] = key
            self._args[0]['candels'] = val['candels']
            self._args[0]['nfft'] = val['nfft']
            print(" ")
            _calc_fft[key] = FFTOneTimeInicial(*copy.deepcopy(self._args))

        print(" ====  запускаем расчет =====")
        for key, val in _calc_fft.items():
            print(f"  {key}")
            val.start()

        print(" ====  запускаем ожидание завершение потоков !!!!  =====")
        for key, val in _calc_fft.items():
            print(f"  {key}")
            val.join()
        print("---  все потоки закончились  -- ")
