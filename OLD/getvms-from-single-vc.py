#!/usr/bin/env python3
#

from pyVim import connect
from pyVmomi import vim
import psycopg2
import datetime
import argparse 

scandate = datetime.datetime.now()
dbconn = psycopg2.connect("dbname=findmyvmdb user=findmyvmuser")
cur_s = dbconn.cursor()
cur_i = dbconn.cursor()

p=argparse.ArgumentParser()
p.add_argument('-v',action='store',required=True)
p.add_argument('-t',action='store',default="y")
p.add_argument('-d',action='store',default="y")

vc_host=p.parse_args().v
script_debug=p.parse_args().d
script_test=p.parse_args().t

cur_s.execute("SELECT vc_user, vc_pwd FROM vc WHERE vc_host = \'%s\'" % (vc_host))
xrows = cur_s.fetchone()
vc_user = xrows[0]
vc_pwd = xrows[1]


vc_instance = connect.SmartConnectNoSSL(host=vc_host,user=vc_user,pwd=vc_pwd)
print (vc_instance)
content = vc_instance.RetrieveContent()
containter = content.rootFolder
viewType = [vim.VirtualMachine]
recursive = True
containerView = content.viewManager.CreateContainerView (containter, viewType, recursive)
children = containerView.view

for child in children:

  storage_bytes = 0
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
      else:
        macs += nic.macAddress + ";"
      addresses = nic.ipConfig.ipAddress
      for adr in addresses:
        if ":" in adr.ipAddress or "169.254." in adr.ipAddress or "172." in adr.ipAddress or "192.168." in adr.ipAddress:
          pass
        else:
          ipall += adr.ipAddress + ';'

  except:
    pass


  if script_test == "y":
    try:
      print ("DEBUG: " + str(summary.vm))
      print ("DEBUG VM: " + summary.config.name)
      print ("DEBUG IP: " + ipall)
      print ("DEBUG MAC: " + macs)
      print ("DEBUG CPN: " + c_p_n)
      print ("DEBUG UUID " + summary.config.uuid)
      print ("DEBUG UUID " + summary.config.instanceUuid)
      storage_bytes = summary.storage.committed
      #cur_i.execute("INSERT INTO vms_test VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
      print("INSERT INTO vms_test VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
          (scandate, str(summary.vm), summary.config.name, summary.config.vmPathName, summary.config.guestFullName, summary.runtime.powerState, summary.guest.ipAddress,
           summary.guest.toolsStatus, str(summary.runtime.host.name), summary.config.memorySizeMB, summary.config.numCpu,
           vc_host, c_p_n, macs, ipall, summary.config.uuid, summary.config.instanceUuid, storage_bytes ))
    except Exception as e:
      print("Failed to add %s" % ( summary.config.name ))
      print (e)
      pass
  else:
    cur_i.execute("INSERT INTO vms VALUES     (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )", 
      (scandate, str(summary.vm), summary.config.name, summary.config.vmPathName, summary.config.guestFullName, summary.runtime.powerState, 
       summary.guest.ipAddress,summary.guest.toolsStatus, str(summary.runtime.host.name), summary.config.memorySizeMB, summary.config.numCpu, 
       vc_host, c_p_n, macs, ipall, summary.config.uuid.encode(), summary.config.instanceUuid.encode(), summary.storage.committed ))
    cur_i.execute("UPDATE vc SET scandate = %s, ignore = False, failcount = 0 WHERE vc_host = %s", (scandate,vc_host))


  dbconn.commit()

