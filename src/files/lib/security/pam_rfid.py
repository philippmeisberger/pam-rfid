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
import uuid
import syslog
import os


def auth_log(message, priority=syslog.LOG_INFO):
    """
    Sends errors to default authentication log

    @param string message
    @param integer priority
    @return void
    """

    syslog.openlog(facility=syslog.LOG_AUTH)
    syslog.syslog(priority, 'pamrfid: ' + message)
    syslog.closelog()


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

    except Exception as e:
        auth_log(e.message, syslog.LOG_CRIT)
        return pamh.PAM_USER_UNKNOWN

    ## Tries to init Config
    try:
        config = Config('/etc/pamrfid.conf')

    except Exception as e:
        auth_log(e.message, syslog.LOG_CRIT)
        return pamh.PAM_IGNORE

    auth_log('The user "' + userName + '" is asking for permission for service "' + str(pamh.service) + '".', syslog.LOG_DEBUG)

    ## Checks if the the user was added in configuration
    if ( config.itemExists('Users', userName) == False ):
        auth_log('The user was not added!', syslog.LOG_ERR)
        return pamh.PAM_IGNORE

    ## Tries to get user information
    try:
        userData = config.readList('Users', userName)
        salt = userData[0]
        expectedTagHash = userData[1]

    except Exception as e:
        auth_log(e.message, syslog.LOG_CRIT)
        return pamh.PAM_AUTH_ERR

    ## Gets RFID sensor connection values
    port = config.readString('PyRfid', 'port')
    baudRate = config.readInteger('PyRfid', 'baudRate')

    ## Tries to establish connection
    try:
        rfid = PyRfid(port, baudRate)

    except Exception as e:
        auth_log(e.message, syslog.LOG_CRIT)
        pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, 'pamrfid ' + VERSION + ': Sensor initialization failed!'))
        return pamh.PAM_IGNORE

    msg = pamh.Message(pamh.PAM_TEXT_INFO, 'pamrfid ' + VERSION + ': Waiting for tag...')
    pamh.conversation(msg)

    ## Tries to read RFID
    try:
        ## Read out tag data
        if ( rfid.readTag() != True ):
            raise Exception('User aborted!')

        ## Hashs read tag
        tagHash = hashlib.sha256(salt.encode() + rfid.rawTag.encode()).hexdigest()

        ## Checks if the read Hash matches the stored
        if ( tagHash == expectedTagHash ):
            auth_log('Access granted!')
            pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, 'pamrfid ' + VERSION + ': Access granted!'))
            return pamh.PAM_SUCCESS
        else:
            auth_log('The found match is not assigned to user "' + userName + '"!', syslog.LOG_WARNING)
            pamh.conversation(pamh.Message(pamh.PAM_TEXT_INFO, 'pamrfid ' + VERSION + ': Access denied!'))
            return pamh.PAM_AUTH_ERR

    except Exception as e:
        auth_log('RFID read failed!' + e.message, syslog.LOG_CRIT)
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


def pam_sm_acct_mgmt(pamh, flags, argv):
    """
    PAM service function for account management.

    @param pamh
    @param flags
    @param argv
    @return integer
    """

    return pamh.PAM_SUCCESS


def pam_sm_open_session(pamh, flags, argv):
    """
    PAM service function to start session.

    @param pamh
    @param flags
    @param argv
    @return integer
    """

    return pamh.PAM_SUCCESS


def pam_sm_close_session(pamh, flags, argv):
    """
    PAM service function to terminate session.

    @param pamh
    @param flags
    @param argv
    @return integer
    """

    return pamh.PAM_SUCCESS


def pam_sm_chauthtok(pamh, flags, argv):
    """
    PAM service function for authentication token management.

    @param pamh
    @param flags
    @param argv
    @return integer
    """

    return pamh.PAM_SUCCESS
