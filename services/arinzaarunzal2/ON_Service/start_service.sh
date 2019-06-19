#!/bin/bash
echo "arinzaarunzal2 starting"
sleep 1
screen -S arinzaarunzal2 socat TCP-LISTEN:12345,reuseaddr,backlog,fork SYSTEM:./arinzaarunzal2
exit 0
