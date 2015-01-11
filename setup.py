#!python

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
    license=("GPL (+Microsoft Visual C++ 2007 "
             "Redistributable License Agreement)"),
    zip_safe=False,
    platforms="any",
    packages=['Tyche', 'Tyche.Sources',
              'Tyche.Backends', 'Tyche.Backends.Java',
              'Tyche.Backends.Fallback', 'Tyche.Backends.Fallback.pyaes'],
    url='https://github.com/Varbin/Tyche',)

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
