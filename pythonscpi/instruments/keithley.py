from pyvisa import ResourceManager
from pyvisa.errors import InvalidSession
rm = ResourceManager('@py')


class picoamperimeter6485():

    RANGES = {
        2e-2: "20 mA",
        2e-3: "2 mA",
        2e-4: "200 \u03BCA",
        2e-5: "20 \u03BCA",
        2e-6: "2 \u03BCA",
        2e-7: "200 nA",
        2e-8: "20 nA",
        2e-9: "2 nA"
        }

    def __init__(self, address=None, model=None, id_number=None, baud_rate=19200):

        self.conn = None
        self.model = model
        self.address = address
        self.id_number = id_number
        self.baud_rate = baud_rate

    def connect(self):
        if self.address is not None:
            if self.conn is not None and self.is_connected():
                pass
            else:
                self.conn = rm.open_resource(self.address)
                self.conn.baud_rate = self.baud_rate
        else:
            raise Exception("Set address property first")

    def is_connected(self):
        try:
            if self.conn.session:
                return True

        except InvalidSession:
            return False

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()

    def check_scpi_error(self):
        return self.query('SYST:ERR?')

    def write(self, text):
        self.conn.write(text)

    def read(self):
        return self.conn.read()

    def query(self, text):
        return self.conn.query(text)

    def run_cmd(self, cmd):
        self.connect()
        self.write(cmd)
        err = self.check_scpi_error()
        self.disconnect()
        return "{}, {}".format(cmd, err)

    def init_measure(self):
        self.write('INIT')

    def enable_zchk(self, state):
        self.connect()
        if state:
            self.write('SYST:ZCH ON')
        else:
            self.write('SYST:ZCH OFF')
        self.disconnect()

    def enable_median(self, state):
        self.connect()
        if state:
            self.write('SENS:MED ON')
        else:
            self.write('SENS:MED OFF')
        self.disconnect()

    def set_median_rank(self, rank):
        self.connect()
        if 1 <= rank <= 5:
            self.write('SENS:MED:RANK {}'.format(rank))
        else:
            raise Exception("Invalid range")
        self.disconnect()

    def enable_zcorr(self, state):
        self.connect()
        if state:
            self.write('SYST:ZCOR ON')
        else:
            self.write('SYST:ZCOR OFF')
        self.disconnect()

    def set_range(self, range):
        if range == "AUTO":
            cmd = 'CURR:RANG:{} 1'.format(range)
        else:
            cmd = 'CURR:RANG {}'.format(range)
        return self.run_cmd(cmd)

    def enable_aver(self, state):
        cmd = 'SENS:AVER {}'.format(str(state))
        return self.run_cmd(cmd)

    def enable_adv(self, state):
        self.connect()
        self.write('SENS:AVER:ADV {}'.format(str(state)))
        err = self.check_scpi_error()
        self.disconnect()
        return 'SENS:AVER:ADV {}, {}'.format(str(state), err)

    def set_aver_type(self, type):
        self.connect()
        self.write('SENS:AVER:TCONtrol {}'.format(type))
        err = self.check_scpi_error()
        self.disconnect()
        return 'SENS:AVER:TCONtrol {}, {}'.format(type, err)

    def set_aver_count(self, count):
        self.connect()
        self.write('SENS:AVER:COUNt {}'.format(str(count)))
        err = self.check_scpi_error()
        self.disconnect()
        return 'SENS:AVER:COUNt {}, {}'.format(str(count), err)

    def set_nplc(self, value):
        cmd = 'SENS:CURR:NPLC {}'.format(value)
        return self.run_cmd(cmd)

    def zero(self):
        self.connect()
        self.write('SYST:ZCOR OFF')
        print(self.check_scpi_error())
        self.write('SYST:ZCH ON')
        print(self.check_scpi_error())
        zero = self.query('READ?')
        print(self.check_scpi_error())
        self.write('SYST:ZCOR:ACQ')
        print(self.check_scpi_error())
        self.write('SYST:ZCH OFF')
        print(self.check_scpi_error())
        self.write('SYST:ZCOR ON')
        print(self.check_scpi_error())
        self.disconnect()
        return zero

    def read_value(self):
        return self.query('READ?')


