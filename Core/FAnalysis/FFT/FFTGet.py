
#import threading
from ElementPostgres import ElementPostgres


class FFTGet(ElementPostgres):
    def __init__(self, *args, **kwargs):
        ElementPostgres.__init__(self, *args, 'fft', 'json', **kwargs)


    def get(self, **kwargs ):
        dan = self.get_field(**kwargs)
        return dan


    def fft_key(self, **kwargs):
        return self.get_key_dict_field1(**kwargs)

    def get_key_dict(self, **kwargs):
        keys = kwargs.get('keys', ['open'])
        _ls_keys = self.get_key_dict_field1(**kwargs)
        if len(keys)==0:
            return None
        _ls = [item for item in keys if item in _ls_keys]
        dan = self.get_field(**kwargs)
        _sourse = {}
        _fft = dan['fft']
        _dfft = {key:[] for key in _ls}
        for key, val in  _fft.items():
            for item_key in _ls:
                _dfft[item_key]+=[val[item_key]]
        _dfft['datetime'] = [ val for key, val in  dan['datetime'].items()]
        return _dfft

        # for item in _ls:
        #     ccc =dan['fft'][item]
        #     kkk=1
#
# class FFTOneTimeInicial(threading.Thread, ElementPostgres):
#     def __init__(self, *args, **kwargs):
#         threading.Thread.__init__(self)
#         ElementPostgres.__init__(self, *args, 'fft', 'json', **kwargs)
