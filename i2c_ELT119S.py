#!/usr/bin/env python
#       filename: i2c_ELT119S.py
#       desc: i2c demonstration for ELT119S Display
#       requirements for i2c operation must be completed before running this

from smbus import SMBus
import time

i2caddress = 0x20  # Address of display driver
cmd_alloff = 0x19
cmd_allon  = 0x1A
cmd_setseg = 0x01
cmd_setbrt = 0x02

def cksum(ckdat):
""" Return XOR checksum of data in list """
        c = 0
        for x in ckdat:
                c = c ^ x
        return c

def dispwrite(dispbus, dispcmd, dispdata):
""" Send i2c command plus data """
        outbuff = [len(dispdata)+3]+dispdata
        outbuff.append(cksum([dispcmd]+outbuff))
        dispbus.write_i2c_block_data(i2caddress, dispcmd, outbuff)

def setbits(dbytes, sbits):
""" Takes a list of bytes with the bit number to set, returns list of bytes with bit or'd."""
    b = sbits % 8
    d = sbits // 8
    for i, item in enumerate(dbytes):
        if i == d:
            dbytes[i] |= 2**b
    return dbytes

def main():
""" cycle through all 119 segments at max brightness """
        i2cbus = SMBus(1)  # Create a new I2C bus

        dispwrite(i2cbus, cmd_setbrt, [2,10,0])

        for j in range(119):
                dispwrite(i2cbus, cmd_setseg, setbits([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], j))
                time.sleep(.1)
        dispwrite(i2cbus, cmd_setseg, [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

#############################################################################

if __name__ == "__main__":
    main()
