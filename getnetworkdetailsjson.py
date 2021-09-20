#!/usr/bin/env python3
#

import argparse

p=argparse.ArgumentParser()
p.add_argument('-s','--server',action='store',required=True)
p.add_argument('-u','--username',action='store',required=True)
p.add_argument('-p','--password',action='store',required=True)
p.add_argument('--api',action='store',default='2.6.1')
p.add_argument('-o','--output',action='store',required=True)
p.add_argument('-n','--network',action='store',required=True)

import urllib3
import requests
import json

urllib3.disable_warnings()

payload = {
        '_max_results': '10000',
        '_return_fields+': 'extattrs',
}

url = 'https://' + p.parse_args().server + '/wapi/v' + p.parse_args().api  + '/ipv4address'
req4params = {'network' : p.parse_args().network}
req4 = requests.get(url,auth=(p.parse_args().username, p.parse_args().password),verify=False,params=req4params)

#f = open(p.parse_args().output,'w')
#json.dump(req4, f, indent=4) 
#f.close()

print(req4.text)

