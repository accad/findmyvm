#!/usr/bin/env python3
#

import psycopg2
import datetime

header1='/var/www/roweb/wcinc/header.shtml'
header2='/var/www/roweb/findmyvm/index.inc'
footer='/var/www/roweb/wcinc/footer.shtml'

dbconn = psycopg2.connect("dbname=findmyvmdb user=findmyvmuser")
cur = dbconn.cursor()

today = datetime.date.today()

cur.execute ("SELECT * FROM clusters where scandate >= \'%s\'" % today)
rows = cur.fetchall()

with open(header1,'r') as fin:
  print(fin.read())

print ('<table id="myTable"><tr>')
print ('<tr><td>VC</td><td>Cluster</td><td>Scandate</td><td>DRS</td><td>HA</td></tr>')

for row in rows:
	print ('<tr>')
	print ('<td>%s</td>' % row[0])
	print ('<td>%s</td>' % row[1])
	print ('<td>%s</td>' % row[2])
	print ('<td>%s</td>' % row[3])
	print ('<td>%s</td>' % row[4])
	print ('</tr>')

print ('</table>')

with open(footer,'r') as fin:
  print(fin.read())
