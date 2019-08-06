# Se importan los archivos generados por Pyside2-uic
from .mainwindow import Ui_MainWindow
from PySide2.QtGui import (QIcon, QPixmap, QFont)
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtCore import SIGNAL, Slot


class MainApp (Ui_MainWindow):

    def setupUi(self, jmc_prensa_daq):

        super(MainApp, self).setupUi(jmc_prensa_daq)

        # Cargar datos en los desplegables que configuran el tipo
        # de sensor y los decimales a mostrar.

        # Generar los planos donde graficaremos los datos
        # Inicializar base de ploteo para mainplot
        jmc_prensa_daq.vbl_presure_plot = QVBoxLayout(jmc_prensa_daq.plot_e_p)
        jmc_prensa_daq.presure_canvas = canvas(jmc_prensa_daq.plot_e_p)
        # jmc_prensa_daq.presure_tlb = NavigationToolbar(jmc_prensa_daq.presure_canvas,
        #                                      jmc_prensa_daq.plot_e_p)
        jmc_prensa_daq.vbl_presure_plot.insertWidget(0, jmc_prensa_daq.presure_canvas)
        # jmc_prensa_daq.vbl_presure_plot.insertWidget(1, jmc_prensa_daq.presure_tlb)

        jmc_prensa_daq.vbl_displacement_plot = QVBoxLayout(jmc_prensa_daq.plot_e_d)
        jmc_prensa_daq.displacement_canvas = canvas(jmc_prensa_daq.plot_e_d)
        # jmc_prensa_daq.displacement_tlb = NavigationToolbar(jmc_prensa_daq.displacement_canvas,
        #                                           jmc_prensa_daq.plot_e_d)
        jmc_prensa_daq.vbl_displacement_plot.insertWidget(0, jmc_prensa_daq.displacement_canvas)
        # jmc_prensa_daq.vbl_displacement_plot.insertWidget(1, jmc_prensa_daq.displacement_tlb)

        jmc_prensa_daq.fe_vbl_presure_plot = QVBoxLayout(jmc_prensa_daq.plot_v_p)
        jmc_prensa_daq.fe_presure_canvas = canvas(jmc_prensa_daq.plot_v_p)
        jmc_prensa_daq.fe_presure_tlb = NavigationToolbar(jmc_prensa_daq.fe_presure_canvas,
                                                jmc_prensa_daq.plot_v_p)
        jmc_prensa_daq.fe_vbl_presure_plot.insertWidget(0, jmc_prensa_daq.fe_presure_canvas)
        jmc_prensa_daq.fe_vbl_presure_plot.insertWidget(1, jmc_prensa_daq.fe_presure_tlb)

        jmc_prensa_daq.fe_vbl_displacement_plot = QVBoxLayout(jmc_prensa_daq.plot_v_d)
        jmc_prensa_daq.fe_displacement_canvas = canvas(jmc_prensa_daq.plot_v_d)
        jmc_prensa_daq.fe_displacement_tlb = NavigationToolbar(jmc_prensa_daq.fe_displacement_canvas,
                                                     jmc_prensa_daq.plot_v_d)
        jmc_prensa_daq.fe_vbl_displacement_plot.insertWidget(0, jmc_prensa_daq.fe_displacement_canvas)
        jmc_prensa_daq.fe_vbl_displacement_plot.insertWidget(1, jmc_prensa_daq.fe_displacement_tlb)

        # jmc_prensa_daq.lb_tn_force.setEnabled(True)
        # jmc_prensa_daq.lb_kn_force.setStyleSheet("color: rgb(85, 255, 127);")
        font = QFont()
        font.setFamily("Exo 2")
        font.setPointSize(12)
        font.setWeight(50)
        font.setBold(False)
        jmc_prensa_daq.setFont(font)

        icon = QIcon()
        icon.addPixmap(QPixmap("gui/images/logo-symbol-64x64.png"),
                       QIcon.Normal,
                       QIcon.Off
                       )
        jmc_prensa_daq.setWindowIcon(icon)

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
