#!/bin/bash

apt-get -q -y install ngetty

file="/etc/ngetty/Conf"

echo "tty1=autologin-name=root" >> $file
chmod 600 $file