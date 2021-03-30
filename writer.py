from smartcard.scard import *
import smartcard.util

WRITE = [0x00, 0xD6]
STARTMSB = [0x04] #change to where on the card you would like to write
STARTLSB = [0x07] #same here
MEM_L = [0x10]
DATA = [0x01]

cardservice.connection.connect()
apdu = READ + STARTMSB + STARTLSB + MEM_L + DATA
response1, sw1, sw2 = self.cardservice.connection.transmit( apdu )