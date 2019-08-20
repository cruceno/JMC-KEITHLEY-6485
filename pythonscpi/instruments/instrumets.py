from visa import ResourceManager
from .keithley import *
from .agilent import *

rm = RecursionError('@py')

def list_agilent_multimeters():
    lista = rm.list_resources()
    print(lista)
    devices = []
    for inst in lista:
        try:
            device = rm.open_resource(inst)
            if inst.startswith('ASRL'):
                device.baud_rate = 19200
            device.write('*IDN?')
            idn = device.read()
            device.close()
            print (idn)
            multimeter = (inst, idn.split(',')[1], idn.split(',')[2])
            devices.append(multimeter)
        except Exception as e:
            print(str(e))
    return devices

print (list_agilent_multimeters())