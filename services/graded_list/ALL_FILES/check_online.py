from pwn import *

addr = "192.168.1.117"
port = 10010

r = remote(addr, port)
res = r.readuntil('> ')
r.send('referee')
r.send('thischeck')
r.send('0')
r.send('255')
r.send('255')
res = r.readuntil('Hahahh')
print(res)
res = res.splitlines()
res2 = filter(lambda x: 'Your score is: 608' in x, res)
if res2:
	res2 = filter(lambda x: 'referee thischeck 608' in x, res)
	if res2:
		res2 = filter(lambda x: 'Mmhh, puzzled!' in x, res)
		if res2:
			print('Check Success')
		else:
			print('Check Fail')
	else:
		print('Check Fail')
else:
	print('Check Fail')