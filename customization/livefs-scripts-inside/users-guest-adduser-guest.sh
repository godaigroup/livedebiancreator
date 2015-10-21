#!/bin/bash

USER="guest"
PASS="guest"

expect <<EOF
spawn adduser $USER
expect "UNIX password:"
send "$PASS\r"
expect "UNIX password:"
send "$PASS\r"
expect "[]:"
send "\r"
expect "[]:"
send "\r"
expect "[]:"
send "\r"
expect "[]:"
send "\r"
expect "[]:"
send "\r"
expect "information correct?"
send "\r"
expect eof
exit
EOF