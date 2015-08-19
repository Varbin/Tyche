#!python
# -*- encoding: utf-8 -*-

"""
    Sources/windows.py - Entropy on Windows systems
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


from __future__ import with_statement

from Tyche.Sources.egd import EGD

import subprocess
import os
import socket

sources_windows = []
sources_kernel = []


def CryptGenRandom16():
    # avoid 128-KiB bug on old systems - making it slow on vista+
    assert len(os.urandom(128*1024)) == 128*1024
    out = os.urandom(16)  # calls CryptGenRandom - ultimate here
    assert len(os.urandom(128*1024)) == 128*1024
    return out


class EGDW(EGD):
    def __init__(self, port=708):
        try:
            self._egdw = subprocess.Popen(
                "powershell Start-Process " +
                os.path.join(os.path.dirname(__file__),
                             "egdw.exe") +
                " --port="+str(int(port)) +
                " -Verb runAs", shell=True)
        except:
            self._egdw = subprocess.Popen("egdw.exe "
                                          "--port="+str(int(port)),
                                          shell=True)
        if self._egdw.poll() is not None:
            # Already running - can't start a new one
            try:  # possible bad now...
                with open(os.path.join(os.environ['WINDIR'],
                                       "egd.port")) as egdport:
                    port = int(egdport.read().replace("\n", ""))
            except:
                assert 0
            else:
                self.need_shutdown = False
        else:
            self.need_shutdown = True
        EGD.__init__(self, port)

    def shutdown(self):
        EGD.shutdown(self)
        if self.need_shutdown:
            os.startfile("egdw.exe --close", "runas")
'''
try:
    _egdw_service = EGDW()
except (AssertionError, socket.error, WindowsError):
    "Continue - ignore it"
else:
    egdw_random = lambda: _egdw_service.gen_random(16)
    egdw_random.__name__ = "<lambda: egdw_random>"
    sources_windows.append(egdw_random)
'''

try:
    import winreg
except ImportError:
    try:
        import _winreg as winreg
    except ImportError:
        winreq = None

if winreg is not None:
    from hashlib import sha1
    def win_internal_states():
        return sha1(
            winreg.QueryValueEx(
                winreg.HKEY_PERFORMANCE_DATA, 'global')[0]
            ).digest()
    sources_windows += [win_internal_states]

try:
    import win32api
except ImportError:
    "Do nothing."
else:
    class MouseEntroWindows(object):
        def __init__(self):
            self.last = ""

        def get_mouse_data(self):
            try:
                out = struct.pack("HH", *win32api.GetCursorPos())
            except Exception:
                out = ""
            m = out
            if out == self.last:
                out = ""
            self.last = m
            return out

    sources_windows.append(MouseEntroWindows().get_mouse_data)

sources_kernel.append(CryptGenRandom16)
