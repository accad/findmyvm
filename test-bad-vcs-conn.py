#!/usr/bin/env python3

from pyVim import connect
from pyVmomi import vim
import psycopg2
import os
import datetime

dbconn = psycopg2.connect("dbname=findmyvmdb user=findmyvmuser")
cur_s = dbconn.cursor()
cur_i = dbconn.cursor()
cur_s.execute('SELECT vc_host,vc_user,vc_pwd,failcount FROM vc WHERE failcount BETWEEN 2 AND 19 ORDER BY vc_host');
rows=cur_s.fetchall()

for row in rows:

  failcount=row[3]
  failcount+=1
  vci=0
  scandate = datetime.datetime.now()

  try:
    #  ping -c 1 -q -W 2 -n accadn.drm.lab.emc.com 2>&1 > /dev/null
    pingresponse = os.system("ping -q -W 2 -n -c 1 " + row[0] + " 2>&1 > /dev/null" )
    if pingresponse == 0:
      vci=connect.SmartConnectNoSSL(host=row[0],user=row[1],pwd=row[2],connectionPoolTimeout=30)
  except:
    print (row[0])
    pass
    

  if vci:
    cur_i.execute('UPDATE vc SET ignore = false, failcount = 0 WHERE vc_host = \'%s\'' % row[0])
    cur_i.execute('INSERT INTO vclog VALUES ( \'%s\', \'%s\', \'%s\', \'%s\' )' % ( row[0], scandate, 't', 'OK'))
  elif pingresponse == 0:
    cur_i.execute('UPDATE vc SET ignore = true, failcount = %s WHERE vc_host = \'%s\'' % (failcount, (row[0])))
    cur_i.execute('INSERT INTO vclog VALUES ( \'%s\', \'%s\', \'%s\', \'%s\' )' % ( row[0], scandate, 'f', 'Connection Failed'))
  else:
    cur_i.execute('UPDATE vc SET ignore = true, failcount = %s WHERE vc_host = \'%s\'' % (failcount, (row[0])))
    cur_i.execute('INSERT INTO vclog VALUES ( \'%s\', \'%s\', \'%s\', \'%s\' )' % ( row[0], scandate, 'f', 'PING Failed'))
  

dbconn.commit()
