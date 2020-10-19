#!/usr/bin/env python3
#

from pyVim import connect
from pyVmomi import vim
import psycopg2
import datetime

dbconn = psycopg2.connect("dbname=findmyvmdb user=findmyvmuser")
cur_s = dbconn.cursor()
cur_i = dbconn.cursor()

cur_s.execute ("SELECT vc_host,vc_user,vc_pwd,ignore FROM vc WHERE ignore = false")
rows = cur_s.fetchall()

for row in rows:

  try:
    vc_instance = connect.SmartConnectNoSSL(host=row[0],user=row[1],pwd=row[2])
    content = vc_instance.RetrieveContent()
    containter = content.rootFolder
    viewType = [vim.HostSystem]
    recursive = True
    containerView = content.viewManager.CreateContainerView (containter, viewType, recursive)
    children = containerView.view
    scandate = datetime.datetime.now()

    for child in children:

      summary = child.summary
      hw = child.hardware

      #print(summary.config.name)

      _serviceTag = 'none'
      for _data in child.hardware.systemInfo.otherIdentifyingInfo:
        if _data.identifierType.key == 'ServiceTag':
          _serviceTag = _data.identifierValue 


      ipAddress = '';
      vmkCount=0

      try:
        for vmk in child.config.network.vnic:
          if vmkCount < 9:  
            ipAddress += vmk.spec.ip.ipAddress + ';'
            vmkCount += 1
          else:
            pass
      except:
        pass

      try:
        _biosVersion = hw.biosInfo.biosVersion
        _biosRelease = hw.biosInfo.releaseDate
      except:
        _biosVersion = 'unknown'
        _biosRelease = 0

      #print       ("INSERT INTO esxi VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
      cur_i.execute("INSERT INTO esxi VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
        ( scandate, row[0], str(summary.host), summary.hardware.model, summary.hardware.vendor, summary.config.name, 
          summary.config.product.fullName,summary.overallStatus,child.hardware.systemInfo.uuid, _serviceTag,  
          hw.memorySize, _biosVersion, _biosRelease,ipAddress
        ))

  except Exception as e:
    print(e, row[0], vmkCount, ipAddress)
    pass

dbconn.commit()
dbconn.close()
