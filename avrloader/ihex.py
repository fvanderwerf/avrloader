
import struct

class IntelHex:
    def __init__(self, input, image):
        self._input = input
        self._image = image

    def load(self):
        while True:
            line = self._input.readline()
            line = line.rstrip()

            if len(line) == 0:
                break

            if line[0] != ':':
                raise ValueError()

            binline = line[1:].decode("hex")
            cksum = 0;

            for byte in binline:
                cksum += ord(byte)

            cksum &= 0xFF

            if cksum != 0:
                raise ValueError('Intel Hex Checksum failed')

            reclen = struct.unpack('B', binline[0:1])[0]
            loadoffset = struct.unpack('>H', binline[1:3])[0]
            rectype = struct.unpack('B', binline[3:4])[0]
            data = binline[4:-1]

            if rectype == 1:
                break

            if len(data) != reclen:
                raise ValueError('Invalid record length')

            if rectype == 0:
                self._image.set(loadoffset, data)
        else:
            raise ValueError('Unexpected end of file')





