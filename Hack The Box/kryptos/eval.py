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
import sys

'''
Write-up: https://0xrick.github.io/hack-the-box/kryptos/
Description: Script for Hack The Box retired machine kryptos, used to evaluate expression depending on the given seed. 
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

def sign(sk,msg):
    return binascii.hexlify(sk.sign(msg))

def eval(seed,expr): 
	rand = secure_rng(seed) + 1 
	sk = SigningKey.from_secret_exponent(rand, curve=NIST384p) 
	vk = sk.get_verifying_key() 
	sig = sign(sk,expr)
	req = requests.post('http://127.0.0.1:81/eval', json={'expr': expr, 'sig': sig})
	response = req.text
	print response

if len(sys.argv) != 3 :
	print "Usage: {} <seed> <expression>".format(sys.argv[0])
	exit()
else:
	seed = int(sys.argv[1])
	expr = sys.argv[2]
	eval(seed,expr)