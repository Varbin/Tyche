=========================
Tyche - Fortuna in Python
=========================

Python implementation of the CSPRNG
(Cryptographic-Secure-Pseudo-Random-Number-Generator)
Fortuna, designed by Bruce Schneier and Niels Ferguson, build with AES as
block cipher and SHAd256 as secure hash function. In future releases using Two- and Threefish and 
and sha3 as secure hash will be added.

-----------------------
Why do I need a CSPRNG?
-----------------------

CSPRNGs are mainly designed to generate securely random data for cryptographic purposes. 
The output must be unpredictable (it is impossible to compute the next number without having the full 
PRNG state) and it must be impossible to get previously generated output.


On many systems, the OS' PRNG isn't secure, mainly on Windows XP and 2000 (and older).
Also old OpenBSD versions (before October 2013). In Windows XP and 2000 it was possible to
read 128 KiB of output even before they were computed and 128KiB previous output.
OpenBSD's arc4random PRNG used the broken stream cipher RC4. 
OpenSSL doesn't handle correctly forking ('cloning' of the processes) so it was possible 
to get two (or more) times the same output, PyCrypto's (a python library for cryptographic purposes) 
PRNG was not able to handle this correctly for a long time (2.6.0 and older), too.

Mainly on these systems (but not only on them), you need a new, better CSPRNG.


Tests
=====

Tyche's Fortuna passes a bunch of randomness tests. On other computers, these tests may fail 
(it's random, ok?).

FIPS 140-2
----------

|    rngtest 4
|    Copyright (c) 2004 by Henrique de Moraes Holschuh
|    This is free software; see the source for copying conditions.  There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

|    rngtest: starting FIPS tests...
|    rngtest: entropy source drained
|    rngtest: bits received from input: 32768000
|    rngtest: FIPS 140-2 successes: 1638
|    rngtest: FIPS 140-2 failures: 0
|    rngtest: FIPS 140-2(2001-10-10) Monobit: 0
|    rngtest: FIPS 140-2(2001-10-10) Poker: 0
|    rngtest: FIPS 140-2(2001-10-10) Runs: 0
|    rngtest: FIPS 140-2(2001-10-10) Long run: 0
|    rngtest: FIPS 140-2(2001-10-10) Continuous run: 0
|    rngtest: input channel speed: (min=307.637; avg=7814.500; max=19073.486)Mibits/s
|    rngtest: FIPS tests speed: (min=7.833; avg=46.833; max=53.728)Mibits/s
|    rngtest: Program run time: 671678 microseconds


ENT-Test
--------

|    Entropy = 7.999955 bits per byte.
|
|    Optimum compression would reduce the size of this 4096000 byte file by 0 percent.
|
|    Chi square distribution for 4096000 samples is 255.87, and randomly
|    would exceed this value 50.00 percent of the times.
|
|    Arithmetic mean value of data bytes is 127.4906 (127.5 = random).
|    Monte Carlo value for Pi is 3.142936663 (error 0.04 percent).
|    Serial correlation coefficient is -0.000507 (totally uncorrelated = 0.0).


It passes even the DIEHARD test suite, the log is just too big to add here.

------------
Installation
------------

Install it with pip::

	$ pip install Tyche

	
Do not use easy_install to install.

-----------
Exapmples
-----------

Use Tyche's easy to use CSPRNG::

    >>> from Tyche import FortunaEasy
    >>> f = FortunaEasy()
    >>> f.get_random_bytes(16)  # AES key
    ...
    >>> f.get_random_bytes(100*1024) # 100KiB
    ...

Replacing python's random module::

    >>> from Tyche import random
    >>> random.randint(1, 6)
    ...  # it' s random!
    >>> random.random()
    ...  # random again!

You could also use Fortuna directly, but be sure you now what you do (forking an reseeding will NOT be handled!)::

    >>> from Tyche import FortunaGenerator
    >>> f = FortunaGenerator()
    >>> f.reseed(b"secret seed")
    >>> f.pseudoRandomData(8)
    '\xd8w)W!\xe4\x93\xc4'  # py3: b'\xd8w)W!\xe4\x93\xc4'
    

------------
Requirements
------------

Tyche requires no external module to run, it is based on *hashlib* (shipped with python) and some 
other, internal libraries. It's shipped with pyaes to have an own aes library if PyCrypto is not found. 
*PyCrypto* will speed up Tyche up to 8 times.

.. note::
    If using python 2.5 (and maybe 2.6) and older you *have* to install PyCrypto to use Tyche! 

Tyche is tested with CPython 3.4, CPython 2.6, CPython 2.7, PyPy 2.4, PyPy3 2.4, Jython 2.7b3 and 
Jython 2.5.3, all 32-bit. Please note if using Jython, Oracle Java and living outside US, apply the 
*Java Cryptography Extension (JCE) Unlimited Strength Jurisdiction Policy* 
to not use the *realy slow* pure python AES library shipped with Tyche.

To use the *Tyche.Test* module, you have to install at least Python 2.7.
 
.. note:: 
    On Windows, Tyche requests administrator access to start *egdw*, an entropy 
    gathering daemon as administrator. *egdw* adds additional entropy (randomness) to 
    the generator.

---
FAQ
---

Help! It does not work!
=======================

Please write a bug report. The bug report should contain some basic information about your system 
(OS, Python version, what type of python (Jython, PyPy, ...), etc.) and a log of your program.

Tests are not working
=====================

To run all tests, you have to install rng-tools (FIPS tests) and ENT. They are NOT shipped with Tyche. 
If the FIPS tests fail, not problem. It's random - there is no perfect test. Please note that the tests 
requires at least python 2.7 (or the py3k equivalent). If it still does not work, write a bug report.

It's so slow!
=============

This sometimes happens. Currently, the fall-back library (pyaes) is slow (even on PyPy), remember to install 
PyCrypto (even on PyPy).

Haven't you said above, PyCrypto is insecure?
=============================================

I've talked about the PRNG part of PyCrypto, not general PyCrypto. That's a big difference.

How can I help to improve Tyche?
================================

Fork the project on Github. Please have backwards compatibility at least to 
python 2.5 (Jython 2.5.3), if adding something new this does not apply (only the program core 
hash to run on python 2.5+; additional things (for example Two- or Threefish) does not need 
to work on all python versions). Please also try to not add extra dependencies (this only applies to
core functionality). 

What it is licensed?
=======================

GPL v2.0+