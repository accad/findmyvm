#!/usr/bin/env python3
#

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

cur.execute("SELECT config_name,* FROM esxi WHERE config_name like '%s' ORDER BY scandate DESC" % (search_string)) 

rows = cur.fetchall()
print ('<table><tr>')
print ('<td><a href=/findmyvm>Go Back</a></td>')
print ('<td>Total results: %d</td>' % (len(rows)))
print ('<td>Query: %s</td>' % (search_string))
print ('</tr></table>')
print ('<br/>')

colnames = [desc[0] for desc in cur.description]

for row in rows:
  print ('<button class="collapsible">%s<br>%s</button>' % (row[0], row[2]))
  print ('<div class="content">')
  print ('<table>')
  for x in range(len(row)):
    rowval = row[x]
    if ( colnames[x] == 'vc' or colnames[x] == 'config_name' ):
      rowval = '<a href=https://' + rowval + ' target=_blank>' + rowval + '</a>'

    #print ("<tr><td>%s</td><td>%s</td></tr>" % (colnames[x], row[x]))
    print ("<tr><td>%s</td><td>%s</td></tr>" % (colnames[x], rowval))
  print ('</table>')
  print ('</div>')

cur.close()
dbconn.close()

with open(footer,'r') as fin:
  print (fin.read())

