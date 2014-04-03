"""
PyRfid
Example RFID read.

Copyright 2014 Philipp Meisberger (PM Code Works).
All rights reserved. 
"""

from PyRfid.PyRfid import *

   
rfid = PyRfid('/dev/ttyUSB0', 9600)

try:
    print 'Waiting for tag...'

    if ( rfid.readTag() != True ):
        raise Exception('User aborted!')
    
    print 'ID:       '+ rfid.tagId
    print 'Type:     '+ rfid.tagType
    print 'Checksum: '+ rfid.tagChecksum
    print 'RAW:      '+ rfid.rawTag

except Exception as e:
    print '[Exception] '+ e.message
