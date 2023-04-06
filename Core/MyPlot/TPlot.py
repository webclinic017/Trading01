# https://www.youtube.com/watch?v=8V3y6NCdo0k    - хороший!!!
import matplotlib.pyplot as plt
#from datetime import time
import time

def PltShow():
    plt.show()

class TPlot():
    def __init__(self, *args, **kwargs):
        self._fread = kwargs.get("fread", None)
        self._dan_plot = {}

        if len(kwargs) > 0:
            self._fread = kwargs.get("fread", None)
            self._kwargs = kwargs


    def RunOneWin(self,  *args, **kwargs):

        # if(isinstance(args[0], list)):
        #   plt.figure()
        #   plt.plot(args[0])
        #   plt.grid()
        #   plt.show()
        #   return

        self._fread = kwargs.get("fread", None)

        if self._fread is None:
            return

        if len(args) > 0:
             title = args[0]

        i=0
        self._dan=[]
        for item0 in self._fread():
            __ncount_param = len(item0)
            if __ncount_param == 0:
                continue

            if 'test0' in item0:
                plt.figure()
                plt.title(f"{title}  {i} ")

                _dan =item0['test0']['dan']
                _count_dan = len(_dan)
                self._dan.extend(_dan)
                _count_dan_2 = _count_dan//2+_count_dan
                _count_all_dan = len(self._dan)

                self._dan = self._dan if _count_all_dan < _count_dan_2 else  self._dan[_count_all_dan-_count_dan_2:]

                plt.plot(self._dan)
                plt.grid()
                plt.show()
                i=i+1
#                time.sleep(1)
                k=1
#        plt.show()

    def PlotDict(self, dmas, show=True):
        _title = dmas.get('title', "-")
        _t = dmas.get('t', [])
        try:
            _ = dmas.pop('title')
        except:
            pass
        try:
            _ = dmas.pop('t')
        except:
            pass

        _count_key = dmas.keys()
        if len(_count_key) < 1:
            return

        if len(_t)==0:
          _s =  list(_count_key)[0]
          _t = range(len(dmas[ list(_count_key)[0]]))

        plt.figure()
        plt.title(f"{_title}  ")

        for it in _count_key:
            plt.plot(_t, dmas[it])

        plt.grid(True)
        if show:
            plt.show()

    def add_plot(self, **kwargs):
        _nplot = kwargs.get('nplot', len(self._dan_plot))
        _xy = kwargs.get('xy', None)
        _t = kwargs.get('t', None)
        _txt = kwargs.get('txt', None)
        _namey = kwargs.get('namey', None)

        if (_nplot is None) or (_xy is None):
            return

        d = {'xy': _xy}

        if _t is not None:
            d['t'] = _t

        if _txt is not None:
            d['txt'] = _txt

        if _namey is not None:
            d['namey'] = _namey

        _title = kwargs.get('title', None)
        if _title is not None:
            d['title'] = _title

        self._dan_plot[_nplot] = d


        # if _nplot
        # try:
        #     x = self._dan_plot
        #     pass
        # except:
        #     pass

    def show_plots_column1(self):
        count = len(self._dan_plot)

        if count == 0:
            return
        __title=None

        fig, axs = plt.subplots(count, 1)             # Нарисовать сигнал временной области
        plt.title(__title)

        for i in range(count):
            d = self._dan_plot[i]
            if 't' in d.keys():
                axs[i].plot(d['t'], d['xy'])
            else:
                axs[i].plot(d['xy'])
                axs[i].grid(True)
            if 'txt' in d.keys():
                axs[i].text(d['txt']['xy'][0], d['txt']['xy'][1], d['txt']['txt'])
                axs[i].grid(True)

            if 'namey' in d.keys():
                axs[i].set_ylabel(d['namey'])

            if 'title'  in d.keys():
                __title = d['title']

        # if __title is not None:
        #     plt.title(__title )
        #plt.grid(True)

        plt.show()


    #         axs[0,0].plot(x2)
    # _z2 = myFFT(x2)
    # axs[0,1].text(100, 0.01, _z2[2], va = 'baseline')
    # axs[0,1].plot(_z2[1], _z2[0])
    #
    # x4 = dan[n_start:n_start+ncount, 4]
    # axs[1,0].plot(x4)
    # _z4 = myFFT(x4)
    # axs[1,1].text(100, 0.01, _z4[2], va = 'baseline')
    # axs[1,1].plot(_z4[1], _z4[0])

