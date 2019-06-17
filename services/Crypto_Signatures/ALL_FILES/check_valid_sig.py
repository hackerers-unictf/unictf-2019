from pwn import *
import csv 

ip = "192.168.1.117"
port = 46325

with open('signatures.csv') as fd:
	incsv = csv.reader(fd)
	for row in incsv:
		s = remote(ip, port)
		res = s.readuntil('form: ')
		print(res)
		s.send(",".join(row)+'\n')
		res = s.readall()
		print(res)
		s.close()