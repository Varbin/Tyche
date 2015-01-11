#!python
# -*- encoding: utf-8 -*-

"""
    Backends/Java/AES.py - PEP-272 conform AES libraray from java (J2Py)
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

import java, javax, warnings

MODE_ECB = 1

b256 = True

### Test for 256 bit support!
key = javax.crypto.spec.SecretKeySpec(' '*32, "AES")
cipher = javax.crypto.Cipher.getInstance("AES")
try:
    cipher.init(javax.crypto.Cipher.ENCRYPT_MODE, key)
    cipher.doFinal(' '*32).tostring()
except java.security.InvalidKeyException:
    b256 = False

if not b256:
    raise ImportError('to be cought')

class AES:
    def __init__(self, key, mode=MODE_ECB):
        assert len(key) in (16, 24, 32)
        assert mode == MODE_ECB
        if len(key) == 32 and not BITS_256:
            raise Exception('Cannot use AES-256. Please install Java Cryptography Extension (JCE) Unlimited Strength Jurisdiction Policy Files for your java version')
        key = javax.crypto.spec.SecretKeySpec(key, "AES")
    def encrypt(self, data):
        cipher = javax.crypto.Cipher.getInstance("AES")
        cipher.init(javax.crypto.Cipher.ENCRYPT_MODE, self.key)
        return cipher.doFinal(data).tostring()
    def decrypt(self, data):
        cipher = javax.crypto.Cipher.getInstance("AES")
        cipher.init(javax.crypto.Cipher.DECRYPT_MODE, self.key)
        return cipher.doFinal(data).tostring()
    

def new(key, mode=MODE_ECB, iv=None):
    return AES(key, mode)

if __name__ == "__main__":
    a = AES(' '*16)
    print a.encrypt(' '*32).encode('hex')
    a = AES(' '*32)
    print a.encrypt(' '*32).encode('hex')
