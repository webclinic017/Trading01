import numpy as np
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap


class PlotGraph:

    def __init__(self):
        pass

    def Show(self):
        plt.show()

    def OnePlot(self, v, title):
        plt.figure()
        plt.title(title)
        plt.plot(v)
        plt.grid()
#        plt.show()

    def PlotN(self, dan:dict):
        fig, ax = plt.subplots(len(dan), 1, sharex=True)
        i=0
        for key, value in dan.items():
            ax[i].plot(value[0],value[1])
            ax[i].set_title(value[2])
            i=i+1
        kkk=1

    def Plot3xSpectr(self, mas):
        print(" ==-- Plot3xSpectr ")
        i, j = mas.shape
        x, y = np.meshgrid(np.arange(0, i, 1), np.arange(0, j, 1))
        fig = pylab.figure()
        fig.auto_add_to_figure=False
        axes = Axes3D(fig)

        axes.plot_surface(x, y, mas[x, y], rstride=3, cstride=3,
                          cmap=LinearSegmentedColormap.from_list("red_blue", ['b', 'w', 'r'], 128))
#        pylab.show()

    def makeData(self):
        x = np.arange(-10, 10, 0.1)
        y = np.arange(-10, 10, 0.1)
        xgrid, ygrid = np.meshgrid(x, y)

        zgrid = np.sin(xgrid) * np.sin(ygrid) / (xgrid * ygrid)
        return xgrid, ygrid, zgrid

    def Test3x(self):
        mm = self.FFTAll([1, 1, 1, ])
        _z = mm.shape
        x, y, z = self.makeData()

        fig = pylab.figure()
        axes = Axes3D(fig)

        axes.plot_surface(x, y, z, rstride=3, cstride=3,
                          cmap=LinearSegmentedColormap.from_list("red_blue", ['b', 'w', 'r'], 256))

        pylab.show()
