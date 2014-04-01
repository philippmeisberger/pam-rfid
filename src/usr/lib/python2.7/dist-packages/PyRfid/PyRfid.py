"""
"" RFID
"" A python written library for an RFID reader.
""
"" Requirements:
"" ~# apt-get install python-serial
""
"" @see http://www.seeedstudio.com/wiki/index.php?title=Electronic_brick_-_125Khz_RFID_Card_Reader#Demo_code
"" @see https://github.com/johannrichard/SeeedRFIDLib/blob/master/SeeedRFIDLib.cpp
""
"" Copyright 2014 Philipp Meisberger (PM Code Works).
"" All rights reserved. 
"""

import utilities
import serial
import os

class PyRfid(object):

    """
    "" Flag for RFID connection start.
    "" @var hex RFID_STARTCODE
    """
    RFID_STARTCODE = 0x02

    """
    "" Flag for RFID connection end.
    "" @var hex RFID_ENDCODE
    """
    RFID_ENDCODE = 0x03

    """
    "" UART serial connection via PySerial.
    "" @var Serial __serial
    """
    __serial = None

    """
    "" Holds the ID after reading.
    "" @var string __tagId
    """
    __tagId = None
    
    """
    "" Holds the checksum after reading.
    "" @var string __checksum
    """
    __checksum = None
    
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

    """
    "" Destructor
    ""
    "" @return void
    """
    def __del__(self):

        ## Closes connection if established
        if ( self.__serial != None and self.__serial.isOpen() == True ):
            self.__serial.close()
    
    """
    "" Returns the ID of a RFID card.
    ""
    "" @return boolean
    """
    def read(self):

        self.__tagId = None
        self.__checksum = None
        receivedPacketData = []
        index = 0

        while ( True ):

            ## Reads one byte
            receivedFragment = self.__serial.read()
            print str(index) +': '+ receivedFragment

            if ( len(receivedFragment) != 0 ):
                #receivedFragment = utilities.stringToByte(receivedFragment)

                ## Inserts byte if packet seems valid
                receivedPacketData.insert(index, receivedFragment)
                index += 1

            ## Packet complete received (maximum length is 14 bytes)
            if ( index == 14 ):

                print 'complete!'
                return True
                
                """
                ## Checks if start and end bytes are valid
                if ( receivedPacketData[0] != self.RFID_STARTCODE | receivedPacketData[13] != self.RFID_ENDCODE ):
                    raise Exception('Invalid packet header!')

                packetPayload = []
                checksum = 0x00
                
                ## Collects package payload (10 bytes) and calculates checksum
                for i in range(1, 12, 2):
                    checksum = checksum ^ receivedPacketData[i] ^ receivedPacketData[i+1]
                    packetPayload.append(receivedPacketData[i])
                    print receivedPacketData[i]

                print checksum    
                
                ## Calculates checksum of the 2 checksum bytes
                receivedChecksum = utilities.leftShift(receivedPacketData[11], 8)
                receivedChecksum = receivedChecksum | utilities.leftShift(receivedPacketData[12], 0)
                
                if ( packetChecksum != receivedChecksum ):
                    raise Exception('Checksum of packet is wrong!')

                ## Store checksum
                self.__checksum = receivedChecksum
                
                ## Gets ID of tag
                tagId = ''

                for i in range(2, 10):
                    tagId += packetPayload[i]                

                ## Store ID of tag
                self.__tagId = tagId
                
                return True
                """
    
    """
    "" Returns ID of tag.
    ""
    "" @return string (5 bytes)
    """
    @property
    def tagId(self):

        return self.__tagId

    """
    "" Returns type of tag (0800 = round tag, 0300 = rectangle tag).
    ""
    "" @return hex (2 bytes)
    """
    @property
    def tagType(self):

        if ( len(self.__tagId) != 10 ):
            raise ValueError('Invalid packet length!')

        tagType = self.__tagId[0]
        tagType += self.__tagId[1]
        return hex(tagType)

    """
    "" Returns checksum of read tag ID.
    ""
    "" @return hex (2 bytes)
    """
    @property
    def checksum(self):

        return self.__checksum

"""     
# Checksumme berechnen
for I in range(0, 9, 2):
    Checksumme = Checksumme ^ (((int(ID[I], 16)) << 4) + int(ID[I+1], 16))
Checksumme = hex(Checksumme)

# Tag herausfiltern
Tag = ((int(ID[1], 16)) << 8) + ((int(ID[2], 16)) << 4) + ((int(ID[3], 16)) << 0)
Tag = hex(Tag)

# Ausgabe der Daten
print "------------------------------------------"
print "Datensatz: ", ID
print "Tag: ", Tag
print "ID: ", ID[4:10]
print "Checksumme: ", Checksumme
print "------------------------------------------"
"""

# Tests:
if ( __name__ == '__main__' ):

    __rfid = PyRfid('/dev/ttyUSB0', 9600)

    ## Tries to bind a tag to a user
    try:
        print 'Waiting for tag...'

        while ( __rfid.read() != True ):
            pass

        ## The new user information
        #rfidHash = hashlib.sha256(__rfid.tagId).hexdigest() 

    except Exception as e:
        print '[Exception] '+ e.message
