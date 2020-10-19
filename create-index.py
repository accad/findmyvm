#!/usr/bin/env python3
#

import psycopg2
header1='/var/www/roweb/wcinc/header.shtml'
header2='/var/www/roweb/findmyvm/index.inc'
footer='/var/www/roweb/wcinc/footer.shtml'

dbconn = psycopg2.connect("dbname=findmyvmdb user=findmyvmuser")
cur = dbconn.cursor()

cur.execute ("SELECT vc_host,ignore, scandate,type,failcount FROM vc")
rows = cur.fetchall()

with open(header1,'r') as fin:
  print(fin.read())

with open(header2,'r') as fin:
  print(fin.read())


print ('<button class="collapsible">vCenter List (Click to expand)</button>')
print ('<div class="content">')
print ('<br/><br/>')
print ('<table id="myTable"><tr>')
print ('<th onclick="sortTable(0)">vCenter</th><th onclick="sortTable(1)">ScanOK</th>')
print ('<th onclick="sortTable(2)">ScanDate</th><th>Inventory</th>')
print ('<th>ScanLog</th><th onclick="sortTable(3)">Type</th></tr>')

for row in rows:
  print('<tr><td><a href=https://%s target=_blank>%s</a></td>' % (row[0], row[0]))
  accessible='True'
  if row[1]:
    accessible='<mark> False </mark>'
  print('<td>%s</td><td>%s</td>' % (accessible, row[2]))
  print('<td><a href=/cgi-bin/findmyvm/export.py?input=%s>Export</a> / <a href=/cgi-bin/findmyvm/export.py?input=%s&output=table target=_blank>View</a></td>' % ( row[0], row[0]))
  print('<td><a href=/cgi-bin/findmyvm/vclog.py?input=%s>Log</a> %s </td>'  % (row[0], row[4]))
  print('<td>%s</td>' % row[3])
  print('</tr>')

print ('</table>')

with open(footer,'r') as fin:
  print(fin.read())
