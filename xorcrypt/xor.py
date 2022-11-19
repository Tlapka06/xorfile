from ._cryptProtocol import EncryptedData

class XorEncryptedData(EncryptedData):
    def __init__(self, encryptedData):
        self.data = encryptedData
    
    def __init__(self, key, data):
        self.data = self.crypt(key, data)

    def decrypt(self, key):
        return self.crypt(key, self.data)
    
    def crypt(self, key, data):
        if not isinstance(key, bytes) or not isinstance(data, bytes):
            raise TypeError("Key and data should be bytes")
        data_out = bytearray()
        for i in range(len(data)):
            data_out.append(data[i] ^ key[i % len(key)])
        return data_out
