#!/usr/bin/env python

# Copyright (c) Klaudisz Staniek.
# See LICENSE for details.

"""
Simple validation script
"""

from jsonschema import validate
import json
import requests

import os

_HC2_IP_ADDR = "192.168.1.230"
_USER = 'admin'
_PASS = 'admin'

def main():
    
    url_base = "http://{}/api".format(_HC2_IP_ADDR)
    
    
    schema_map = {}
    for root, subFolders, files in os.walk('.'):
        for file in files:
            if file.endswith(".json"):
                file_name = os.path.join(root, file)
                with open(file_name) as f:
                    schema = json.load(f)
                    schema_map[schema['name']] = schema
    
    
    url = url_base + "/settings/info"
    response = requests.get(url, auth=(_USER, _PASS))
    validate(response.json(), schema_map['info'])
    print("Settings Info Validated")
    
    url = url_base + "/rooms"
    items = requests.get(url, auth=(_USER, _PASS)).json()
    for item in items:
        validate(item, schema_map['room'])
    print("Rooms Validated")
    
    url = url_base + "/sections"
    items = requests.get(url, auth=(_USER, _PASS)).json()
    for item in items:
        validate(item, schema_map['section'])
    print("Sections Validated")
    
    url = url_base + "/users"
    items = requests.get(url, auth=(_USER, _PASS)).json()
    for item in items:
        validate(item, schema_map['user'])
    print("Users Validated")
    
    url = url_base + "/globalVariables"
    items = requests.get(url, auth=(_USER, _PASS)).json()
    for item in items:
        validate(item, schema_map['variable'])
    print("Variables Validated")
    
    
    
    url = url_base + "/devices"
    device_ids = [ device['id'] for device in requests.get(url, auth=(_USER, _PASS) ).json() ]
        
    #print device_ids
    
    schema_map = {}
    for root, subFolders, files in os.walk('.'):
        for file in files:
            if file.endswith(".json"):
                file_name = os.path.join(root, file)
                with open(file_name) as f:
                    schema = json.load(f)
                    schema_map[schema['name']] = schema

    
    
    for device_id in device_ids:
        url = url_base + "/devices?id={}".format(device_id)
        device = requests.get(url, auth=(_USER, _PASS) ).json()
        device_type = device['type']
        try:
            schema = schema_map[device_type]
        except:
            print("Device {}({}) does not match any known schema".format(device_type, device_id))
            continue
        
        print("Device {}({})".format(device_type, device_id)),
        validate(device, schema)
        print("is valid")
    


if __name__ == '__main__':
    main()
