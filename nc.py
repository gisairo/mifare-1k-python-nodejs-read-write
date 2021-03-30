
import pcsclite
import binascii

# SELECT = "\xFF\x00\x00\x00\x00\x00\x05\x00\x0D4\x40\x30\x04\x07"
SELECT = "\xFF\x00\x00\x00\x05\x0D4\x40\x01\x30\x04\x07"
COMMAND = "\xFF,\x86,\x00,\x00,\x05,\x01,\x00,\x04,\x60,\x00"

try:
    context = pcsclite.Context()
    readers = context.list_readers()
    print "PCSC readers:", readers
    reader = readers[0]
    print "Using reader:", reader

    card = context.connect(reader)

    data = card.transmit(SELECT)
    print "SELECT"
    print binascii.b2a_hex(data)

    print "COMMAND"
    data = card.transmit(COMMAND)
    print "----"
    print data
    print "---"
    hexval = binascii.b2a_hex(data)
    print hexval

    # print hexval.hex()

    card.disconnect()

    del card
    del context

except Exception, message:
    print "Exception:", message