'''
Created on 6 abr. 2017

@author: cruce
'''

# Librerias para graficar en el ploter
import matplotlib; matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class canvas(FigureCanvas):

    def __init__(self, parent):
        # Se instancia el objeto figure
        self.fig = Figure()
        self.fig.patch.set_facecolor('xkcd:charcoal grey')
        # Se define la grafica en coordenadas polares
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('xkcd:black')
        # Se define una grilla
        self.axes.grid(color='xkcd:mint green', linestyle='--', linewidth=0.2, visible=True)
        # se inicializa FigureCanvas
        FigureCanvas.__init__(self, self.fig)

        # se define el widget padre
        self.setParent(parent)
        self.fig.canvas.draw()

    def reload(self):
        self.axes.cla()
        # Se define una grilla
        self.axes.grid(True)

    def plot(self, x, y):

        # Dibujar Curva
        self.reload()
        self.axes.plot(x, y, 'ob')
        self.fig.canvas.draw()


class NavigationToolbar(NavigationToolbar):
    pass
