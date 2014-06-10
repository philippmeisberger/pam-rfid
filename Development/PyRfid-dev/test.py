from PyRfid import PyRfid

rfid = PyRfid()

try:
    while ( True ):
        
        if ( rfid.readTag() == True ):
            print 'ok'
            
except KeyboardInterrupt:
    print 'end'
