#!/usr/bin/env python3
#
# vclog

import cgi
import psycopg2

form = cgi.FieldStorage()
dbconn = psycopg2.connect("dbname=findmyvmdb user=findmyvmuser")
cur=dbconn.cursor()

search_string = form["input"].value.strip()

header='/var/www/roweb/wcinc/header.shtml'
footer='/var/www/roweb/wcinc/footer.shtml'

print ("Content-Type: text/html\n")

with open(header,'r') as fin:
  print (fin.read())

cur.execute("SELECT scandate,good,reason FROM vclog WHERE vc_host = '%s' ORDER BY scandate DESC" % (search_string)) 

rows = cur.fetchall()
print ('<table><tr>')
print ('<td><a href=/findmyvm>Go Back</a></td>')
print ('<td>Total results: %d</td>' % (len(rows)))
print ('<td>Query: %s</td>' % (search_string))
print ('</tr></table>')
print ('<br/>')

colnames = [desc[0] for desc in cur.description]

print ("<table>")

for row in rows:
  print ("  <tr>")
  for x in range(len(row)):
    print("    <td>%s</td>" % row[x])
  print("  </tr>")

print ("</table>")
 
cur.close()
dbconn.close()

with open(footer,'r') as fin:
  print (fin.read())

