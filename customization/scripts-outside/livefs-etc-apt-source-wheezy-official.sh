#!/bin/bash

filesrc="customization/aptsources/wheezy-official.list"
filesrc=$BUILDERPATH$filesrc

filedest="etc/apt/sources.list.d/"
filedest=$LIVEFSPATH$filedest

cp $filesrc $filedest
