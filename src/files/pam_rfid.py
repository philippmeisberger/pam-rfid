#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pamrfid
PAM implementation

Copyright 2015 Philipp Meisberger, Bastian Raschke.
All rights reserved.
"""

import hashlib
import uuid
import syslog
import os
import pamrfid.Config as Config
import pamrfid.__version as VERSION
import pyrfid.PyRfid as PyRfid


def showPAMTextMessage(pamh, message):
    """
    Shows a PAM conversation text info.

    @param pamh
    @param string message

    @return void
    """

    if ( type(message) != str ):
        raise ValueError('The given parameter is not a string!')

    msg = pamh.Message(pamh.PAM_TEXT_INFO, 'pamrfid ' + VERSION + ': '+ message)
    pamh.conversation(msg)


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
        auth_log(str(e), syslog.LOG_CRIT)
        return pamh.PAM_USER_UNKNOWN

    ## Tries to init Config
    try:
        config = Config('/etc/pamrfid.conf')

    except Exception as e:
        auth_log(str(e), syslog.LOG_CRIT)
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
        auth_log(str(e), syslog.LOG_CRIT)
        return pamh.PAM_AUTH_ERR

    ## Gets RFID sensor connection values
    port = config.readString('PyRfid', 'port')
    baudRate = config.readInteger('PyRfid', 'baudRate')

    ## Tries to establish connection
    try:
        rfid = PyRfid(port, baudRate)

    except Exception as e:
        auth_log(str(e), syslog.LOG_CRIT)
        showPAMTextMessage(pamh, 'Sensor initialization failed!')
        return pamh.PAM_IGNORE

    showPAMTextMessage(pamh, 'Waiting for tag...')

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
            showPAMTextMessage(pamh, 'Access granted!')
            return pamh.PAM_SUCCESS
        else:
            auth_log('The found match is not assigned to user "' + userName + '"!', syslog.LOG_WARNING)
            showPAMTextMessage(pamh, 'Access denied!')
            return pamh.PAM_AUTH_ERR

    except Exception as e:
        auth_log('RFID read failed!' + str(e), syslog.LOG_CRIT)
        showPAMTextMessage(pamh, 'Access denied!')
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
