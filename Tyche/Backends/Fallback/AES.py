from Tyche.Backends.Fallback.pyaes import AESModeOfOperationECB


MODE_ECB = 1

class AES(object):
    def __init__(self, key, mode=MODE_ECB, iv=None):
        assert mode == MODE_ECB  # this is just a fallback - no more
        self._aes = AESModeOfOperationECB(key)
    def encrypt(self, data):
        return self._aes.encrypt(data)

    def decrypt(self, data):
        return self._aes.decrypt(data)

def new(key, mode=MODE_ECB):
    return AES(key, mode)
