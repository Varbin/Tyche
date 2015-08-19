#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
    Test.py - programm to execute (external) rng tests
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

from __future__ import print_function
from __future__ import with_statement

from Tyche import FortunaEasy
import os
import subprocess
import sys

EMPTY = ""
DOUBLE_N = "\n\n"

if float(sys.version[0:3]) < 2.7:
    print ("test suites will probably NOT work with python 2.6 and older")

def preparefile(file="RNGTESTFILE.txt"):
    print("Generating lots of random data!")
    f = FortunaEasy()
    print(" |", end=EMPTY)
    sys.stdout.flush()  # py3.2
    with open(file, "wb") as out:
        for i in range(35):
            out.write(f.get_random_bytes(448*1024))
            print("=", end=EMPTY)
            sys.stdout.flush()
    print(("| Done! (with %s reseeds)" % f.countSeeds()), end=DOUBLE_N)
    sys.stdout.flush()
    return f.countSeeds()


def rngtoolstest():
    print(" cat RNGTESTFILE.txt | rngtest")
    try:
        print(subprocess.check_output("cat RNGTESTFILE.txt | rngtest",
                                      shell=True))
        g = True
    except subprocess.CalledProcessError as e:
        print(str(e))
        g = False
    except OSError:
        print("Skipping test - rng-tools not installed or on windows")
        g = None
    return g


def enttest():
    print(" ent RNGTESTFILE.txt")
    try:
        print(
            subprocess.check_output("ent RNGTESTFILE.txt", shell=True).decode(
                "latin-1"))
        g = True
    except subprocess.CalledProcessError as e:
        print(str(e))
        g = False
    except OSError:
        print("Skipping test - ENT not foundSS")
        g = None
    return g


def run():
    valid = []
    preparefile()
    rngtest_result = rngtoolstest()
    if rngtest_result is not None:
        if rngtest_result:
            print("RNGTEST -> succes")
            valid.append(True)
        else:
            print("RNGTEST -> failed!")
    enttest_result = enttest()
    if enttest_result is not None:
        if enttest_result:
            print("ENTTEST -> succes")
            valid.append(True)
        else:
            print("ENTTEST -> failed!")

    return int(not bool(valid))


if __name__ == "__main__":
    exit(run())
