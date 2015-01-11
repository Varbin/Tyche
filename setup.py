#!python

"""
    setup.py - Setup of Tyche
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

import sys
import warnings
import os

try:
    from setuptools import setup
    from setuptools import Command
except ImportError:
    from distutils.core import setup
    from distutils.core import Command

try:
    raw_input
except NameError:
    raw_input = input

kwargs = dict(
    name="Tyche",
    version="1.0",
    description="Fortuna CSPRNG in Python",
    long_description=open("README.rst").read(),
    author="Simon Biewald",
    author_email="simon.biewald@hotmail.de",
    license=(open('LICENSE').read()),
    zip_safe=False,
    platforms="any",
    packages=['Tyche', 'Tyche.Sources',
              'Tyche.Backends', 'Tyche.Backends.Java',
              'Tyche.Backends.Fallback', 'Tyche.Backends.Fallback.pyaes'],
    url='https://github.com/Varbin/Tyche',
    classifiers=['Topic :: Security :: Cryptography',
                 'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.5',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: CPython',
                 'Programming Language :: Python :: Jython',
                 'Development Status :: 4 - Beta',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 ])

if float(sys.version[0:3]) < 2.5:
    kwargs['install_requires']=['pycrypto>=2.0']


if (('sdist' in sys.argv or
        'bdist_wheel' in sys.argv or
        'bdist_wininst' in sys.argv or
        'bdist_egg' in sys.argv or
        'bdist' in sys.argv) or (os.name == 'nt' and
                                 ('install' in sys.argv or
                                  'build' in sys.argv)
                                 )) and "--exclude-msvc" not in sys.argv:
    while True:
        agree = raw_input('\nYou need to agree to the Microsoft '
                          'Visual C++ 2007 Redistributable '
                          'License Agreement in order to '
                          'install this library together with '
                          'Visual C++ 2007 Redistributable '
                          'which is required for EGDW with windows '
                          '[Y/n] ')
        if agree in ('', 'y'):
            break
        print ('invalid answer, must be y or n')
        print ('')
addfiles = []
addfiles += ['Sources/cl32.dll']
addfiles += ['Sources/egdw.exe']
if "--exclude-msvc" not in sys.argv:
    addfiles += ['Sources/msvcr71.dll']
else:
    sys.argv.remove("--exclude-msvc")
addfiles = ['Backends/Fallback/pyaes/License.txt']

kwargs["package_data"] = {"Tyche": addfiles}


class test(Command):
    user_options = []
    description = "Run self-test"

    def initialize_options(self):
        "Function not used!"

    def finalize_options(self):
        "Function not used!"

    def run(self):
        if float(sys.version[0:3]) < 2.7:
            print("tests will not work with python < 2.7, skipping")
            return
        try:
            from Tyche import Test
        except:
            print("unable to run tests")
            raise
        else:
            Test.run()


kwargs['cmdclass'] = {'test' : test}
setup(**kwargs)
