#!/usr/bin/env python
#
import socket

print socket.gethostbyname('accadn.drm.lab.emc.com')
print socket.gethostbyname('10.141.61.73')
try:
  print socket.gethostbyname('garbage')
except:
  print "not a host"

