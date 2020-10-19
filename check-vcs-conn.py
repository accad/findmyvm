#!/usr/bin/env python3

from pyVim import connect
from pyVmomi import vim
import psycopg2
import cgi
import os

dbconn = psycopg2.connect("dbname=findmyvmdb user=findmyvmuser")
cur=dbconn.cursor()
form = cgi.FieldStorage()

vc_host = form["input"].value.strip()

cur.execute("SELECT vc_user, vc_pwd FROM vc WHERE vc_host = \'%s\'" % (vc_host))
rows = cur.fetchone()

vc_user = rows[0]
vc_pwd = rows[1]

try:
  pingresponse = os.system("ping -q -W 2 -n -c 1 " + vc_host + " 2>&1 > /dev/null" )
  if pingresponse == 0:
    vci=connect.SmartConnectNoSSL(host=vc_host,user=vc_user,pwd=vc_pwd,connectionPoolTimeout=30)
    print ('Success %s %s %s' % (vc_host, vc_user, vc_pwd))
  else:
    print ('PING Failed %s %s %s' % (vc_host, vc_user, vc_pwd))
except:
  print ('Connection Failed %s %s %s' % (vc_host, vc_user, vc_pwd))

