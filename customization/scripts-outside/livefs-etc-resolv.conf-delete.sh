#!/bin/bash

filedest="etc/resolv.conf"
filedest=$LIVEFSPATH$filedest
rm -f $filedest

filedest="run/resolvconf/resolv.conf"
filedest=$LIVEFSPATH$filedest
rm -f $filedest
