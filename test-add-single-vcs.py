#!/usr/bin/env python3

from pyVim import connect
from pyVmomi import vim
import argparse
import psycopg2

dbconn = psycopg2.connect("dbname=findmyvmdb user=findmyvmuser")
cur=dbconn.cursor()

parser=argparse.ArgumentParser(description='Test VC Connection')
parser.add_argument('-v', help='vCenter Hostname/IP',action='store', required=True)
parser.add_argument('-u', help='Username', action='store', required=True)
parser.add_argument('-p', help='Password', action='store', required=True)
parser.add_argument('-a', help='Add to DB on Success (y/n)', action='store', default='n')
parser.add_argument('-t', help='vCenter Type (default=other)', action='store', default='other')

vc_host=parser.parse_args().v
vc_user=parser.parse_args().u
vc_pass=parser.parse_args().p

vc_yadd = parser.parse_args().a
vc_type = parser.parse_args().t

vci=0

cur.execute('SELECT * FROM vc WHERE vc_host ilike \'%s\'' % (vc_host))

if cur.rowcount != 0 and vc_yadd == 'y' :
  print ("Host already exists in DB, ignoring")
  exit()

try:
  vci=connect.SmartConnectNoSSL(host=vc_host,user=vc_user,pwd=vc_pass)
except:
  print ('Failed %s %s %s' % (vc_host, vc_user, vc_pass))

if vci:
  print ('Success %s %s %s' % (vc_host, vc_user, vc_pass))
  if vc_yadd == 'y':
    cur.execute('INSERT INTO vc VALUES(\'%s\',\'%s\',\'%s\',\'false\',null,\'%s\')' % (vc_host,vc_user,vc_pass,vc_type))
    cur.close()
    dbconn.commit()
    dbconn.close()
    print ("Added to database with type %s" % (vc_type))
