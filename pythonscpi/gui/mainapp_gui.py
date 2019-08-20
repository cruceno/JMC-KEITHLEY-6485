# Se importan los archivos generados por Pyside2-uic
from .mainwindow import Ui_MainWindow
from PySide2.QtGui import (QIcon, QPixmap, QFont)
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtCore import SIGNAL, Slot
from pythonscpi.ploter.QtMatplotLibPlot import canvas, NavigationToolbar


class MainApp (Ui_MainWindow):

    def setupUi(self, app):

        super(MainApp, self).setupUi(self)
        self.widgetPlot(self.fr_main_plot)

        # app.lb_kn_force.setStyleSheet("color: rgb(85, 255, 127);")
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
        widget.canvas = canvas(widget)
        widget.toolbar = NavigationToolbar(widget.canvas, widget)
        widget.layout().addWidget(widget.toolbar)
        widget.layout().addWidget(widget.canvas)