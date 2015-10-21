#!/bin/bash

filedest="run/resolvconf/resolv.conf"
filedest=$LIVEFSPATH$filedest
rm -f $filedest

filedest="etc/resolv.conf"
filedest=$LIVEFSPATH$filedest
rm -f $filedest
ln -s /etc/resolvconf/run/resolv.conf $filedest
