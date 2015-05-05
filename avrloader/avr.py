
import time

class avr:
    def __init__(self, sck, nreset):
        self._sck = sck
        self._nreset = nreset;

    def reset(self):
        self._sck.clear()
        time.sleep(1)

        self._nreset.set()
        time.sleep(1)
        self._nreset.clear()

