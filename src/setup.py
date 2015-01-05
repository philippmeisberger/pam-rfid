#!/usr/bin/env python

from distutils.core import setup

setup(
    name            = 'libpam-rfid',
    version         = '1.1',
    description     = ' Pluggable Authentication Module (PAM) for hardware authentication via RFID.',
    author          = 'Philipp Meisberger',
    author_email    = 'team@pm-codeworks.de',
    url             = 'http://www.pm-codeworks.de/pamrfid.html',
    license         = 'BSD 3 License',
    package_dir     = {'': 'files'},
    packages        = ['pamrfid'],
)
