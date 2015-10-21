#!/bin/bash

apt-get -q -y install ngetty

sed -e '/getty/ s/^#*/#/' -i /etc/inittab

sed -i '/6:23/a ng:2345:respawn:/sbin/ngetty 1 2 3 4 5 6' /etc/inittab
