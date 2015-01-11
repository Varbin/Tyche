import os

if os.name == 'java':
    try:
        from Tyche.Backends.Java.AES import *
    except ImportError:
        try:
            from Tyche.Backends.Fallback.AES import *
        except:
            raise SystemError('Your Jython version is outdated. '
                              'Please update or install the Java '
                              'Cryptography Extension (JCE) Unlimited '
                              'Strength Jurisdiction Policy for your '
                              'Java version.')
else:
    try:
        from Crypto.Cipher.AES import *
    except ImportError:
        from Tyche.Backends.Fallback.AES import *
