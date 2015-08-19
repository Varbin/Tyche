#!python
# -*- encoding: utf-8 -*-

"""
    Backends/Java/AES.py - PEP-272 conform AES libraray for Jython (J2Py)
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
