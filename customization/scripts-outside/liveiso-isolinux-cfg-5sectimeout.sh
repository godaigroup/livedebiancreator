#!/bin/bash

file="isolinux/isolinux.cfg"
filepath=$LIVEISOPATH$file

sed -i "s/timeout 10/timeout 50/" $filepath