# -*-coding:utf8;-*-
# qpy:2
# qpy:console

"""
Tyche - Fortuna in Python
=========================

Python implementation of the CSPRNG
(Cryptographic-Secure-Pseudo-Random-Number-Generator)
Fortuna, designed by Bruce Schneier and Niels Ferguson, build with AES as
blockcipher and SHAd256 as secure hash function.


Why do I need a CSPRNG? My OS has one by itself!
-------------------------------------------------

On many systems, the OS' PRNG isn't secure, mainly on
Windows XP and 2000 and older OpenBSD versions (before
October 2013). In Windows XP and 2000 it was possible to
read 128 Kib of output before they were computed and
OpenBSD's arc4random used the broken stream cipher
ARC4 / RC4. Mainly on these system (but not only on them), you
definetly need a new, better CSPRNG.

Tyche passes all FIPS 140-2 tests perfectly (Testing with around 4.1 MiB)::

    rngtest 4
    Copyright (c) 2004 by Henrique de Moraes Holschuh
    This is free software; see the source for copying conditions.
    There is NO warranty; not even for MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE.

    rngtest: starting FIPS tests...
    rngtest: entropy source drained
    rngtest: bits received from input: 32768000
    rngtest: FIPS 140-2 successes: 1638
    rngtest: FIPS 140-2 failures: 0
    rngtest: FIPS 140-2(2001-10-10) Monobit: 0
    rngtest: FIPS 140-2(2001-10-10) Poker: 0
    rngtest: FIPS 140-2(2001-10-10) Runs: 0
    rngtest: FIPS 140-2(2001-10-10) Long run: 0
    rngtest: FIPS 140-2(2001-10-10) Continuous run: 0
    rngtest: input channel speed: (min=307.637; avg=7814.500; max=19073.486)\
    Mibits/s
    rngtest: FIPS tests speed: (min=7.833; avg=46.833; max=53.728)Mibits/s
    rngtest: Program run time: 671678 microseconds

How to use
----------

Access Fortuna directly (and secure - automaticly gather entropy)::

    >>> from Tyche import FortunaEasy
    >>> f = FortunaEasy()
    >>> f.get_random_bytes(9)
    ...
    >>> f.get_random_bytes(100*1024) # 100KiB
    ...


Requirements
------------

Tyche requires PyCrypto to use AES. For windows you can get prebuilt librarys \
http://www.voidspace.org.uk/python/modules.shtml#pycrypto__ .

.. note::
    On Windows, Tyche requests administrator access to start *egdw*, an \
    entropy gathering daemon as administrator. *egdw* adds additional \
    entropy (randomness) to the generator.

"""

__all__ = ["Sources", "random", "FortunaGenerator",
           "FortunaAccumulator", "FortunaEasy"]

from Tyche.Backends.py3compat import *

import array
import socket
import time
import threading
import Tyche.Sources as Sources
import os

from hashlib import sha256
from Tyche.Backends import AES
# from Crypto.Cipher import AES

Sources.sources = Sources.sources_all
# range = xrange


def sha256d(string):
    return sha256(sha256(string).digest()).digest()


class Counter(object):
    def __init__(self, nonce):
        self.__nonce = nonce
        self.reset()

    def __call__(self):
        old = self.__current.tostring()
        for i in range(len(self.__current)):
            try:
                self.__current[i] += 1
                break
            except:
                self.__current[i] = 0
#            return self.__current.tostring()
        return old

    def reset(self):
        self.__current = array.array("B", self.__nonce)


class FortunaGenerator(object):
    _p9 = 10

    def __init__(self):
        self.K = "".encode()
        self.C = Counter(("\x00"*16).encode('latin-1'))
        self.blocks = 0
        self.reseeds = 0

    def reseed(self, seed):
        self.K = sha256d(self.K + seed)
        self.C()
        self.reseeds += 1
#        print "Reseeding:", sha256d(seed).encode("hex")

    def generateBlocks(self, amount):
        assert self.K
        return ("".encode()).join([AES.new(key=self.K, mode=AES.MODE_ECB).encrypt(
            self.C()) for i in range(amount)])

    def pseudoRandomData(self, n):
        assert 0 <= n <= 2**20
        r = self.generateBlocks(n//16+1)[:n]
        self.K = self.generateBlocks(2)
        return r


class Pool(object):
    def __init__(self, minbits=-1):
        self.entropy = "".encode()
        self.inputs = []
        self.minbits = minbits
        self.there = self.length

    def digest(self):
        assert self.length() >= self.minbits
        data = sha256d(self.entropy)
        self.entropy = "".encode()
        return data

    def length(self):
        return len(self.entropy)*16

    def update(self, string):
        self.entropy += string
#        print "--------------------"
#        print string.encode("hex")
#        print self.entropy.encode("hex")


class FortunaAccumulator(object):
    minPoolSize = 128

    def __init__(self):
        self.__pools = [Pool() for i in range(32)]
        self.__G = FortunaGenerator()
        self._last_reseed = -1 # never seeded
        self._reseedCnt = 0

    def randomData(self, n):
        assert self._last_reseed < time.time()
        assert 0 <= n <= 1024**2
        if (self.__pools[0].length() >= 128) and (
                time.time() - self._last_reseed > 0.1):
            self._last_reseed = time.time()
            self._reseedCnt += 1
            s = "".encode()
            r = self._reseedCnt
            """ *** Took from PyCrypto *** """
            retval = []
            mask = 0
            for i in range(32):
                if (r & mask) == 0:
                    retval.append(i)
                else:
                    break  # optimization. once this fails, it always fails
                mask = (mask << 1) | 1
            """ *** End of PyCrypto Code *** """
            for pool in retval:
                s += self.__pools[pool].digest()
            self.__G.reseed(s)
        return self.__G.pseudoRandomData(n)

    def addRandomEvent(self, s, i, e):
        assert 1 <= len(e) <= 32 and 0 <= s <= 255 and 0 <= i <= 31
        self.__pools[i].update(bchr(s))
        self.__pools[i].update(bchr(len(e)))
        self.__pools[i].update(e)

    def forgetLastReseed(self):  # ok pycrypto, you have won... BUT
        self._last_reseed = -1   # using a negative number instead of none


class EntropySourceManager:
    def __init__(self, func, accumulator, s, start=0):
        self._A = accumulator
        self._s = s
        self._pool = start
        self._func = func

    def compute(self):
        d = self._func()
        # debug
        # from binascii import hexlify
        # print("RANDOM EVENT")
        # print(self._func.__name__)
        # print("EVENT:",hexlify(d))
        # print("POOL:", self._pool)
        # self._A.addRandomEvent(self._s, self._pool, d)
        # self._pool += 1
        # self._pool %= 32


class FortunaEasy:
    def __init__(self):
        self.__F = FortunaAccumulator()
        self._pid = os.getpid()
        self.__managers = [
            EntropySourceManager(
                Sources.sources[i], self.__F, i, (30+i) % 32)
            for i in range(len(Sources.sources))]
        self.atfork()  # reinit

    def atfork(self):
        for i in range(2):
            for i in range(32):
                self.__F.addRandomEvent(255, i, Sources.sources_kernel[0]())
        self.__F.forgetLastReseed()

    def get_random_bytes(self, bytes):
        if self._pid != os.getpid():
            self.atfork()
            self._pid = os.getpid()
        for manager in self.__managers:
            manager.compute()
        self.__F.addRandomEvent(255, 0, Sources.sources_kernel[0]())
        return self.__F.randomData(bytes)

    def countSeeds(self):
        return self.__F._reseedCnt
