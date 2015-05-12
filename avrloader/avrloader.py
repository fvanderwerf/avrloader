#!/usr/bin/env python

import numato
import avr
import spi
import bitstring
import sys
import io
import ihex
import image
import pager

if __name__ == '__main__':

    hexfile = io.open(sys.argv[1], mode='r', encoding='ascii')
    image = image.BinImage()

    ihex = ihex.IntelHex(hexfile, image)
    ihex.load()
    image.dump()

    line = numato.LineCommand('/dev/ttyACM0')

    line.initialize()

    numato = numato.Numato(line)

    sck = numato.get_pin(0)
    mosi = numato.get_pin(1)
    miso = numato.get_pin(2)
    nreset = numato.get_pin(3)

    spi = spi.bitbangspi(sck, mosi, miso)

    avr = avr.avr(sck, nreset, spi)

    for x in xrange(10):
        avr.reset()
        if avr.program_enable():
            break
    else:
        raise IOError('AVR does not response to Program Enable instruction')

    print 'Connection established'

    signature = []
    signature.append(avr.read_signature_byte(0))
    signature.append(avr.read_signature_byte(1))
    signature.append(avr.read_signature_byte(2))

    if signature == ['\x1e', '\x91', '\x08']:
        print 'ATtiny25 detected'
    elif signature == ['\x1e', '\x92', '\x06']:
        print 'ATtiny45 detected'
    elif signature == ['\x1e', '\x93', '\x0B']:
        print 'ATtiny85 detected'
    else:
        raise IOError('Unrecognized AVR')

    avr.chip_erase()

    pager = pager.Pager(pagesize=64)

    for page in pager.pages(image.get_chunks()):
        address, data = page
        avr.load_page(data)
        avr.write_page(address)

