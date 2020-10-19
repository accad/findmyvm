#!/usr/bin/env python3
#

import cgi
import re
import psycopg2
import sys

form = cgi.FieldStorage()
dbconn = psycopg2.connect("dbname=findmyvmdb user=findmyvmuser")
cur=dbconn.cursor()


search_string = form["input"].value.strip()

try:
  if form["output"].value:
    output_type = form["output"].value.strip()
except:
  output_type = 'csv'
  
#query = "SELECT scandate FROM vc WHERE vc_host = '%s'" % (search_string)
query = "SELECT scandate FROM vclog WHERE vc_host = '%s' and reason = 'OK' order by scandate desc limit 1" % (search_string)
cur.execute(query)  
scandate = cur.fetchone()[0]

query = "SELECT DISTINCT config_name,config_vmpathname,config_guestfullname,runtime_powerstate,guest_ipaddress,guest_toolsstatus,runtime_host_name,config_memorysizeMB,config_numcpu,parent_name,nic_macaddress,nic_ipaddress FROM vms WHERE vc = '%s' AND scandate >= '%s' " % (search_string, scandate) 
cur.execute(query)
rows = cur.fetchall()

if output_type == 'csv':
  sys.stdout.write('Content-Type: text/csv\n')
  sys.stdout.write('Content-Disposition: attachment; filename=%s.csv\n\n' % (search_string))
  for row in rows:
    line=''
    for xx in range(len(row)):
      line+="%s," % ( row[xx])
    sys.stdout.write(line)
    sys.stdout.write("\n")
else:
  header='/var/www/roweb/wcinc/header.shtml'
  footer='/var/www/roweb/wcinc/footer.shtml'
  print ("Content-Type: text/html\n")
  with open(header,'r') as fin:
    print (fin.read())
  print('<table><tr>')
  colnames = [desc[0] for desc in cur.description]
  for coln in range(len(colnames)):
    print("<td>%s</td>" % (colnames[coln]))
  print ("</tr>")
  for row in rows:
    line='<tr>'
    for xx in range(len(row)):
      line+="<td>%s</td>" % (row[xx])
    line+="</tr>\n"
    print(line)
  print('</table>')
  with open(footer,'r') as fin:
    print (fin.read())


cur.close()
dbconn.close()
