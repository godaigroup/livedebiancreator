#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin

##/usr/sbin/update-rc.d  remove
##/usr/sbin/update-rc.d  disable

update-rc.d acct disable
update-rc.d apache2 disable
update-rc.d binfmt-support disable
update-rc.d cron disable
update-rc.d fglrx-atieventsd disable
update-rc.d libvirt-bin disable
update-rc.d libvirt-guests disable
update-rc.d mcstrans disable
update-rc.d nginx disable
update-rc.d ntop disable
update-rc.d nvidia-kernel disable
update-rc.d openafs-client disable
update-rc.d owserver disable
update-rc.d restorecond disable
update-rc.d rsync disable
update-rc.d samba disable
update-rc.d samhain disable
update-rc.d saned disable
update-rc.d sendmail disable
update-rc.d slim disable
update-rc.d snort disable
update-rc.d ssh disable
update-rc.d stunnel4 disable
update-rc.d udftools disable
update-rc.d virtualbox disable
update-rc.d vsftpd disable