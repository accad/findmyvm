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

  try: # CONNECT_VC
    vc_instance = connect.SmartConnectNoSSL(host=row[0],user=row[1],pwd=row[2])
    content = vc_instance.RetrieveContent()
    containter = content.rootFolder
    viewType = [vim.VirtualMachine]
    recursive = True
    containerView = content.viewManager.CreateContainerView (containter, viewType, recursive)
    children = containerView.view

    for child in children: # FOR_CHILD

      try: # GET_CHILD
        summary = child.summary
        cpn = "None"
        if child.parent:
          cpn = str(child.parent.name)
        macs = ''
        ipall = ''

        try: # GET_IP
          for nic in child.guest.net:

            if '02:00:4c:4f:4f:50' in nic.macAddress: ##NPCAP LOOPBACK
              pass
            elif len(macs) < 2030:
              macs += nic.macAddress + ";"
            else:
             pass

            if ( summary.runtime.powerState == 'poweredOn' ):
              addresses = nic.ipConfig.ipAddress
              for adr in addresses:
               if ":" in adr.ipAddress or "169.254." in adr.ipAddress:
                 pass
               elif len(ipall) < 2033:
                 ipall += adr.ipAddress + ';'
               else:
                 pass
            else:
              ipall = '0.0.0.0;'

        except Exception as e1: # GET_IP
          print ("E1: Failed network add for %s %s" %(summary.vm, row[0]))
          print (e1)
          pass

        storage_bytes = 0
        if summary.storage.committed:
          storage_bytes = summary.storage.committed
                  
        cur_i.execute ("INSERT INTO vms VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )", # 18
            (scandate, str(summary.vm), summary.config.name, summary.config.vmPathName, summary.config.guestFullName, summary.runtime.powerState,
             summary.guest.ipAddress, summary.guest.toolsStatus, str(summary.runtime.host.name), summary.config.memorySizeMB, summary.config.numCpu, row[0],
             cpn, macs, ipall, summary.config.uuid, summary.config.instanceUuid, storage_bytes ))

      except Exception as e2: # GET_CHILD
        print ("E2: Failed to add %s %s" % ( str(summary.vm), summary.config.name ) )
        print (e2)
        pass

  # FOR_CHILD

  except Exception as e3: # CONNECT_VC
    cur_i.execute("UPDATE vc SET ignore = True WHERE vc_host = '" + row[0] + "'")
    print ("E3: %s" % (row[0]))
    print (e3)
    pass

  cur_i.execute("UPDATE vc SET scandate = %s WHERE vc_host = %s", (scandate,row[0]))  
  dbconn.commit()
