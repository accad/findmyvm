#!/usr/bin/env python3
#

import cgi
import re
import psycopg2

regex_ip = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
regex_mac = "^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$"
regex_host = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$";
regex_num = "^[-+]?[0-9]+$"

form = cgi.FieldStorage()
dbconn = psycopg2.connect("dbname=findmyvmdb user=findmyvmuser")
cur=dbconn.cursor()

search_string = form["input"].value.strip()

best_guess = "VM Name"
like_cond = "="
limit_cond = "10"

try:
  if form["limit"].value:
    limit_cond = form["limit"].value
except:
  pass

try: 
  if form["fuzzy"].value:
    fuzzy_search="ON"
    if re.match(regex_ip, search_string):
      query_from = "nic_ipaddress"
      search_string = "%" + search_string + "%;"
      best_guess = "IP Address"
    elif re.match(regex_mac, search_string):
      query_from = "nic_macaddress"
      search_string =  "%" + search_string + "%;"
      best_guess = "MAC Address"
    elif re.match(regex_num, search_string):
      query_from = "parent_name"
      search_string = "_%" + search_string + "%_"
      best_guess = "Deployment ID"
    else:
      query_from = "config_name"
      search_string = "%" + search_string + "%"
except: 
  fuzzy_search="OFF"
  if re.match(regex_ip, search_string):
    query_from = "nic_ipaddress"
    search_string = search_string + ";"
    best_guess = "IP Address"
  elif re.match(regex_mac, search_string):
    query_from = "nic_macaddress"
    search_string =  search_string + ";"
    best_guess = "MAC Address"
  elif re.match(regex_num, search_string):
    query_from = "parent_name"
    search_string = "%_" + search_string + "_%"
    best_guess = "Deployment ID"
    like_cond = 'like' 
  else:
    query_from = "config_name"



header='/var/www/roweb/wcinc/header.shtml'
footer='/var/www/roweb/wcinc/footer.shtml'

print ("Content-Type: text/html\n")

with open(header,'r') as fin:
  print (fin.read())

if fuzzy_search == "ON":
  like_cond = "ILIKE"

cur.execute("SELECT * FROM vms WHERE %s %s '%s' ORDER BY scandate DESC LIMIT %s" % (query_from, like_cond, search_string, limit_cond)) 

rows = cur.fetchall()
print ('<table><tr>')
print ('<td><a href=/findmyvm>Go Back</a></td>')
print ('<td>Total results: %d</td>' % (len(rows)))
print ('<td>Best guess: %s</td>' % (best_guess))
print ('<td>Fuzzy search: %s</td>' % (fuzzy_search))
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
    if (colnames[x] == 'vc'):
      rowval = '<a href=https://' + rowval + ' target=_blank>' + rowval + '</a>'
    if (colnames[x] == 'runtime_host_name'):
      rowval = '<a href=/cgi-bin/findmyvm/esxinfo.py?input=' + rowval + ' target=_blank>' + rowval + '</a>'
    #print ("<tr><td>%s</td><td>%s</td></tr>" % (colnames[x], row[x]))
    print ("<tr><td>%s</td><td>%s</td></tr>" % (colnames[x], rowval))
  print ('</table>')
  print ('</div>')

cur.close()
dbconn.close()

with open(footer,'r') as fin:
  print (fin.read())

