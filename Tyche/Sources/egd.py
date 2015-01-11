#!python
# -*- encoding: utf-8 -*-

"""
    Sources/egd.py - (Unused) EGD manager
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

# encoding could also be ASCII


import socket
from Tyche.Backends.py3compat import *

class EGD(object):
    def __init__(self, port=708, address='localhost', family=socket.AF_INET):
        for i in range(5):
            try:
                self.sock = sock = socket.socket(family=family)
                if hasattr(socket, "AF_UNIX"):
                    if family == socket.AF_UNIX:
                        socket.connect((address))
                    else:
                        sock.connect((address, port))
                else:  # non-unix
                    sock.connect((address, port))
            except:
                self.running = False
            else:
                self.running = True
                break

    def gen_random(self, amount):
        assert -1 < amount < 256 and isinstance(amount, int) and self.running
        self.sock.send(b("\x01")+bchr(amount))
        return self.sock.recv(256)[1:]

    def shutdown(self):
        self.sock.close()
        self.running = False
