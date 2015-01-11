
# Tyche/x.py
# Sources on *nix systems

sources_kernel = []
sources_posix = []

import os
import socket
import subprocess
from Tyche.Sources.egd import EGD

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
