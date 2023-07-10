#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PAM RFID implementation

Copyright 2014 Philipp Meisberger <team@pm-codeworks.de>,
               Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.
"""

import hashlib
import syslog
import os
from configparser import ConfigParser

from pamrfid import __version__ as version
from pamrfid import CONFIG_FILE
from pyrfid.pyrfid import PyRfid


class UserUnknownException(Exception):
    """Dummy exception class for unknown user."""
    pass


class InvalidUserCredentials(Exception):
    """Dummy exception class for invalid user credentials."""
    pass


def show_pam_text_message(pamh, message, error_message=False):
    """
    Shows a PAM conversation text info.

    :param pamh: The PAM handle
    :param message: The message to print
    :param error_message: True if it is an error or False otherwise
    :return: bool
    """

    try:
        if error_message:
            style = pamh.PAM_ERROR_MSG
        else:
            style = pamh.PAM_TEXT_INFO

        msg = pamh.Message(style, 'PAM RFID {0}: {1}'.format(version, message))
        pamh.conversation(msg)
        return True

    except Exception as e:
        auth_log(str(e), syslog.LOG_ERR)
        return False


def auth_log(message, priority=syslog.LOG_INFO):
    """
    Sends errors to default authentication log

    :param message: The message to write to syslog
    :param priority: The priority of the syslog message
    """

    syslog.openlog(facility=syslog.LOG_AUTH)
    syslog.syslog(priority, 'PAM RFID: {0}'.format(message))
    syslog.closelog()


def pam_sm_authenticate(pamh, flags, argv):
    """
    PAM service function for user authentication.

    :param pamh:
    :param flags:
    :param argv:
    :return: int
    """

    # The authentication service should return [PAM_AUTH_ERROR] if the user has a null authentication token
    flags = pamh.PAM_DISALLOW_NULL_AUTHTOK

    # Initialize authentication progress
    try:
        # Tries to get user which is asking for permission
        user_name = pamh.ruser

        # Fallback
        if user_name is None:
            user_name = pamh.get_user()

        # Be sure the user is set
        if user_name is None:
            raise UserUnknownException('The user is not known!')

        # Checks if path/file is readable
        if not os.access(CONFIG_FILE, os.R_OK):
            raise Exception('The configuration file "{0}" is not readable!'.format(CONFIG_FILE))

        config_parser = ConfigParser()
        config_parser.read(CONFIG_FILE)

        # Log the user
        auth_log('The user "{0}" is asking for permission for service "{1}".'.format(user_name, pamh.service),
                 syslog.LOG_DEBUG)

        # Checks if the user was added in configuration
        if not config_parser.has_option('Users', user_name):
            raise Exception('The user was not added!')

        # Tries to get user information
        user_data = config_parser.get('Users', user_name).split(',')

        # Validates user information
        if len(user_data) != 2:
            raise InvalidUserCredentials('The user information of "{0}" is invalid!'.format(user_name))

        salt = user_data[0]
        expected_tag_hash = user_data[1]

    except UserUnknownException as e:
        auth_log(str(e), syslog.LOG_ERR)
        return pamh.PAM_USER_UNKNOWN

    except InvalidUserCredentials as e:
        auth_log(str(e), syslog.LOG_ERR)
        return pamh.PAM_AUTH_ERR

    except Exception as e:
        auth_log(str(e), syslog.LOG_ERR)
        return pamh.PAM_IGNORE

    # Initialize RFID sensor
    try:
        # Gets RFID sensor connection values
        port = config_parser.get('PyRfid', 'port')
        baud_rate = int(config_parser.get('PyRfid', 'baudRate'), 10)

        # Tries to establish connection
        rfid = PyRfid(port, baud_rate)

    except Exception as e:
        auth_log('The RFID sensor could not be initialized: ' + str(e), syslog.LOG_ERR)
        show_pam_text_message(pamh, 'Sensor initialization failed!', True)
        return pamh.PAM_IGNORE

    if not show_pam_text_message(pamh, 'Waiting for tag...'):
        return pamh.PAM_CONV_ERR

    # Authentication progress
    try:
        # Read out tag data
        if rfid.readTag() != True:
            raise Exception('User aborted!')

        # Hashs read tag
        tag_hash = hashlib.sha256(salt.encode() + rfid.rawTag.encode()).hexdigest()

        # Checks if the read Hash matches the stored
        if tag_hash == expected_tag_hash:
            auth_log('Access granted!')
            show_pam_text_message(pamh, 'Access granted!')
            return pamh.PAM_SUCCESS
        else:
            auth_log('The found match is not assigned to user "{0}"!'.format(user_name), syslog.LOG_WARNING)
            show_pam_text_message(pamh, 'Access denied!', True)
            return pamh.PAM_AUTH_ERR

    except Exception as e:
        auth_log('RFID read failed: {0}'.format(e), syslog.LOG_CRIT)
        show_pam_text_message(pamh, 'Access denied!', True)
        return pamh.PAM_AUTH_ERR

    # Deny per default
    return pamh.PAM_AUTH_ERR


def pam_sm_setcred(pamh, flags, argv):
    """
    PAM service function to alter credentials.

    :param pamh:
    :param flags:
    :param argv:
    :return: int
    """

    return pamh.PAM_SUCCESS


def pam_sm_acct_mgmt(pamh, flags, argv):
    """
    PAM service function for account management.

    :param pamh:
    :param flags:
    :param argv:
    :return: int
    """

    return pamh.PAM_SUCCESS


def pam_sm_open_session(pamh, flags, argv):
    """
    PAM service function to start session.

    :param pamh:
    :param flags:
    :param argv:
    :return: int
    """

    return pamh.PAM_SUCCESS


def pam_sm_close_session(pamh, flags, argv):
    """
    PAM service function to terminate session.

    :param pamh:
    :param flags:
    :param argv:
    :return: int
    """

    return pamh.PAM_SUCCESS


def pam_sm_chauthtok(pamh, flags, argv):
    """
    PAM service function for authentication token management.

    :param pamh:
    :param flags:
    :param argv:
    :return: int
    """

    return pamh.PAM_SUCCESS
