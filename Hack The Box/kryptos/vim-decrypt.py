#!/usr/bin/python
import sys

'''
Write-up: https://0xrick.github.io/hack-the-box/kryptos/
Description: Script for Hack The Box retired machine kryptos, used to decrypt vim blowfish encrypted files (in this case rijndael credentials) if the first 8 characters of plaintext are known. 
'''

if len(sys.argv) != 3:
	print "[-] Usage: {} <encrypted file> <plaintext> ".format(sys.argv[0])
	exit()

file = sys.argv[1]
plaintext = sys.argv[2]

def xor(string,key):
	return ''.join(chr(ord(a)^ord(b)) for a, b in zip(string, key))

with open(file,"rb") as f:
	
	temp = f.read(28)

	block1 = f.read(8)
	block2 = f.read(8)
	block3 = f.read(8)
	block4 = f.read(8)
	
	f.close()

key = xor(block1, plaintext)

final = ""
final += xor(block1, key)
final += xor(block2, key)
final += xor(block3, key)
final += xor(block4, key)

print "[+] Decrypted: \n"
print final