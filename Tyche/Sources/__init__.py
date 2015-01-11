#!python
# -*- encoding: utf-8 -*-

# Source/__init__.py
# Get all sources

# encoding could also be ASCII

import os

sources_all = []

sources_kernel = []  # these are (most times) the best
sources_posix = []
sources_windows = []
sources_universal = []

# time (recommendation by BSI)
sources_weak = []

if os.name == 'nt':
    from Tyche.Sources.Windows import *
elif os.name == 'posix':
    from Tyche.Sources.X import *
elif os.name == 'java':  # ?  PyCrypto on JAVA???
    # mabe the J2Crypto library ^^
    import array
    import java
    import java.lang.System
    import java.security.SecureRandom
    random = java.security.SecureRandom()
    os_name = java.lang.System.getProperty("os.name").lower()
    if "windows" in os_name:
        from Tyche.Sources.Windows import *
        # BUT:  the kernel source is different
    elif hasattr(java.nio.file.attribute, "PosixFilePermission"):
        from Tyche.Sources.X import *
    def javaGenerateSeed():
        seed = random.generateSeed(16)
        if type(seed) == array.array:
            seed = seed.tostring()
        return seed
    if "windows" in os_name:  # no CryptGenRandom.. replace!
        sources_kernel = [javaGenerateSeed]
    else:  # ADD to /dev/random
        sources_kernel += [javaGenerateSeed]
    
else:
    osurandom_fallback = lambda: os.urandom(8)
    osurandom.__name__ = "os.urandom-8"
    sources_kernel += [osurandom]

from Tyche.Sources.Universal import *

sources_all += (sources_kernel +
                sources_posix +
                sources_windows +
                sources_universal +
                sources_weak)

#while len(sources_all) < 8:
#    sources_all += (sources_posix +
#                    sources_windows +
#                    sources_universal +
#                    sources_kernel)


# time.time, time.clock, other_weak_source, sort of OSRANDOM
assert len(sources_all) > 3
