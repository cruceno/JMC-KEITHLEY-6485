from visa import ResourceManager
from .keithley import *
from .agilent import *

rm = ResourceManager('@py')


def list_scpi_devices(baud_rate=19200, debug=False):

    available_ports = rm.list_resources()
    devices = []
    for inst in available_ports:
        try:
            conn = rm.open_resource(inst)
            if inst.startswith('ASRL'):
                conn.baud_rate = baud_rate
            idn = conn.query('*IDN?')
            conn.close()
            dev = (inst, idn.split(',')[1], idn.split(',')[2])
            devices.append(dev)
        except Exception as e:
            if debug:
                print(str(e))
            else:
                pass
    return devices