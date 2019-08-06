import serial
import time
import matplotlib.pyplot as plt

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


ser = serial.Serial('/dev/ttyUSB0',
                    baudrate=19200,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    timeout=120
                    )
dev = Picoamperimeter(ser)

dev.check_scpi_error()
# dev.write(b'*RST\n')
# dev.conn.write(b'CONF:CURR')

# Proceso de correccion de zero
dev.conn.write(b'SYST:ZCH ON\n') # Zero check
dev.check_scpi_error()
time.sleep(1)

dev.conn.write(b'SENS:MED ON\n') # Activa mediana
dev.check_scpi_error()
time.sleep(1)
dev.conn.write(b'SENS:AVER:ADV ON\n')
dev.check_scpi_error()
time.sleep(1)
dev.conn.write(b'CURR:RANG 2e-9\n')
dev.check_scpi_error()
time.sleep(1)
dev.write(b'SENS:CURR:NPLC 6\n')
dev.check_scpi_error()
time.sleep(1)
dev.write(b'ARM:COUN 1\n')
dev.check_scpi_error()
time.sleep(1)
dev.conn.write(b'INIT\n')
dev.check_scpi_error()
time.sleep(1)

dev.conn.write(b'SYST:ZCOR:ACQ\n')
dev.check_scpi_error()
time.sleep(1)
dev.conn.write(b'SYST:ZCOR ON\n')
dev.check_scpi_error()
time.sleep(1)

# Conectar fuente de señal antes de seguir.
dev.conn.write(b'SYST:ZCH OFF\n')
dev.check_scpi_error()
time.sleep(1)
#Cantidad de mediciones por adquisicion.


# dev.write(b'ARM:SOUR IMM')
dev.conn.write(b'CURR:RANG:AUTO 1\n')
dev.check_scpi_error()
time.sleep(1)
#TODO: Calcular datos por segundo segun velocidad de adquisicion y filtros utilizados
# samples = 100
# dev.write('ARM:COUN {}\n'.format(str(samples)).encode())
# dev.check_scpi_error()
# time.sleep(1)

dev.write(b'FORM:ELEM READ,TIME\n')
dev.check_scpi_error()

print("Comienza medicion")
time.sleep(3)
start = time.time()
t = 0
timestamps = []
values = []
while t <= 180:
    dev.conn.write(b'READ?\n')

    read = dev.conn.readline().decode()
    t = time.time() - start
    val, timestamp = read.strip('\n').split(',')

    timestamps.append(t)
    values.append(val)

    print(t, timestamp, val)

# measure = dev.conn.read_until(terminator=b'\n').decode().split(',')
# dev.conn.write(b'SYST:ZCH ON\n')
# values = slice(0, samples, 2)
# timestamps = slice(1, samples+1, 2)
# values = measure[values]
# timestamps = measure[timestamps]
# start = float(timestamps[0])

timestamps = [float(v) for v in timestamps]
values = [float(val) for val in values]
# print(timestamps, values)
print(timestamps, values)
f = open('medicion.dat', 'w')
lines = []
for t, v in zip(timestamps, values):
    lines.append("{}\t{}".format(t,v))
f.write("\n".join(lines))

plt.plot(timestamps, values)
plt.show()
