#!/bin/bash

echo "
auto eth0
iface eth0 inet static
  address 0.0.0.0
  #netmask x.x.x.x
  #gateway x.x.x.x
  #dns-nameservers x.x.x.x
" >> /etc/network/interfaces