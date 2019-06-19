# ArinzaArunzal2 service
This program is vulnerable to stack buffer overflow prepered for the CTF called "uniCTf2019" ,it is not a readable-friendly code.
The concept of the program is very simple: it's a home address mananger.
Vulnarable line code is 320 that take 128 bytes instead of 64,combined with no ASLR permit to do a ret2libc.

I was inspired to this video to prepare this vulnerable and exploit(https://www.youtube.com/watch?v=m17mV24TgwY&list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN&index=16)


## OS tested
-Ubuntu server 14.04.6 LTS 32 bit 
-Debian 8 32 bit

## Requirements
- Linux system
- pwn module for python

