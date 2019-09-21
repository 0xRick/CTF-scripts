#!/usr/bin/python
import random 
import json
import hashlib
import binascii
from ecdsa import VerifyingKey, SigningKey, NIST384p
from bottle import route, run, request, debug
from bottle import hook
from bottle import response as resp

'''
Write-up: https://0xrick.github.io/hack-the-box/kryptos/
Description: Script for Hack The Box retired machine kryptos, used to test the secure random number generator function. 
'''

def secure_rng(seed): 
    p = 2147483647
    g = 2255412
    keyLength = 32
    ret = 0
    ths = round((p-1)/2)
    for i in range(keyLength*8):
        seed = pow(g,seed,p)
        if seed > ths:
            ret += 2**i
    return ret

for i in range(15):
    seed = random.getrandbits(128) 
    rand = secure_rng(seed) + 1 
    print rand