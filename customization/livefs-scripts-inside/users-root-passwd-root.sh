#!/bin/bash

NEWPASS="root"

expect <<EOF
spawn passwd
expect "UNIX password:"
send "$NEWPASS\r"
expect "UNIX password:"
send "$NEWPASS\r"
expect eof
exit
EOF