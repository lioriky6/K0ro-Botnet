from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import os

class RSAcrypto:
    def __init__(self):
        if(os.path.exists("key.key") and os.path.exists("PublicKey.key")):
            self.privateKey = open("key.key", 'rb').read()
            self.publicKey = open("PublicKey.key", 'rb').read()
            self.decryptor = PKCS1_OAEP.new(RSA.import_key(self.privateKey))

        else:
            self.generateKey()
    def generateKey(self):
        with open("key.key", 'wb') as file:
            self.privateKey = RSA.generate(1024)
            file.write(self.privateKey.exportKey())
            self.publicKey = self.privateKey.publickey()
        with open("PublicKey.key", 'wb') as file:
            file.write(self.publicKey.exportKey())

        self.decryptor = PKCS1_OAEP.new(RSA.import_key(self.privateKey))

    def getPrivateKey(self):
        with open("key.key", 'rb') as file:
            return file.read()

    def getPubKey(self):
        with open("PublicKey.key", 'rb') as file:
            return file.read()

    def decrypt(self, msg):
        return self.decryptor.decrypt(msg)

