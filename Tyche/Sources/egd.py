#!python
# -*- encoding: utf-8 -*-

# Source/egd.py
# For egd modules

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
