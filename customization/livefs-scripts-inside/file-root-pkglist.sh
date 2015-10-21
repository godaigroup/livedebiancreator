#!/bin/bash

/usr/bin/dpkg --get-selections | /usr/bin/awk '{print $1}' > /root/pkg.list