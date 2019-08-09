#!/usr/bin/python
from __future__ import division
import base64
import hashlib
import os
import six
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CFB8

'''
Write-up : https://0xrick.github.io/hack-the-box/fortune/

pgadmin4 dba password decryption script from Hack The Box - Fortune, Functions are taken from pgadmin4 - crypto.py : https://github.com/postgres/pgadmin4/blob/master/web/pgadmin/utils/crypto.py
'''

padding_string = b'}'
iv_size = AES.block_size // 8


def pad(key):
    """Add padding to the key."""

    if isinstance(key, six.text_type):
        key = key.encode()

    # Key must be maximum 32 bytes long, so take first 32 bytes
    key = key[:32]

    # If key size is 16, 24 or 32 bytes then padding is not required
    if len(key) in (16, 24, 32):
        return key

    # Add padding to make key 32 bytes long
    return key.ljust(32, padding_string)

def decrypt(ciphertext, key):
    """
    Decrypt the AES encrypted string.

    Parameters:
        ciphertext -- Encrypted string with AES method.
        key        -- key to decrypt the encrypted string.
    """

    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:iv_size]

    cipher = Cipher(AES(pad(key)), CFB8(iv), default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext[iv_size:]) + decryptor.finalize()

ciphertext = raw_input("hash : ")
key = raw_input("key : ")
password = decrypt(ciphertext,key)

print "[*] Password : " + password
