#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PAM RFID implementation

Copyright 2014 Philipp Meisberger <team@pm-codeworks.de>,
               Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.
"""

import hashlib
import uuid
import syslog
import os
import ConfigParser

from pamrfid import __version__ as VERSION
from pyrfid.pyrfid import PyRfid


class UserUnknownException(Exception):
    """
    Dummy exception class for unknown user.

    """

    pass

class InvalidUserCredentials(Exception):
    """
    Dummy exception class for invalid user credentials.

    """

    pass

def showPAMTextMessage(pamh, message, errorMessage=False):
    """
    Shows a PAM conversation text info.

    @param pamh
    The PAM handle.

    @param str message
    The message to print.

    @return bool
    """

    try:
        if ( errorMessage == True ):
            style = pamh.PAM_ERROR_MSG
        else:
            style = pamh.PAM_TEXT_INFO

        msg = pamh.Message(style, 'pamrfid ' + VERSION + ': '+ str(message))
        pamh.conversation(msg)
        return True

    except Exception as e:
        auth_log(str(e), syslog.LOG_ERR)
        return False


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

    @return int
    """

    ## The authentication service should return [PAM_AUTH_ERROR] if the user has a null authentication token
    flags = pamh.PAM_DISALLOW_NULL_AUTHTOK

    ## Initialize authentication progress
    try:
        ## Tries to get user which is asking for permission
        userName = pamh.ruser

        ## Fallback
        if ( userName == None ):
            userName = pamh.get_user()

        ## Be sure the user is set
        if ( userName == None ):
            raise UserUnknownException('The user is not known!')

        ## Checks if path/file is readable
        if ( os.access(CONFIG_FILE, os.R_OK) == False ):
            raise Exception('The configuration file "' + CONFIG_FILE + '" is not readable!')

        configParser = ConfigParser.ConfigParser()
        configParser.read(CONFIG_FILE)

        ## Log the user
        auth_log('The user "' + userName + '" is asking for permission for service "' + str(pamh.service) + '".', syslog.LOG_DEBUG)

        ## Checks if the the user was added in configuration
        if ( configParser.has_option('Users', userName) == False ):
            raise Exception('The user was not added!')

        ## Tries to get user information
        userData = configParser.get('Users', userName).split(',')

        ## Validates user information
        if ( len(userData) != 2 ):
            raise InvalidUserCredentials('The user information of "' + userName + '" is invalid!')

        salt = userData[0]
        expectedTagHash = userData[1]

    except UserUnknownException as e:
        auth_log(str(e), syslog.LOG_ERR)
        return pamh.PAM_USER_UNKNOWN

    except InvalidUserCredentials as e:
        auth_log(str(e), syslog.LOG_ERR)
        return pamh.PAM_AUTH_ERR

    except Exception as e:
        auth_log(str(e), syslog.LOG_ERR)
        return pamh.PAM_IGNORE

    ## Initialize RFID sensor
    try:
        ## Gets RFID sensor connection values
        port = config.readString('PyRfid', 'port')
        baudRate = config.readInteger('PyRfid', 'baudRate')

        ## Tries to establish connection
        rfid = PyRfid(port, baudRate)

    except Exception as e:
        auth_log('The RFID sensor could not be initialized: ' + str(e), syslog.LOG_ERR)
        showPAMTextMessage(pamh, 'Sensor initialization failed!', True)
        return pamh.PAM_IGNORE

    if ( showPAMTextMessage(pamh, 'Waiting for tag...') == False ):
        return pamh.PAM_CONV_ERR

    ## Authentication progress
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
            showPAMTextMessage(pamh, 'Access denied!', True)
            return pamh.PAM_AUTH_ERR

    except Exception as e:
        auth_log('RFID read failed: ' + str(e), syslog.LOG_CRIT)
        showPAMTextMessage(pamh, 'Access denied!', True)
        return pamh.PAM_AUTH_ERR

    ## Denies for default
    return pamh.PAM_AUTH_ERR


def pam_sm_setcred(pamh, flags, argv):
    """
    PAM service function to alter credentials.

    @param pamh
    @param flags
    @param argv
    @return int
    """

    return pamh.PAM_SUCCESS

def pam_sm_acct_mgmt(pamh, flags, argv):
    """
    PAM service function for account management.

    @param pamh
    @param flags
    @param argv
    @return int
    """

    return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
    """
    PAM service function to start session.

    @param pamh
    @param flags
    @param argv
    @return int
    """

    return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
    """
    PAM service function to terminate session.

    @param pamh
    @param flags
    @param argv
    @return int
    """

    return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
    """
    PAM service function for authentication token management.

    @param pamh
    @param flags
    @param argv
    @return int
    """

    return pamh.PAM_SUCCESS
