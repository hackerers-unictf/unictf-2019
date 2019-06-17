from pwn import *
import time

def smartowen4755(host, port):
	result = False
	r = remote(host, port)
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
	r.send("0\n")
	r.close();
	return result
