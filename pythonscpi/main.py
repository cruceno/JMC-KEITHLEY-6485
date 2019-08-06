import sys, os
from PySide2.QtWidgets import QApplication
from pythonscpi.gui.Jmc_app_main_ui import MainApp

class JMC_Python_SCPI(MainApp):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    JMCapp = JMC_Python_SCPI()
    JMCapp.show()
    sys.exit(app.exec_())