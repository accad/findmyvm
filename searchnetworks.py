#!/usr/bin/env python3
#

import argparse

p=argparse.ArgumentParser()
p.add_argument('-i','--input',action='store',required=True)
p.add_argument('-s','--search',action='store',required=True)
p.add_argument('-t','--html',action='store_true')

import json
import json2table
import ipaddress

f=open(p.parse_args().input,'r')
json_data = json.load(f)

for i in range(len(json_data)):
    if ipaddress.ip_address(p.parse_args().search) in ipaddress.ip_network(json_data[i]["network"]):
        if p.parse_args().html:
            print(json2table.convert(json_data[i]))
        else:
            print (json.dumps(json_data[i],indent=4))

