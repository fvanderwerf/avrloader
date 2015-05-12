
import serial

class LineCommand:
    def __init__(self, device):
        self._serial = serial.Serial(device, 19200, timeout = 1)
        self._onewline = '\r'
        self._inewline = '\n\r'

    def initialize(self):
        #empty read buffer
        if self._serial.inWaiting() > 0:
            self._serial.read(self._serial.inWaiting())

        self.command('')


    def command(self, command):
        cmd = command + self._onewline
        cmdecho = command + self._inewline

        #print 'command: "' + command + '" ' + ':'.join(x.encode('hex') for x in cmd)

        #empty receive buffer
        if self._serial.inWaiting() > 0:
            print('unexpected data in receive buffer ' + self._serial.read(self._serial.inWaiting()))

        self._serial.write(cmd)
        response = self.readresponse()

        if response[0:len(cmdecho)] == cmdecho:
            response = response[len(cmdecho):]
            response = response[:-2] if response[-2:] == self._inewline else response
            return response
        else:
            raise IOError('expected command to be echoed')



    def readresponse(self):
        response = ''

        while True:
            byte = self._serial.read()
            if len(byte) == 0:
                raise IOError('invalid response from Numato: ' + response)

            if byte[0] == '>':
                break

            response += byte

        #print ':'.join(x.encode('hex') for x in response)
        return response

class Numato:

    def __init__(self, line):
        self._line = line

    def version(self):
        return self._line.command('ver')

    def get_pin(self, index):
        return NumatoPin(self, index)

    def set(self, index):
        self._line.command('gpio set ' + str(index))

    def clear(self, index):
        self._line.command('gpio clear ' + str(index))

    def read(self, index):
        response = self._line.command('gpio read ' + str(index))
        return response[0] == '1'

class NumatoPin:

    def __init__(self, numato, index):
        self._numato = numato;
        self._index = index;

    def set(self):
        self._numato.set(self._index)

    def clear(self):
        self._numato.clear(self._index)

    def read(self):
        return self._numato.read(self._index)
        



