#!python
# -*- encoding: utf-8 -*-

"""
    Backends/AES.py - AES wrapper for java, PyCrypto, pyaes
    Copyright (C) 2015  Simon Biewald

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import os

if os.name == 'java':
    try:
        from Tyche.Backends.Java.AES import *
    except ImportError:
        try:
            from Tyche.Backends.Fallback.AES import *
        except:
            raise SystemError('Your Jython version is outdated. '
                              'Please update or install the Java '
                              'Cryptography Extension (JCE) Unlimited '
                              'Strength Jurisdiction Policy for your '
                              'Java version.')
else:
    try:
        from Crypto.Cipher.AES import *
    except ImportError:
        from Tyche.Backends.Fallback.AES import *
