#!/bin/bash

file="7.8.0-amd64.zip"

cp $EXTRAPATH$file $LIVEISOPATH
cd $LIVEISOPATH
unzip $file
rm -f $file

file="isolinux/isolinux.cfg"
filepath=$LIVEISOPATH$file

echo "
label Install
  menu label ^Install
  kernel /install/vmlinuz
  append vga=788 initrd=/install/initrd.gz preseed/file=/cdrom/live/preseed.cfg
" >> $filepath