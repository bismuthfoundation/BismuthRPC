"""
Crypto keys manager for Bismuth rpcserver
Will eventually be merged with node keys management to avoid duplicate code.

@EggPool
"""

import base64
# import base64, os, getpass, hashlib
# from Crypto import Random

# import os
import hashlib

from Cryptodome.Hash import SHA
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5

from simplecrypt import decrypt, encrypt

__version__ = "0.0.5"


# TODO: maybe keep this class for compatibility, but use polysign instead of direct RSA calls.


class Key:
    """
    Represent a RSA crypto key object and associated methods
    """

    # TODO: Could add a "label" later on
    __slots__ = (
        "verbose",
        "encrypted",
        "privkey",
        "pubkey",
        "address",
        "passphrase",
    )

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.encrypted = False
        self.privkey = ""
        self.pubkey = ""
        self.address = ""
        self.passphrase = None

    @property
    def as_dict(self):
        """
        The core properties as a dict
        """
        return {
            "address": self.address,
            "encrypted": self.encrypted,
            "privkey": self.privkey,
            "pubkey": self.pubkey,
        }

    @property
    def hashed_pubkey(self):
        """
        The pubkey, hashed
        :return: str
        """
        return str(base64.b64encode(self.pubkey.encode("utf-8")).decode("utf-8"))

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
        raise RuntimeError("key.from_dict broken")

    def from_list(self, alist):
        """
        load Keys from the list, returns self so we can chain if needed
        :param alist:
        :return:
        """
        self.address, self.encrypted, self.privkey, self.pubkey = alist
        return self

    def from_privkey(self, privkey):
        """
        imports privkey and recomputes pubkey and address
        :param privkey: privkey PEM format as in privkey.der, including boundaries
        :return:self
        """
        key = RSA.importKey(privkey)
        self.privkey = privkey
        self.pubkey = key.publickey().exportKey().decode("utf-8")
        self.address = hashlib.sha224(key.publickey().exportKey()).hexdigest()
        self.encrypted = False
        return self

    def sign(self, signed_part, base64_output=False):
        """
        Sign a message or transaction with PKCS1_v1_5
        :param signed_part: the message or transaction tuple to sign
        :param base64_output: if True, encodes the signature with b64 (default False)
        :return: String. The signature alone.
        """
        key = RSA.importKey(self.privkey)
        h = SHA.new(str(signed_part).encode("utf-8"))
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(h)
        if base64_output:
            return base64.b64encode(signature)
        else:
            return signature

    def generate(self):
        """
        Generates key pair as well as address, uncrypted
        """
        key = RSA.generate(4096)
        self.privkey = key.exportKey().decode("utf-8")
        """
        TODO: surely we should strip the RSA header and footer -----BEGIN RSA PRIVATE KEY-----\n
        from the data when encrypting, or this may make it easier to brute force.
        """
        self.encrypted = False
        self.pubkey = key.publickey().exportKey().decode("utf-8")
        # address is hash of pubkey
        self.address = hashlib.sha224(self.pubkey.encode("utf-8")).hexdigest()
        return self.as_dict

    def crypt(self, passphrase=""):
        """
        Encodes privkey only with passphrase
        """
        if self.encrypted:
            raise AlreadyEncrypted
        if passphrase == "":
            passphrase = self.passphrase
        if passphrase == "":
            raise NoCryptCredentials
        self.privkey = encrypt(passphrase, data=self.privkey)
        self.encrypted = True
        return self.as_dict

    def decrypt(self, passphrase=""):
        """
        Decodes privkey with passphrase
        """
        if not self.encrypted:
            raise AlreadyEncrypted
        if passphrase == "":
            passphrase = self.passphrase
        if passphrase == "":
            raise NoCryptCredentials
        decrypted = decrypt(passphrase, data=self.privkey)
        if "-----BEGIN RSA PRIVATE KEY-----" not in decrypted:
            raise BadCryptCredentials
        self.privkey = decrypted
        self.encrypted = False
        return self.as_dict


"""
Custom exceptions
"""


class AlreadyEncrypted(Exception):
    code = -32001
    message = "Key is already encrypted"
    data = None


class AlreadyDecrypted(Exception):
    code = -32002
    message = "Key is already decrypted"
    data = None


class NoCryptCredentials(Exception):
    code = -32003
    message = "Crypt credentials required"
    data = None


class BadCryptCredentials(Exception):
    code = -32004
    message = "Wrong crypt credentials"
    data = None


if __name__ == "__main__":
    print("I'm a module, can't run!")
