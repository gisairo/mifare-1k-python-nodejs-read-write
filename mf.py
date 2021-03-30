from smartcard.scard import *
import smartcard.util

# SELECT = [0xFF, 0x00, 0x00, 0x00, 0x00, 0x05, 0x0D4, 0x40, 0x30, 0x04]
SELECT = [0xFF, 0x00, 0x00, 0x00, 0x05, 0x0D4, 0x40, 0x01, 0x30, 0x04, 0x07]
# COMMAND = [0x00, 0x00, 0x00, 0x00]
COMMAND = [0xFF,0x86,0x00,0x00,0x05,0x01,0x00,0x04,0x60,0x00]


try:
    hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
    if hresult != SCARD_S_SUCCESS:
        raise Exception('Failed to establish context : ' +
            SCardGetErrorMessage(hresult))
    print 'Context established!'

    try:
        hresult, readers = SCardListReaders(hcontext, [])
        if hresult != SCARD_S_SUCCESS:
            raise Exception('Failed to list readers: ' +
                SCardGetErrorMessage(hresult))
        print 'PCSC Readers:', readers

        if len(readers) < 1:
            raise Exception('No smart card readers')

        reader = readers[0]
        print "Using reader:", reader

        try:
            hresult, hcard, dwActiveProtocol = SCardConnect(hcontext, reader,
                SCARD_SHARE_SHARED, SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
            if hresult != SCARD_S_SUCCESS:
                raise Exception('Unable to connect: ' +
                    SCardGetErrorMessage(hresult))
            print 'Connected with active protocol', dwActiveProtocol

            try:
                hresult, response = SCardTransmit(hcard, dwActiveProtocol,
                    SELECT)
                if hresult != SCARD_S_SUCCESS:
                    raise Exception('Failed to transmit: ' +
                        SCardGetErrorMessage(hresult))
                print 'Select: ' + smartcard.util.toHexString(response,
                    smartcard.util.HEX)
                hresult, response = SCardTransmit(hcard, dwActiveProtocol,
                    COMMAND)
                if hresult != SCARD_S_SUCCESS:
                    raise Exception('Failed to transmit: ' +
                        SCardGetErrorMessage(hresult))
                print 'Command: ' + smartcard.util.toHexString(response,
                    smartcard.util.HEX)
            finally:
                hresult = SCardDisconnect(hcard, SCARD_UNPOWER_CARD)
                if hresult != SCARD_S_SUCCESS:
                    raise Exception('Failed to disconnect: ' +
                        SCardGetErrorMessage(hresult))
                print 'Disconnected'

        except Exception, message:
            print "Exception:", message

    finally:
        hresult = SCardReleaseContext(hcontext)
        if hresult != SCARD_S_SUCCESS:
            raise Exception('Failed to release context: ' +
                    SCardGetErrorMessage(hresult))
        print 'Released context.'

except Exception, message:
    print "Exception:", message

import sys
if 'win32' == sys.platform:
    print 'press Enter to continue'
    sys.stdin.read(1)