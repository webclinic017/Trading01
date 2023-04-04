#   https://devpractice.ru/matplotlib-lesson-5-1-mplot3d-toolkit/#p2

import numpy as np
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap


class Plot3D:
  def __init__(self):
    print("  ____ class 3D plot ____ ")

  def plot_mas(self, mas):
    print(" ==-- Plot3xSpectr ")
    mas = mas[:,:60]
    i, j = mas.shape
    x, y = np.meshgrid(np.arange(0, i, 1), np.arange(0, j, 1))
    fig = pylab.figure()
    fig.auto_add_to_figure=False
    axes = Axes3D(fig)

    axes.plot_surface(x, y, mas[x, y], rstride=3, cstride=3,
                          cmap=LinearSegmentedColormap.from_list("red_blue", ['b', 'w', 'r'], 128))
    pylab.show()


#     _dan_ij = mas.shape
#     x = np.linspace(0, _dan_ij[0], _dan_ij[0], endpoint=False)
#     y = np.linspace(0, _dan_ij[1], _dan_ij[1], endpoint=False)
# #    z = mas.tolist()
#
#     z[0] = mas[0, :].tolist()
# #    z = mas[:, :]
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     ax.plot(zdir=mas, label='parametric curve')
#     plt.show()

#     _dan_ij = mas.shape
#     x = np.linspace(0, _dan_ij[0], _dan_ij[0], endpoint=False)
#     y = np.linspace(0, _dan_ij[1], _dan_ij[1], endpoint=False)
# #    z = mas.tolist()
#
#     z[0] = mas[0, :].tolist()
# #    z = mas[:, :]
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     ax.plot(x, y, z, label='parametric curve')
#     plt.show()

    k=1


def test3dPlot():
  x = np.linspace(-np.pi, np.pi, 50)
  y = x
  z = np.cos(x)
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.plot(x, y, z, label='parametric curve')
  plt.show()

