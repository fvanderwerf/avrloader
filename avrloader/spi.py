
import time
import bitstring

class bitbangspi:
    def __init__(self, sck, mosi, miso):
        self._sck = sck
        self._mosi = mosi
        self._miso = miso

    def transmit(self, command):
        response = bitstring.BitArray()

        for bit in command:
            if bit:
                self._mosi.set()
            else:
                self._mosi.clear()
            self._sck.set()

            if self._miso.read():
                response.append('0b1')
            else:
                response.append('0b0')

            self._sck.clear()

        return response
