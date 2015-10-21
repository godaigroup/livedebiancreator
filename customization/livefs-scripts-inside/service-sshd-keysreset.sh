#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin

rm -f /etc/ssh/*key*

test=`/usr/bin/dpkg --get-selections | grep -w patch`

apt-get -q -y install patch

echo "74a75,81
> check_keys_avail() {
> if [ ! -e /etc/ssh/ssh_host_dsa_key ]; then
>             dpkg-reconfigure openssh-server
>             fi
> }
> 
> 
79a87
>       check_keys_avail
110a119
>       check_keys_avail
124a134
>       check_keys_avail
" > /etc/init.d/ssh.patch

#cp /etc/init.d/ssh /etc/init.d/ssh.orig
patch /etc/init.d/ssh -i /etc/init.d/ssh.patch
rm -f /etc/init.d/ssh.patch

#echo $test
if [ -z "$test" ];
 then
  echo "not installed - remove patch now"
  apt-get -q -y remove patch
 else
  echo "installed prior - not removing patch"
fi
