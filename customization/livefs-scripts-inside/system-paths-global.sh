#!/bin/bash

sed -i 's/PATH=.*/PATH=\"\/bin:\/sbin\:\/usr\/bin:\/usr\/sbin:\/usr\/local\/bin:\/usr\/local\/sbin\"/' /etc/profile
