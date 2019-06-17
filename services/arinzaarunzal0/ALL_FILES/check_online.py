from pwn import *

addr = "192.168.1.117"
port = 18321
success = False

r = remote(addr, port)
res = r.readuntil('user:')
print(res)
r.send("referee\n")
res = r.readuntil('>')
print(res)
r.send("2\n")
res = r.readuntil('read?')
print(res)
r.send("0\n")
res = r.readuntil('>')
print(res)
res = res.splitlines()
res = filter(lambda x: 'Hi, my name is referee' in x, res)
if res:
	r.send("6\n")
	res = r.readuntil('>>')
	print(res)
	r.send("Hi8342DHD34gjsW\n")
	res = r.readuntil('INTRUDEEER!!')
	res = res.splitlines()
	res = filter(lambda x: 'Hi Hawk, insert your root password' in x, res)
	if res:
		success = True
r.send("7\n")
if success:
	print("Check_Success")
else:
	print("Check_Fail")
r.close();
