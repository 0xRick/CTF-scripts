#!/usr/bin/python
import random 
import json
import hashlib
import binascii
from ecdsa import VerifyingKey, SigningKey, NIST384p
from bottle import route, run, request, debug
from bottle import hook
from bottle import response as resp
import requests

'''
Write-up: https://0xrick.github.io/hack-the-box/kryptos/
Description: Script for Hack The Box retired machine kryptos, used to bruteforce the seed.
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

def sign(msg):
    return binascii.hexlify(sk.sign(msg))

num = 1
YELLOW = "\033[93m"
GREEN = "\033[32m"

for i in range(10000):
    expr = "1+1"
    seed = random.getrandbits(128) 
    rand = secure_rng(seed) + 1 
    sk = SigningKey.from_secret_exponent(rand, curve=NIST384p) 
    vk = sk.get_verifying_key() 
    sig = sign(expr) 
    
    req = requests.post('http://127.0.0.1:81/eval', json={'expr': expr, 'sig': sig})
    response = req.text
    if response == "Bad signature":
        print YELLOW + "[-] Attempt " + str(num) + ": failed"
        num += 1
    else:
        print GREEN + "[+] Found the seed: " + str(seed)
        exit()