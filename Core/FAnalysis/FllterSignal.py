from scipy import signal
from scipy.fftpack import fft
import numpy as  np
import matplotlib.pyplot as plt


import pylab
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap

from PlotGraphs import PlotGraph


class MyFllter:
    def __init__(self, nfft = 64, kus=1):
        self.kus=kus
        self.__fs = 100
        self.__nfft =nfft
        self.__mfft = int( self.__nfft/2)
        self.sos = signal.ellip(24, 0.2, 1, 2, 'hp', fs=100, output='sos')
        self._plot = PlotGraph()

    def FEllip(self, sig, k=0):
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ellipord.html
        _jj = k
        return signal.sosfilt(self.sos, sig)* (k if k!=0 else self.kus)

    def FFT(self, sig):
        z = abs(fft(sig, n=None, axis=- 1, overwrite_x=False))
        _count = round( len(z)/2)
        return z[:_count]

    def FFTAll(self, sig):
        __count = len(sig)
        mSpectr = np.zeros((__count,  self.__mfft))
#        eSpectr = np.zeros((__count,  1))
        eSpectr = np.zeros((__count))

        for i in range(self.__nfft, __count):
            mSpectr[i:] = self.FFT(sig[i-self.__nfft: i])
            xx = np.sum(mSpectr[i:])
            eSpectr[i] = xx
        return eSpectr, mSpectr


    def FFTtest(self, sig):
        self.__fs = 100
        __n=10000
        t = np.linspace(0, __n, __n, False)
        w0=2*np.pi*0.5/self.__fs
        w1=2*np.pi*10/self.__fs
        sig =1.0* np.sin(w0*t) + 1.0* np.sin(w1*t)

        z1= self.FFT(sig)
        self._plot.OnePlot(z1, "Test ")

        return z1


    def TestFilter(self, f0=0.5, f1=10):
        __n=10000
        t = np.linspace(0, __n, __n, False)
        w0=2*np.pi*f0/self.__fs
        w1=2*np.pi*f1/self.__fs
        sig =1.0* np.sin(w0*t) + 1.0* np.sin(w1*t)

        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        ax1.plot(t, sig)
        ax1.set_title(f'After {f0} + {f1} Hz  and 20 Hz sinusoids')
        ax1.axis([0, __n, -2, 2])
#        sos = signal.ellip(12, 1, 1, 2, 'hp', fs=100, output='sos')
        filtered = self.FEllip(sig)
        ax2.plot(t, filtered)
        ax2.set_title(f' filtr ___/ 2 Hz high-pass filter')
        ax2.axis([0, __n, -3, 3])
        ax2.set_xlabel('Time [seconds]')
        plt.tight_layout()
        plt.show()


