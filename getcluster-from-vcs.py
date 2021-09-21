#!/usr/bin/env python3
#

from pyVim import connect
from pyVmomi import vim
import psycopg2
import datetime

dbconn = psycopg2.connect("dbname=findmyvmdb user=findmyvmuser")
cur_s = dbconn.cursor()
cur_i = dbconn.cursor()

cur_s.execute ("SELECT vc_host,vc_user,vc_pwd,ignore FROM vc WHERE ignore = false ORDER BY vc_host ASC")
rows = cur_s.fetchall()

for row in rows:
  scandate = datetime.datetime.now()
  try: 
    vc_instance = connect.SmartConnectNoSSL(host=row[0],user=row[1],pwd=row[2])
    content = vc_instance.RetrieveContent()
    containter = content.rootFolder
    viewType = [vim.ClusterComputeResource]
    recursive = True
    containerView = content.viewManager.CreateContainerView (containter, viewType, recursive)
    children = containerView.view
    scandate = datetime.datetime.now()

    for child in children:
      #print(row[0], child.name, child.configuration.drsConfig.enabled, child.configuration.dasConfig.enabled)
      cur_i.execute("INSERT INTO clusters VALUES (%s, %s, %s, %s, %s)", 
        (row[0], child.name, scandate, child.configuration.drsConfig.enabled, child.configuration.dasConfig.enabled))
  except Exception as e:
    print(e)


dbconn.commit()
