import sys, os, time
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QThread, Signal, Slot
from pythonscpi.gui.mainapp_gui import MainApp
from pythonscpi.instruments.instrumets import list_scpi_devices, rm


class Worker(QThread):
    msg = Signal(str)
    data = Signal(list)
    exiting = False

    def __init__(self):
        super(Worker, self).__init__()
        self.dev2 = None
        self.dev1 = None

    def test(self, dev1, time, dev2=None):
        
        self.t = time
        self.dev1 = rm.open_resource(dev1)
        if dev2 is not None:
            self.dev2 = rm.open_resource(dev2)
        else:
            self.dev2 = None
        
        self.start()

    def run(self):
        if self.dev1 is not None:
            print("Comienza medicion")
            time.sleep(3)
            start = time.time()
            t = 0
            timestamps = []
            values = []
            while not self.exiting and t < self.t:
                read = self.dev1.query('READ?')
                t = time.time() - start
                val, timestamp = read.strip('\n').split(',')
                timestamps.append(t)
                values.append(val)
                print(t, timestamp, val)
                self.data.emit([t, timestamp, val])


class JMC_Python_SCPI(QMainWindow, MainApp):
    def __init__(self):
        super(JMC_Python_SCPI, self).__init__()
        self.setupUi(self)
        self.get_devices()
        self.init_6485()


    def get_devices(self):
        devices = list_scpi_devices()
        for dev in devices:
            if dev[2] == '4031608':
                self.cbx_main_port.addItem(dev[1], dev[0])
            else:
                self.cbx_aux_port.addItem(dev[1], dev[0])

    def init_6485(self):

        dev = rm.open_resource(self.get_cbx_data(self.cbx_main_port))
        dev.baud_rate = 19200
        # dev.write(b'*RST\n')
        # dev.conn.write(b'CONF:CURR')
        # Proceso de correccion de zero
        dev.write('SYST:ZCH ON')  # Zero check
        # time.sleep(1)
        dev.write('SENS:MED ON')  # Activa mediana
        # time.sleep(1)
        dev.write('SENS:AVER:ADV ON')
        # time.sleep(1)
        dev.write('CURR:RANG 2e-9')
        # time.sleep(1)
        dev.write('SENS:CURR:NPLC 6')
        # time.sleep(1)
        dev.write('ARM:COUN 1')
        # time.sleep(1)
        dev.write('INIT')
        # time.sleep(1)
        dev.write('SYST:ZCOR:ACQ')
        # time.sleep(1)
        dev.write('SYST:ZCOR ON')
        # time.sleep(1)
        # Conectar fuente de señal antes de seguir.
        dev.write('SYST:ZCH OFF')
        # time.sleep(1)
        dev.write('CURR:RANG:AUTO 1')
        # time.sleep(1)
        dev.write('FORM:ELEM READ,TIME')
        # time.sleep(1)
        dev.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    JMCapp = JMC_Python_SCPI()
    JMCapp.show()
    sys.exit(app.exec_())