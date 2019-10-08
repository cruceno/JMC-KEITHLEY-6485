import sys, os, time
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide2.QtCore import QThread, Signal, Slot, SIGNAL
from PySide2.QtCore import QMetaObject
from pythonscpi.gui.mainapp_gui import MainApp
import numpy as np
from pythonscpi.instruments.instrumets import rm
from pythonscpi.instruments.instrumets import list_scpi_devices
from pythonscpi.instruments.keithley import picoamperimeter6485
from pythonscpi.instruments.agilent import AG34410A


class Worker(QThread):

    msg = Signal(str)
    data = Signal(list)

    exiting = False
    outfile = None
    dev1 = None
    dev2 = None
    t = 30

    def __init__(self, ):
        QThread.__init__(self)

    def test(self, filename, dev1, dev2=None, duration=30):
        self.t = duration
        self.outfile = filename
        self.dev1 = dev1
        if dev2 is not None:
            self.dev2 = dev2
        else:
            self.dev2 = None
        if self.outfile is None:
            raise Exception('Falta ingresar el nombre del archivo de salida')
        else:
            self.start()

    def run(self):
        print(self.dev1)
        if self.dev1 is not None:
            print("Comienza medicion")
            time.sleep(3)
            start = time.time()
            t = 0
            timestamps = []
            self.dev1.connect()
            self.dev2.connect()
            # print(self.exiting)
            while not self.exiting and t < self.t:

                read_1 = self.dev1.read_value()
                val, timestamp = read_1.strip('\n').split(',')
                t = time.time() - start
                timestamps.append(t)
                # print(t, timestamp, val)
                data = [t, val]
                # print(data)
                if self.dev2 is not None:
                    read_2 = self.dev2.read_value()
                    val2 = read_2.strip('\n')
                    data.append(val2)

                fsock = open(self.outfile, 'a+')
                fsock.write('\t'.join(str(x) for x in data) + '\n')
                fsock.close()
                self.data.emit(data)

            # print("terminando")
            self.dev1.disconnect()
            self.dev2.disconnect()


class JMC_Python_SCPI(QMainWindow, MainApp):

    def __init__(self):
        super(JMC_Python_SCPI, self).__init__()
        self.setupUi(self)
        self.main_dev = None
        self.aux_dev = None
        self.worker = Worker()
        self.thread = QThread()
        self.connect_worker()

        self.cbx_main_range.addItem("AUTO", "AUTO")
        for key, value in picoamperimeter6485.RANGES.items():
            self.cbx_main_range.addItem(value, key)
        self.load_cbx_data()

        self.get_devices()
        if self.main_dev is not None:
            self.init_6485()
            self.on_chk_zero_corr_stateChanged(0)
        if self.aux_dev is not None:
            self.on_cbx_aux_range_currentIndexChanged(0)

    def connect_worker(self):
        self.connect(self.thread,
                     SIGNAL('started()'),
                     self.worker.start)
        self.connect(self.worker,
                     SIGNAL('finished()'),
                     self.thread.quit)

        self.connect(self.worker,
                     SIGNAL('finished()'),
                     self.finished_process)
        self.worker.data.connect(self.incoming_data)
        self.worker.msg.connect(self.change_messagge)

        self.worker.moveToThread(self.thread)

    def get_devices(self):
        devices = list_scpi_devices()
        for dev in devices:
            if dev[2] == '4031608':
                self.cbx_main_port.addItem(dev[1], dev[0])
                self.main_dev = picoamperimeter6485(address=dev[0])
            else:
                self.cbx_aux_port.addItem(dev[1], dev[0])
                self.aux_dev = AG34410A(address=dev[0])

    def init_6485(self):
        self.main_dev.connect()
        self.main_dev.write('*RST')
        time.sleep(2)
        self.main_dev.run_cmd('CONF:CURR')
        self.main_dev.run_cmd('ARM:COUN 1')
        self.main_dev.run_cmd('FORM:ELEM READ,TIME')
        self.main_dev.run_cmd('SYST:LFR:AUTO ON')
        self.main_dev.disconnect()

    @Slot(list)
    def incoming_data(self, data):
        amperes = data[1]
        elapsed_time = data[0]
        volt = data[2]
        self.lb_num_amp.setText(amperes)
        self.lb_num_volt.setText(volt)
        self.lb_num_time.setText("{0:.1f}".format(elapsed_time))
        self.pb_reading.setValue(int(elapsed_time))
        self.plot_data()

    def plot_data(self):
        x, y, y2= np.genfromtxt(self.lb_output_file.text(),
                             usecols=(0,1,2),
                             unpack=True)
        self.fr_main_plot.canvas.plot(x, y, y2=y2)

    @Slot()
    def on_pb_run_clicked(self):
        self.pb_run.setEnabled(False)
        if self.pb_run.text() == "Run":
            self.disable_ui_controls(False)
            filename = "".join(QFileDialog.getSaveFileName(self,
                                               "Guardar medicion",
                                               os.path.expanduser('~'),
                                               '.dat')
                           )
            self.lb_output_file.setText(filename)
            if filename and self.main_dev is not None:
                f = open(filename, 'w')
                f.close()

                self.worker.test(filename,
                                 self.main_dev,
                                 dev2=self.aux_dev,
                                 duration=self.sb_run_time.value()
                                 )
                self.pb_run.setText("Stop")
                self.pb_run.setEnabled(True)
            else:
                self.print_to_pte("Operacion cancelada")
                self.set_process_info()
                self.pb_run.setEnabled(True)

        elif self.pb_run.text() == "Stop":
            self.pb_run.setEnabled(False)
            self.worker.exiting = True
            while self.worker.isRunning():
                self.pb_run.setText("Cancelando ...")
                time.sleep(0.2)
            self.pb_reading.setValue(0)
            self.pb_run.setText("Run")
            self.disable_ui_controls(True)
            self.pb_run.setEnabled(True)

    @Slot()
    def finished_process(self):
        self.pb_run.setText("Run")
        self.pb_reading.setValue(0)
        self.set_process_info()
        self.disable_ui_controls(True)
        self.pb_run.setEnabled(True)

    @Slot(int)
    def on_sb_run_time_valueChanged(self, value):
        self.pb_reading.setMaximum(value)

    @Slot()
    def on_pb_zchk_pressed(self):
        self.pb_zchk.setEnabled(False)
        if self.pb_zchk.text().startswith("Enable"):
            self.main_dev.enable_zchk(True)
            self.print_to_pte("Zero check enabled on 6485")
            self.pb_zchk.setText("Disable ZERO CHECK")
        else:
            self.main_dev.enable_zchk(False)
            self.print_to_pte("Zero check disabled on 6485")
            self.pb_zchk.setText("Enable ZERO CHECK")
        self.pb_zchk.setEnabled(True)

    @Slot(int)
    def on_chk_median_stateChanged(self, state):
        if state > 0:
            self.cbx_median_rank.setEnabled(True)
            self.main_dev.enable_median(True)
        else:
            self.cbx_median_rank.setEnabled(False)
            self.main_dev.enable_median(False)

    @Slot(int)
    def on_chk_zero_corr_stateChanged(self, state):
        if state > 0:
            self.pb_zero.setEnabled(True)
            if self.main_dev is not None:
                self.main_dev.enable_zcorr(True)
        else:
            self.pb_zero.setEnabled(False)
            if self.main_dev is not None:
                self.main_dev.enable_zcorr(False)

    @Slot()
    def on_pb_zero_pressed(self):
        self.pb_zero.setEnabled(False)
        if self.main_dev is not None:
            zero = self.main_dev.zero()
            self.print_to_pte('Nuevo zero : {}'.format(zero))
            self.lb_num_zero.setText(zero.split(',')[0])
        self.pb_zero.setEnabled(True)

    @Slot(int)
    def on_cbx_main_range_currentIndexChanged(self, index):
        range = self.cbx_main_range.itemData(index)
        if self.main_dev is not None:
            self.print_to_pte(self.main_dev.set_range(range))

    @Slot(int)
    def on_cbx_aux_range_currentIndexChanged(self, index):
        range = self.cbx_aux_range.itemData(index)
        if self.aux_dev is not None:
            self.print_to_pte(self.aux_dev.set_range(range))
    @Slot(int)
    def on_cbx_aver_type_currentIndexChanged(self, index):
        type = self.cbx_aver_type.itemData(index)
        if self.main_dev is not None:
            self.print_to_pte(self.main_dev.set_aver_type(type))

    @Slot(int)
    def on_cbx_aver_class_currentIndexChanged(self, index):
        state = self.cbx_aver_class.itemData(index)
        if self.main_dev is not None:
            self.print_to_pte(self.main_dev.enable_adv(state))

    @Slot(int)
    def on_sb_aver_count_valueChanged(self, value):
        if self.main_dev is not None:
            self.print_to_pte(self.main_dev.set_aver_count(value))

    @Slot(int)
    def on_cbx_main_speed_currentIndexChanged(self, index):
        speed = self.cbx_main_speed.itemData(index)
        if self.main_dev is not None:
            self.print_to_pte(self.main_dev.set_nplc(speed))

    def disable_ui_controls(self, state):
        self.gb_ui_control.setEnabled(state)

    def set_process_info(self):
        f = open(self.lb_output_file.text(), 'r')
        data = f.read()
        f.close()
        f = open(self.lb_output_file.text(), 'w')

        info = []
        info.append("Picoammeter: {}".format(self.cbx_main_port.currentText()))
        info.append("Range: {}".format(self.cbx_main_range.currentText()))
        info.append("Speed: {}".format(self.cbx_main_speed.currentText()))
        info.append("Average: {}".format(self.chk_average.checkState()))
        info.append("Average Type: {}".format(self.cbx_aver_type.currentText()))
        info.append("Average Class: {}".format(self.cbx_aver_class.currentText()))
        info.append("Average count: {}".format(self.sb_aver_count.text()))
        info.append("Median Filter: {}".format(self.cbx_median_rank.currentText()))
        info.append("Zero Correction: {}".format(self.chk_zero_corr.checkState()))
        info.append("Zero Value: {}".format(self.lb_num_zero.text()))
        info.append("Multimeter: {}".format(self.cbx_aux_port.currentText()))
        info.append("Multimeter range: {}".format(self.cbx_aux_range.currentText()))
        info.append("Multimeter speed: {}".format(self.cbx_aux_speed.currentText()))
        info.append("Test duration: {}".format(self.sb_run_time.text()))

        for line in info:
            f.write(line+'\n')
        f.write('\n')
        f.write(data)
        f.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    JMCapp = JMC_Python_SCPI()
    JMCapp.show()
    sys.exit(app.exec_())