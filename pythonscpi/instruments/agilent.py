from pyvisa import ResourceManager
from pyvisa.errors import InvalidSession
rm = ResourceManager('@py')


class AG34410A():
    '''
    classdocs
    '''
    def __init__(self, conn=None, address=None, model=None, id_number=None):
        '''
        Constructor
        '''

        self.conn = conn
        self.model = model
        self.address = address
        self.id_number = id_number
        self.message = True

    def connect(self):
        if self.address is not None:
            if self.conn is not None and self.is_connected():
                pass
            else:
                self.conn = rm.open_resource(self.address)
        else:
            raise Exception("Set address property first")

    def check_scpi_error(self):
        return self.query('SYST:ERR?')

    def run_cmd(self, cmd):
        self.connect()
        self.write(cmd)
        err = self.check_scpi_error()
        self.disconnect()
        return "{}, {}".format(cmd, err)

    def is_connected(self):
        try:
            if self.conn.session:
                return True

        except InvalidSession:
            return False

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()

    def write(self, text):
        self.conn.write(text)

    def read(self):
        return self.conn.read()

    def query(self, text):
        return self.conn.query(text)

    def temperature_calibration(self, temp_data):
    #           Pasar de milivoltios a gracdos centigrado el valor leido por el multimetro
        # Polinomio para rango intermedio  -272 a 150 C

        if temp_data < 2: 
            
            Y = 25.39459 * temp_data 
            Y-= 0.44494 * temp_data ** 2 
            Y+= 0.05652 * temp_data ** 3 
            Y-= 0.00412 * temp_data ** 4 
            Y+= 0.0011 * temp_data ** 5 
            Y-= 1.39776E-4 * temp_data ** 6 
            Y+= 4.40583E-6 * temp_data ** 7 
            Y+= 7.709E-8 * temp_data ** 8
            
        #Polinomio para rango positivo 0 a 500 C     
        if temp_data >=2 :
            
            Y = 25.26032 * temp_data
            Y-= 0.57128 * temp_data ** 2
            Y+= 0.13393 * temp_data ** 3
            Y-= 0.01411 * temp_data ** 4
            Y+= 7.7329E-4 * temp_data ** 5
            Y-= 2.32438E-5 * temp_data ** 6
            Y+= 3.64924E-7 * temp_data ** 7
            Y-= 2.34283E-9 * temp_data ** 8
            
        return Y

    def set_range(self, range):
        if range == "AUTO":
            cmd = 'SENS:VOLT:DC:RANG:{} 1'.format(range)
        else:
            cmd = 'SENS:VOLT:DC:RANG {}'.format(range)
        return self.run_cmd(cmd)

    def read_value(self):
        return self.query('READ?')