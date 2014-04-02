"""
PyRfid

Requirements:
~# apt-get install python-serial

@see http://www.seeedstudio.com/wiki/index.php?title=Electronic_brick_-_125Khz_RFID_Card_Reader#Demo_code
@see https://github.com/johannrichard/SeeedRFIDLib/blob/master/SeeedRFIDLib.cpp

Copyright 2014 Philipp Meisberger (PM Code Works).
All rights reserved. 
"""

import utilities
import serial
import os

class PyRfid(object):
    """
    A python written library for an 125kHz RFID reader.

    Flag for RFID connection start.
    @var hex RFID_STARTCODE

    Flag for RFID connection end.
    @var hex RFID_ENDCODE

    UART serial connection via PySerial.
    @var Serial __serial

    Holds the complete tag after reading.
    @var string __tag
    """
    
    RFID_STARTCODE = 0x02
    RFID_ENDCODE = 0x03
    __serial = None
    __tag = None
    
    """
    "" Constructor
    ""
    "" @param string port
    "" @param integer baudRate
    "" @return void
    """
    def __init__(self, port = '/dev/ttyUSB0', baudRate = 9600):

        ## Validates port
        if ( os.path.exists(port) == False ):
            raise Exception('The RFID sensor port "' + port + '" was not found!')
            
        ## Initializes connection
        self.__serial = serial.Serial(port = port, baudrate = baudRate, bytesize = serial.EIGHTBITS, timeout = 1)

    def __del__(self):
        """
        Destructor

        """
        
        ## Closes connection if established
        if ( self.__serial != None and self.__serial.isOpen() == True ):
            self.__serial.close()
    
    def read(self):
        """
        Reads the complete tag and returns status.
        
        @return boolean
        """
        
        self.__tag = None
        tag = ''
        checksum = 0
        receivedPacketData = []
        index = 0

        while ( True ):
            
            ## Reads on byte
            receivedFragment = self.__serial.read()
            
            ## Collects RFID data
            if ( len(receivedFragment) != 0 ):

                ## Cuts start and stop bytes
                if ( index > 0 and index < 13):
                    tag += receivedFragment
                    
                #print receivedFragment
                
                ## Coverts received string to byte for calculation
                receivedFragment = utilities.stringToByte(receivedFragment)
                receivedPacketData.append(receivedFragment)
                index += 1              
                print hex(receivedFragment)

            ## Packet completly received
            if ( index == 14 ):
            
                ## Checks for invalid packet data
                if ( receivedPacketData[0] != self.RFID_STARTCODE ) or ( receivedPacketData[13] != self.RFID_ENDCODE ): 
                    raise Exception('Invalid packet data!')

                print '-----------'
                
                ## Calculates packet checksum
                for i in range(1, 10, 2):
                    byteToCheck = utilities.leftShift(receivedPacketData[i], 4)

                    print 'byteToCheck1: '+ hex(byteToCheck)
                    byteToCheck = byteToCheck | receivedPacketData[i+1]

                    print 'byteToCheck2: '+ hex(receivedPacketData[i+1])

                    byteToCheck = utilities.rightShift(byteToCheck, 4)
                    
                    print 'XOR: '+ hex(byteToCheck)                
                    checksum = checksum ^ byteToCheck

                ## Gets received packet checksum
                receivedChecksum = utilities.leftShift(receivedPacketData[11], 4)
                receivedChecksum = receivedChecksum | receivedPacketData[12]

                print checksum
                print receivedChecksum
                
                ## Checks for wrong checksum
                #if ( checksum != receivedChecksum ):
                #    raise Exception('Calculated checksum is wrong!')

                ## Sets complete tag for other methods
                self.__tag = tag
                
                return True
    
    @property
    def tagId(self):
        """
        Returns ID of tag.
        
        @return string (10 bytes)
        """
        if ( self.__tag != None ):

            ## Calculates ID of tag (10 integer digits = zero padding) 
            return '%010i' % int(self.__tag[4:10], 16)                

    @property
    def tagType(self):
        """
        Returns type of tag (e.g.: 0x0800 = round tag, 0x0300 = rectangle tag).
        
        @return hex (4 bytes)
        """
        if ( self.__tag != None ):
            return hex(int(self.__tag[0:4], 16))

    @property
    def checksum(self):
        """
        Returns checksum of read tag ID.
        
        @return hex (2 bytes)
        """
        if ( self.__tag != None ):
            return hex(int(self.__tag[10:12], 16))

"""     
# Checksumme berechnen
for I in range(0, 9, 2):
    Checksumme = Checksumme ^ (((int(ID[I], 16)) << 4) + int(ID[I+1], 16))
Checksumme = hex(Checksumme)

# Tag herausfiltern
Tag = ((int(ID[1], 16)) << 8) + ((int(ID[2], 16)) << 4) + ((int(ID[3], 16)) << 0)
Tag = hex(Tag)
"""

# Tests:
if ( __name__ == '__main__' ):
    """
    __rfid = PyRfid('/dev/ttyUSB0', 9600)

    try:
        print 'Waiting for tag...'

        while ( __rfid.read() != True ):
            pass

        print 'test: '+ __rfid.tagId
        ## The new user information
        #rfidHash = hashlib.sha256(__rfid.tagId).hexdigest() 

    except Exception as e:
        print '[Exception] '+ e.message
    """
    data = []
    data.append('0')
    data.append('F')
    receivedFragment1 = utilities.stringToByte(data[0])
    print '"0": '+ hex(receivedFragment1) +' (sollte 0 sein)'

    receivedFragment2 = utilities.stringToByte(data[1])
    print '"F": '+ hex(receivedFragment2) +' (sollte 15 sein)'

    #print receivedFragment1 ^ receivedFragment2
    print 'leftshift 4: '+ hex(utilities.leftShift(receivedFragment2, 4))
    print 'leftshift 8: '+ hex(utilities.leftShift(receivedFragment2, 8))
