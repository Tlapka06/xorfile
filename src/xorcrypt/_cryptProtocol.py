from abc import abstractmethod, abstractproperty
from typing import Protocol

class EncryptedData(Protocol):
    @abstractmethod
    def __init__(self, encryptedData):
        # save excryptedData as ... (real suprise) encrypted data
        # it can also perform some integrity checks
        raise NotImplementedError
    
    @abstractmethod
    def __init__(self, key, data):
        # encrypt by some algorithm
        raise NotImplementedError
    
    @abstractmethod
    def decrypt(self, key) -> bytearray:
        # decrypts and returns data
        raise NotImplementedError