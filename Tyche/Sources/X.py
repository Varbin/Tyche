#!python
# -*- encoding: utf-8 -*-

"""
    Sources/X.py - Sources on *nix sytems
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
