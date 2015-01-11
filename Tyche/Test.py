#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
    Test.py - programm to execute (external) rng tests
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
