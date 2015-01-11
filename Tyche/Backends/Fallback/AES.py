#!python
# -*- encoding: utf-8 -*-

"""
    Backends/Fallback/__init__.py - PEP 272 AES API
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

from Tyche.Backends.Fallback.pyaes import AESModeOfOperationECB


MODE_ECB = 1

class AES(object):
    def __init__(self, key, mode=MODE_ECB, iv=None):
        assert mode == MODE_ECB  # this is just a fallback - no more
        self._aes = AESModeOfOperationECB(key)
    def encrypt(self, data):
        return self._aes.encrypt(data)

    def decrypt(self, data):
        return self._aes.decrypt(data)

def new(key, mode=MODE_ECB):
    return AES(key, mode)
