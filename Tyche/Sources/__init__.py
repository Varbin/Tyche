#!python
# -*- encoding: utf-8 -*-

"""
    Sources/__init__.py - Entropy management
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
