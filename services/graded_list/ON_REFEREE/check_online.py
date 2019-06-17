from pwn import *

def unictf_graded_list(host, port):
	r = remote(host, port)
	res = r.readuntil('>')
	r.send('referee\n')
	res = r.readuntil('>')
	r.send('thischeck\n')
	res = r.readuntil('>')
	r.send('0\n')
	res = r.readuntil('>')
	r.send('255\n')
	res = r.readuntil('>')
	r.send('255\n')
	res = r.readuntil('Hahahh')
	res = res.splitlines()
	res2 = filter(lambda x: 'Your score is: 608' in x, res)
	if res2:
		res2 = filter(lambda x: 'referee thischeck 608' in x, res)
		if res2:
			res2 = filter(lambda x: 'Mmhh, puzzled!' in x, res)
			if res2:
				return True
	return False
