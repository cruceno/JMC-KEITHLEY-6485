

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

    def __init__(self, conn, address=None, model=None, id_number=None):

        self.conn = conn
        self.idn = self.dev.query('*IDN?')
        self.model = model if model else self.idn.split(',')[1]
        self.address = address if address else self.idn.split(',')[0]
        self.id_number = id_number if id_number else self.idn.split(',')[2]

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
