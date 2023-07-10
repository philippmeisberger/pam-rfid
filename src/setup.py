#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PAM RFID

Copyright 2014 Philipp Meisberger <team@pm-codeworks.de>
All rights reserved.
"""

from setuptools import setup

import sys

sys.path.insert(0, './files/')

import pamrfid

setup(
    name='libpam-rfid',
    version=pamrfid.__version__,
    description='Linux Pluggable Authentication Module (PAM) for hardware authentication via RFID.',
    author='Philipp Meisberger',
    author_email='team@pm-codeworks.de',
    url='http://www.pm-codeworks.de/pamrfid.html',
    license='D-FSL',
    package_dir={'': 'files'},
    packages=['pamrfid'],
)
