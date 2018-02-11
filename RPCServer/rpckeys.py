"""
Crypto keys manager for Bismuth rpcserver
Will eventually be merged with node keys management to avoid duplicate code.

@EggPool
"""

#import base64, os, getpass, hashlib
#from Crypto import Random
#from simplecrypt import decrypt
#import os
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES


__version__ = "0.0.2"


class Key:
    """
    Represent a crypto key object and associated methods
    """
    
    # TODO: Could add a "label" later on
    __slots__ = ('verbose', 'encrypted', 'privkey', 'pubkey', 'address', 'IV', 'passphrase')
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.encrypted = False
        self.privkey = ''
        self.pubkey = ''
        self.address = ''
        self.IV = None
        self.passphrase = None

    @property
    def as_dict(self):
        """
        The core properties as a dict
        """
        return {"address":self.address, "encrypted":self.encrypted, "privkey":self.privkey, "pubkey":self.pubkey}

    @property
    def as_list(self):
        """
        The core properties as a list
        """
        return [self.address, self.encrypted, self.privkey, self.pubkey]

    def from_dict(self, adict):
        """
        load Keys from the dict, returns self so we can chain if needed
        """
        # TODO: broken!
        """
        for key, value in adict.values():
            self.key = value
        return self
        """

    def generate(self):
        """
        Generates key pair as well as address, uncrypted
        """
        key = RSA.generate(4096)
        self.privkey = key.exportKey().decode("utf-8")
        """
        TODO: surely we sould strip the RSA header and footer -----BEGIN RSA PRIVATE KEY-----\n
        from the data when encrypting, or this makes it easier to brute force.
        """
        self.encrypted = False
        self.pubkey = key.publickey().exportKey().decode("utf-8")
        # address is hash of pubkey
        self.address = hashlib.sha224(self.pubkey.encode("utf-8")).hexdigest()
        return self.as_dict

    def crypt(self, IV='', passphrase=''):
        """
        Encodes privkey only with IV and passphrase
        """
        if self.encrypted:
            raise AlreadyEncrypted
        if IV=='' or passphrase=='':
            IV = self.IV
            passphrase = self.passphrase
        if IV=='' or passphrase=='':
            raise NoCryptCredentials
        # fixed length key is needed, use hash
        key = hashlib.sha256(passphrase.encode("utf-8")).digest()
        mode = AES.MODE_CBC
        encryptor = AES.new(key, mode, IV=IV)
        # TODO : strip header/footer
        # Has to be a multiple of 16
        extra = len(self.privkey) % 16        
        self.privkey += ' ' * (16-extra)
        print("clear",self.privkey,"*",len(self.privkey))
        self.privkey  = encryptor.encrypt(self.privkey)
        self.encrypted = True
        return self.as_dict

    def decrypt(self, IV='', passphrase=''):
        """
        Decodes privkey with IV and passphrase
        """
        # TODO: some code here to factorize.
        if not self.encrypted:
            raise AlreadyEncrypted
        if IV=='' or passphrase=='':
            IV = self.IV
            passphrase = self.passphrase
        if IV=='' or passphrase=='':
            raise NoCryptCredentials
        # fixed length key is needed, use hash
        key = hashlib.sha256(passphrase.encode("utf-8")).digest() # TODO: we could store key once
        mode = AES.MODE_CBC
        decryptor = AES.new(key, mode, IV=IV)
        # TODO: reinject header/footer
        self.privkey  = decryptor.decrypt(self.privkey).strip()
        self.encrypted = False
        return self.as_dict


"""
Custom exceptions
"""


class AlreadyEncrypted(Exception):
    code = -32001
    message = 'Key is already encrypted'
    data = None


class AlreadyDecrypted(Exception):
    code = -32002
    message = 'Key is already decrypted'
    data = None


class NoCryptCredentials(Exception):
    code = -32003
    message = 'Crypt credentials required'
    data = None
    

if __name__ == "__main__":
    print("I'm a module, can't run!")
