#!python
# -*- encoding: utf-8 -*-

"""
    Sources/__init__.py - Universal entropy sources
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

import time
import struct
from math import floor
import os
from getpass import getuser
import threading

NO_RESOURCE = False

try:
    import resource
except ImportError:  # Why ever...
    NO_RESOURCE = True

from Tyche.Backends import py3compat

sources_universal = []
sources_weak = []

try:
    import ssl
except ImportError:
    "ignore it - python without ssl"
else:
    if hasattr(ssl, "RAND_bytes"):
        def ssl8():
            try:
                return ssl.RAND_bytes(8)
            except:
                return ""  # Do not block - return nothing
        sources_universal += [ssl8]

try:
    import rdrand
except SystemError:
    print("Please ignore this warning!")
except ImportError:
    "Module not found..."
else:
    rdrandom = lambda: rdrand.RdRandom().getrandombytes(16)
    rdrandom.__name__ = "rdrandom"
    sources_universal[rdrandom]


def timetime():
    t = time.time()
    return struct.pack("@I", int(2**30 * (t - floor(t))))


def timeclock():
    t = time.clock()
    return struct.pack("@I", int(2**30 * (t - floor(t))))


def other_weak_source():
    numerical = 0
    st = os.stat('/')  # root folder (nt or ce: reference to disk (C:/, E:/)
    if os.name == "posix":
        numerical ^= os.getegid()
        numerical ^= os.geteuid()
        numerical ^= os.getgid()
        numerical ^= os.getpgid(0)
        numerical ^= os.getpgrp()
        numerical ^= os.getppid()
        numerical ^= os.getuid()
        numerical ^= os.getsid(0)
        du = st.st_blocks * st.st_blksize * 512
    else:
        numerical ^= os.getpid()
        du = st.st_size

    numerical ^= os.getpid()
    buf = ""
    if hasattr(threading, 'current_thread'):
        for i in str(threading.current_thread().ident):
            if i not in ("None.L"):
                buf += i
            if len(buf) > 2 or (i == "L" and len(buf) > 1):
                numerical ^= int(buf)
                buf = ""
    del (buf)
    buf = ""
    for i in str(du):
        if i != "L" and i != ".":
            buf += i
        if len(buf) > 2 or (i == "L" and len(buf) > 1):
            numerical ^= int(buf)
            buf = ""
    del (buf)
    if not NO_RESOURCE:
        m = floor(
            resource.getrusage(
                resource.RUSAGE_SELF)[2]*resource.getpagesize())
        buf = ""
        for i in str(m):
            if i != "L" and i != ".":
                buf += i
            if len(buf) > 2 or (i == "L" and len(buf) > 1):
                numerical ^= int(buf)
                buf = ""
    numerical ^= ord(os.urandom(1))*0xff  # there... is... random... !
    return struct.pack("!H", numerical)

sources_weak += [other_weak_source]
sources_weak += [timetime, timeclock]
