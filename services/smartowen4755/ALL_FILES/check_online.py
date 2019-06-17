from pwn import *
import time

addr = "192.168.1.117"
port = 12397

result = False
r = remote(addr, port)
res = r.readuntil('>')
r.send("1\n")
res = r.readuntil('>')
res = res.splitlines()
res = filter(lambda x: 'Door Open' in x, res)
if res:
	r.send("1\n")
	res = r.readuntil('>')
	r.send("9\n")
	res = r.readuntil('>')
	res = res.splitlines()
	res = filter(lambda x: 'Door Closed' in x, res)
	if res:
		r.send("3\n")
		res = r.readuntil('Celsius')
		r.send("122\n")
		res = r.readuntil('>')
		r.send("9\n")
		res = r.readuntil('>')
		res = res.splitlines()
		res = filter(lambda x: 'Temperature setted on: 122' in x, res)
		if res:
			r.send("5\n")
			res = r.readuntil('Max')
			r.send("2\n")
			res = r.readuntil('>')
			r.send("6\n")
			res = r.readuntil(':')
			r.send("1\n")
			res = r.readuntil('>')
			r.send("7\n")
			time.sleep(1)
			res = r.readuntil('>')
			res = res.splitlines()
			res = filter(lambda x: 'Remaining:' in x, res)
			result = True
if result:
	print("Check Success")	
else:
	print("Check_Fail")
r.send("0\n")
r.close();