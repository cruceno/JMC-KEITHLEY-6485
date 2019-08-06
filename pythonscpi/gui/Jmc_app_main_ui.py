# Se importan los archivos generados por Pyside2-uic
import os
from .mainwindow import Ui_MainWindow

from PySide2.QtGui import (QIcon, QPixmap, QFont)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from pythonscpi.gui.MatplotLib_Pyside2 import PlotCanvas
from PySide2.QtWidgets import QVBoxLayout, QFileDialog
from PySide2.QtCore import Slot, QThread, Signal, SIGNAL
import numpy as np

class MainApp (Ui_MainWindow):

    def setupUi(self, app):
        super(MainApp, self).setupUi(app)
        # Generar los planos donde graficaremos los datos
        # Inicializar base de ploteo para mainplot


        font = QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        font.setWeight(50)
        font.setBold(False)
        app.setFont(font)
        icon = QIcon()
        icon.addPixmap(QPixmap("gui/images/logo-symbol-64x64.png"),
                       QIcon.Normal,
                       QIcon.Off
                       )
        app.setWindowIcon(icon)

    def load_cbx_data(self):
        pass

    @staticmethod
    def get_cbx_data(cbx):
        return cbx.itemData(cbx.currentIndex())

    def splash_message(self, message):
        self.emit(SIGNAL("splashUpdate(QString, int)"),
                  message,
                  132)

    @Slot()
    def change_messagge(self, message, duration=1000):
        self.statusbar.showMessage(message, duration)

    @staticmethod
    def change_widget_text_color(widget, r=255, g=255, b=255, a=100):
        widget.setStyleSheet("color: rgb({},{},{},{});".format(r, g, b, a))

    @staticmethod
    def widgetPlot(widget):
        widget.setLayout(QVBoxLayout())
        widget.canvas = PlotCanvas(widget, width=10, height=8)
        widget.toolbar = NavigationToolbar(widget.canvas, widget)
        widget.layout().addWidget(widget.toolbar)
        widget.layout().addWidget(widget.canvas)

