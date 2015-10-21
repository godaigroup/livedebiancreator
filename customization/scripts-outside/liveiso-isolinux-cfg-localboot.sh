#!/bin/bash

file="isolinux/isolinux.cfg"
filepath=$LIVEISOPATH$file

echo "
label Local HDD
localboot -1
" >> $filepath