
import time
import bitstring

class avr:
    def __init__(self, sck, nreset, spi):
        self._sck = sck
        self._nreset = nreset;
        self._spi = spi

    def reset(self):
        self._sck.clear()
        time.sleep(0.1)

        self._nreset.set()
        time.sleep(0.01)
        self._nreset.clear()
        time.sleep(0.05)

    def program_enable(self):
        response = self._spi.transmit(bitstring.BitArray(hex='ac530000'))
        return response[16:] == "0x5300"

    def read_signature_byte(self, index):
        command = bitstring.BitStream('0x3000, 0b000000, uint:2=' + str(index) +  ', 0x00')

        response = self._spi.transmit(command)

        return response[24:].tobytes()

    def chip_erase(self):
        print "chip_erase"
        self._spi.transmit(bitstring.BitArray('0xac800000'))
        time.sleep(0.01)


    def load_page(self, data):
        print "load_page " + data.encode('hex')

        for i in xrange(32):
            command = bitstring.BitStream('0x40, uint:16=' + str(i) + ', uint:8=' + str(ord(data[i * 2])))
            self._spi.transmit(command)
            command = bitstring.BitStream('0x48, uint:16=' + str(i) + ', uint:8=' + str(ord(data[i * 2 + 1])))
            self._spi.transmit(command)

    def write_page(self, address):
        print "write page " + str(address/2)
        command = bitstring.BitStream('0x4c, uint:16=' + str(address/2) + ', 0x00')
        self._spi.transmit(command)
        time.sleep(0.010)
