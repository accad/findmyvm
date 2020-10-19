#!/usr/bin/env python3
#

import argparse

p=argparse.ArgumentParser()
p.add_argument('-s','--server',action='store',required=True)
p.add_argument('-u','--username',action='store',required=True)
p.add_argument('-p','--password',action='store',required=True)
p.add_argument('--api',action='store',default='2.6.1')
p.add_argument('-o','--output',action='store',required=True)

import urllib3
import requests
import json

urllib3.disable_warnings()

payload = {
        '_max_results': '10000',
        '_return_fields+': 'extattrs',
}

url = 'https://' + p.parse_args().server + '/wapi/v' + p.parse_args().api  + '/network'
req4 = requests.get(url,auth=(p.parse_args().username, p.parse_args().password),verify=False,data=payload)

url = 'https://' + p.parse_args().server + '/wapi/v' + p.parse_args().api  + '/ipv6network'
req6 = requests.get(url,auth=(p.parse_args().username, p.parse_args().password),verify=False,data=payload)

content = req4.json() + req6.json()

f = open(p.parse_args().output,'w')
json.dump(content, f, indent=4) 

f.close()
