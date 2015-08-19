#!python
# -*- encoding: utf-8 -*-

"""
    Sources/X.py - Sources on *nix sytems
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


sources_kernel = []
sources_posix = []

import os
import socket
import subprocess
# from Tyche.Sources.egd import EGD

def devRandom():
    if os.path.exists("/proc/sys/kernel/random/entropy_avail"):
        if int(subprocess.check_output(  # cygwin
                ["cat",
                 "/proc/sys/kernel/random/entropy_avail"])) >= 128:
            return open("/dev/random", "rb").read(16)
        else:
            # reading lesser bytes (low entropy)
            return open("/dev/urandom", "rb").read(4)
    else:
        # no difference between /dev/random and /dev/urandom (BSD & Cygwin)
        return open("/dev/urandom", "rb").read(8)

sources_kernel += [devRandom]

if os.path.exists("/dev/hrandom1"):
    def hRandom():
        return open("/dev/hrandom1").read(15)
    sources_posix += [hRandom]
