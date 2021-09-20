#!/usr/bin/env python3
#

from pyVim import connect
from pyVmomi import vim
import psycopg2
import datetime

#scandate = datetime.datetime.now()
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
    viewType = [vim.VirtualMachine]
    recursive = True
    containerView = content.viewManager.CreateContainerView (containter, viewType, recursive)
    children = containerView.view

    for child in children:
      summary = child.summary
      c_p_n = "None"
      if child.parent:
        c_p_n = str(child.parent.name)

      macs = ''
      ipall = ''

      try:
        for nic in child.guest.net:

          if '02:00:4c:4f:4f:50' in nic.macAddress: ##NPCAP LOOPBACK 
            pass
          elif len(macs) < 2030:
            macs += nic.macAddress + ";"
          else:
            pass

          addresses = nic.ipConfig.ipAddress

          for adr in addresses:
            if ":" in adr.ipAddress or "169.254." in adr.ipAddress or "172." in adr.ipAddress or "192.168." in adr.ipAddress:
              pass
            elif len(ipall) < 2033:
              ipall += adr.ipAddress + ';'
            else:
              pass
      except:
        pass

      cur_i.execute("INSERT INTO vms VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (scandate, str(summary.vm), summary.config.name, summary.config.vmPathName, summary.config.guestFullName, summary.runtime.powerState, summary.guest.ipAddress, 
         summary.guest.toolsStatus, str(summary.runtime.host.name), summary.config.memorySizeMB, summary.config.numCpu,
         row[0], c_p_n, macs, ipall, summary.config.uuid, summary.config.instanceUuid ))

  except Exception as e:
    cur_i.execute("UPDATE vc SET ignore = True WHERE vc_host = '" + row[0] + "'")
    print (row[0], e)

  cur_i.execute("UPDATE vc SET scandate = %s WHERE vc_host = %s", (scandate,row[0]))
  dbconn.commit()
  

