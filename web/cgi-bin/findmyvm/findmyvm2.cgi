#!/usr/bin/env python3
#

from cgi import FieldStorage
from re import match
import psycopg2
from json import dumps

regex_ip = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
regex_mac = "^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$"
regex_host = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$";
regex_num = "^[-+]?[0-9]+$"

form = FieldStorage()
dbconn = psycopg2.connect("dbname=findmyvmdb user=findmyvmuser")
cur=dbconn.cursor()
cur2=dbconn.cursor()

search_string = form["input"].value.strip()

best_guess = "VM Name"
like_cond = "like"
limit_cond = "3"

try:
  if form["limit"].value:
    limit_cond = form["limit"].value
except:
  pass

try: 
  if form["fuzzy"].value:
    fuzzy_search="ON"
    if match(regex_ip, search_string):
      query_from = "nic_ipaddress"
      search_string = "%" + search_string + "%;"
      best_guess = "IP Address"
    elif match(regex_mac, search_string):
      query_from = "nic_macaddress"
      search_string =  "%" + search_string + "%;"
      best_guess = "MAC Address"
    elif match(regex_num, search_string):
      query_from = "parent_name"
      search_string = "_%" + search_string + "%_"
      best_guess = "Deployment ID"
    else:
      query_from = "config_name"
      search_string = "%" + search_string + "%"
except: 
  fuzzy_search="OFF"
  if match(regex_ip, search_string):
    query_from = "nic_ipaddress"
    search_string = search_string + ";"
    best_guess = "IP Address"
  elif match(regex_mac, search_string):
    query_from = "nic_macaddress"
    search_string =  search_string + ";"
    best_guess = "MAC Address"
  elif match(regex_num, search_string):
    query_from = "parent_name"
    search_string = "%_" + search_string + "_%"
    best_guess = "Deployment ID"
    like_cond = 'like' 
  else:
    query_from = "config_name"

if fuzzy_search == "ON":
  like_cond = "ILIKE"

print ("Content-Type: application/json\n")
cur.execute("SELECT * FROM vms WHERE %s %s '%s' ORDER BY scandate DESC LIMIT %s" % (query_from, like_cond, search_string, limit_cond)) 

rows = cur.fetchall()

total_rows = len(rows)
current_row = 0 

colnames = [desc[0] for desc in cur.description]

jout = {}
jout['total'] = total_rows
jout['query'] = search_string
jout['best_guess'] = best_guess
jout['fuzzy'] = fuzzy_search
jout['results'] = {}

for row in rows:
  current_row +=1
  jout['results'][current_row]={}
  for x in range(len(row)):
    rowval = row[x]
    jout['results'][current_row][colnames[x]]=rowval
    if colnames[x] == 'runtime_host_name':
      cur2.execute("SELECT assettag from esxi where config_name = '%s' limit 1" % (rowval))
      assettag = cur2.fetchone()
      jout['results'][current_row]['assettag']=assettag

print (dumps(jout, indent=4, default=str))

cur.close()
dbconn.close()


