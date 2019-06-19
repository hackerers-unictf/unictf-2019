
from pwn import *
from struct import unpack, pack
import sys

def checkonline(ip, port):
    try:
    	r = remote(ip, port)
    	res = r.readuntil(">")
        ari="Arinza"
        aru="Arunza"
        #prima verica
    	r.send("8\n")
    	r.readuntil("?")
    	r.send(ari+"\n")
    	r.readuntil("line")
    	r.send(aru+"\n")
    	r.readuntil(">")
        #seconda verifica
    	r.send("18\n")
    	r.readuntil("0xb773aa32")
    	r.recvline()
        res=r.recvline()
	
    	if not (res.find(ari) and res.find(aru)):
            return False
	    #terza verifica

        r.send("89\n")
        r.readuntil("you?")
        r.send("system\n")
        r.readuntil("address?")
        r.send(ip+"\n")
        r.readuntil("address")
        r.send("127.0.0.1\n")
        r.readuntil("address")
        r.send("00:0c:29:7e:0e:e2")
        return True
    except:
        print "errore"
        return False

if __name__ == '__main__':
    if(len(sys.argv)<2):
        print "inserire IP"
    ip = sys.argv[1]
    port = 12345
    ver=checkonline(ip,port)
    print "verifica=",ver
