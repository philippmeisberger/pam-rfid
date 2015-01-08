#!/usr/bin/env python

from distutils.core import setup

setup(
    name            = 'libpam-rfid',
    version         = '1.2',
    description     = 'Pluggable Authentication Module (PAM) for hardware authentication via RFID.',
    author          = 'Philipp Meisberger',
    author_email    = 'team@pm-codeworks.de',
    url             = 'http://www.pm-codeworks.de/pamrfid.html',
    license         = 'Simplified BSD 3 license',
    package_dir     = {'': 'files'},
    packages        = ['pamrfid'],
)
