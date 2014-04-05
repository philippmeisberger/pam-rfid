"""
pamrfid
PAM implementation.

Copyright 2014 Philipp Meisberger, Bastian Raschke.
All rights reserved. 
"""

import sys 
sys.path.append('/usr/lib')

from pamrfid.version import VERSION
from pamrfid.Config import *

from PyRfid.PyRfid import *

import hashlib
import logging
import os

## Configures logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

## Creates and adds a file handler to logger
fileHandler = logging.FileHandler('/var/log/pamrfid.log')
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(fileHandler)


def pam_sm_authenticate(pamh, flags, argv):
    """
    PAM service function for user authentication.

    @param pamh
    @param flags
    @param argv
    @return integer
    """

    ## Tries to get user which is asking for permission
    try:
        userName = pamh.ruser

        ## Fallback
        if ( userName == None ):
            userName = pamh.get_user()            

        ## Be sure the user is set 
        if ( userName == None ):
            raise Exception('The user is not known!')

    except:
        e = sys.exc_info()[1]
        logger.error(e.message, exc_info=True)
        return pamh.PAM_USER_UNKNOWN

    ## Tries to init Config
    try:
        config = Config('/etc/pamrfid.conf')

    except:
        e = sys.exc_info()[1]
        logger.error(e.message, exc_info=True)
        return pamh.PAM_IGNORE

    logger.info('The user "' + userName + '" is asking for permission for service "' + str(pamh.service) + '".')

    ## Checks if the the user was added in configuration
    if ( config.itemExists('Users', userName) == False ):
        logger.error('The user was not added!')
        return pamh.PAM_IGNORE

    ## Tries to get user information
    try:
        expectedTagHash = config.readString('Users', userName)

    except:
        e = sys.exc_info()[1]
        logger.error(e.message, exc_info=False)
        return pamh.PAM_AUTH_ERR

    ## Gets RFID sensor connection values
    port = config.readString('PyRfid', 'port')
    baudRate = config.readInteger('PyRfid', 'baudRate')

    ## Tries to establish connection
    try:
        rfid = PyRfid(port, baudRate)

    except:
        e = sys.exc_info()[1]
        logger.error(e.message, exc_info=True)
        pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, 'pamrfid ' + VERSION + ': Sensor initialization failed!'))
        return pamh.PAM_IGNORE        
        
    msg = pamh.Message(pamh.PAM_TEXT_INFO, 'pamrfid ' + VERSION + ': Waiting for tag...')
    pamh.conversation(msg)

    ## Tries to read RFID
    try:
        ## Read out tag data
        if ( rfid.readTag() != True ):
            raise Exception('User aborted!')
       
        ## Hashs read tag ID       
        tagHash = hashlib.sha256(rfid.rawTag).hexdigest()
           
        ## Checks if the read Hash matches the stored 
        if ( tagHash == expectedTagHash ):
            logger.info('Access granted!')
            pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, 'pamrfid ' + VERSION + ': Access granted!'))
            return pamh.PAM_SUCCESS
        else:
            logger.info('The found match is not assigned to user "' + userName + '"!')
            pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, 'pamrfid ' + VERSION + ': Access denied!'))
            return pamh.PAM_AUTH_ERR

    except:
        e = sys.exc_info()[1]
        logger.error('RFID read failed!', exc_info=True)
        pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, 'pamrfid ' + VERSION + ': Access denied!'))
        return pamh.PAM_AUTH_ERR

    ## Denies for default
    return pamh.PAM_AUTH_ERR

def pam_sm_setcred(pamh, flags, argv):
    """
    PAM service function to alter credentials.

    @param pamh
    @param flags
    @param argv
    @return integer
    """

    return pamh.PAM_SUCCESS
