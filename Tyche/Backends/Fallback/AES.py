#!python
# -*- encoding: utf-8 -*-

"""
    Backends/Fallback/__init__.py - PEP 272 AES API
    The MIT License (MIT)

    Copyright (c) 2015 Simon Biewald

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
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
