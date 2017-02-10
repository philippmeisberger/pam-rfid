#!/usr/bin/env python

from setuptools import setup, find_packages

import sys
sys.path.append('./files/')

## Dynamically get the module version
packageVersion = __import__('pamrfid').__version__

setup(
    name            = 'libpam-rfid',
    version         = packageVersion,
    description     = 'Pluggable Authentication Module (PAM) for hardware authentication via RFID.',
    author          = 'Philipp Meisberger',
    author_email    = 'team@pm-codeworks.de',
    url             = 'http://www.pm-codeworks.de/pamrfid.html',
    license         = 'D-FSL',
    package_dir     = {'': 'files'},
    packages        = ['pamrfid'],
)
