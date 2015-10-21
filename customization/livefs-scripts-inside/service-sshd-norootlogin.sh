#!/bin/bash

filepath="/etc/ssh/sshd_config"

sed -i "s/PermitRootLogin yes/PermitRootLogin no/" $filepath