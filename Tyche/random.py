#!python
# -*- encoding: utf-8 -*-

"""
    random.py - drop-in-replacement of python's random modulr
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

from binascii import hexlify
from random import Random
from random import RECIP_BPF
from Tyche import FortunaEasy

try:
    long
except NameError:  # py3
    long = int


class FortunaRandom(Random):
    def __init__(self):
        self._inst = FortunaEasy()
        Random.__init__(self)

    def random(self):  # poorly implemented
        """Get the next random number from the range [0.0, 1.0]"""
        # --------------------
        # Old, poor method:
        #    return ord(self._inst.get_random_bytes(1)) / 255.0
        # --------------------
        # New method:
        return (long(hexlify(self._inst.get_random_bytes(7)),
                     16) >> 3) * RECIP_BPF

    def getrandbits(self, k):
        """getrandbits(k) -> x, Generate a long int with k random bits"""
        assert k >= 0 and k == int(k)
        numbytes = (k + 7) // 8
        x = int.from_bytes(self._inst.get_random_bytes(numbytes), "big")
        return x >> (numbytes * 8 - k)

    def _stub(self, *args, **kwargs):
        return

    seed = jumpahaed = _stub

    def _notimplemented(self):
        raise NotImplementedError

    getstate = setstate = _notimplemented

_inst = FortunaRandom()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gauss = _inst.gauss
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
getrandbits = _inst.getrandbits
