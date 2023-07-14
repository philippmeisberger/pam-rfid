#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PAM RFID

Copyright 2014 Philipp Meisberger <team@pm-codeworks.de>
All rights reserved.
"""

from setuptools import setup
from src.pamrfid import __version__

setup(
    name='libpam-rfid',
    version=__version__,
    description='Linux Pluggable Authentication Module (PAM) for hardware authentication via RFID.',
    author='Philipp Meisberger',
    author_email='team@pm-codeworks.de',
    url='https://www.pm-codeworks.de/pamrfid.html',
    license='D-FSL',
    package_dir={'': 'src'},
    packages=['pamrfid'],
    classifiers=[
        'Intended Audience :: System Administrators',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
    ]
)
