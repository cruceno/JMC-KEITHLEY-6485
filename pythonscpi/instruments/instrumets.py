

class Picoamperimeter():

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

    def __init__(self, serial):
        self.conn = serial

    def check_scpi_error(self):
        self.conn.write(b'SYST:ERR?\n')
        print(self.conn.readline())

    def write(self, text):
        self.conn.write(text)

    def init_measure(self):
        self.conn.write(b'INIT')

