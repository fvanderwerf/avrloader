#!/usr/bin/env python

import serial
import time
import numato
import avr
import spi
import bitstring

if __name__ == '__main__':

    line = numato.LineCommand('/dev/ttyACM0')

    line.initialize()

    numato = numato.Numato(line)

    sck = numato.get_pin(0)
    mosi = numato.get_pin(1)
    miso = numato.get_pin(2)
    nreset = numato.get_pin(3)

    avr = avr.avr(sck, nreset)


    print ("RESET")
    avr.reset()

    print ("Program Enable")
    spi = spi.bitbangspi(sck, mosi, miso)

    response = spi.transmit(bitstring.BitArray(hex='ac530000'))
    print response



