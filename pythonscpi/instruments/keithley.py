

class picoamperimeter6485():

    _RANGES = {
        2e-2: "20 mA",
        2e-3: "2 mA",
        2e-4: "200 \u03BCA",
        2e-5: "20 \u03BCA",
        2e-6: "2 \u03BCA",
        2e-7: "200 nA",
        2e-8: "20 nA",
        2e-9: "2 nA"
        }

    def __init__(self, conn, connn_type='visa'):
        self.conn = conn

    def check_scpi_error(self):
        self.conn.query('SYST:ERR?')

    def write(self, text):
        self.conn.write(text)

    def init_measure(self):
        self.conn.write('INIT')

    def read_value(self):
        return self.conn.query('READ?')

    def read(self):
        return self.conn.read()
