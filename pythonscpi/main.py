import sys, os
from PySide2.QtWidgets import QApplication, QMainWindow

from pythonscpi.gui.mainapp_gui import MainApp


class JMC_Python_SCPI(QMainWindow, MainApp):
    def __init__(self):
        super(JMC_Python_SCPI, self).__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    JMCapp = JMC_Python_SCPI()
    JMCapp.show()
    sys.exit(app.exec_())