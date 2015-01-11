import java, javax, warnings

MODE_ECB = 1

b256 = True

### Test for 256 bit support!
key = javax.crypto.spec.SecretKeySpec(' '*32, "AES")
cipher = javax.crypto.Cipher.getInstance("AES")
try:
    cipher.init(javax.crypto.Cipher.ENCRYPT_MODE, key)
    cipher.doFinal(' '*32).tostring()
except java.security.InvalidKeyException:
    b256 = False

if not b256:
    raise ImportError('to be cought')

class AES:
    def __init__(self, key, mode=MODE_ECB):
        assert len(key) in (16, 24, 32)
        assert mode == MODE_ECB
        if len(key) == 32 and not BITS_256:
            raise Exception('Cannot use AES-256. Please install Java Cryptography Extension (JCE) Unlimited Strength Jurisdiction Policy Files for your java version')
        key = javax.crypto.spec.SecretKeySpec(key, "AES")
    def encrypt(self, data):
        cipher = javax.crypto.Cipher.getInstance("AES")
        cipher.init(javax.crypto.Cipher.ENCRYPT_MODE, self.key)
        return cipher.doFinal(data).tostring()
    def decrypt(self, data):
        cipher = javax.crypto.Cipher.getInstance("AES")
        cipher.init(javax.crypto.Cipher.DECRYPT_MODE, self.key)
        return cipher.doFinal(data).tostring()
    

def new(key, mode=MODE_ECB, iv=None):
    return AES(key, mode)

if __name__ == "__main__":
    a = AES(' '*16)
    print a.encrypt(' '*32).encode('hex')
    a = AES(' '*32)
    print a.encrypt(' '*32).encode('hex')
