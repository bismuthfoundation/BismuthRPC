#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test and dev json-rpc client
"""

import time

# http://jsonrpcclient.readthedocs.io/en/latest/api.html
import jsonrpcclient
from jsonrpcclient.http_client import HTTPClient

jsonrpcclient.config.validate = False

# The test bismuthd.py server
client = HTTPClient("http://username:password@127.0.0.1:8115/")

## AUTH ##

# Simple Auth - see http://docs.python-requests.org/en/master/user/authentication/
client.session.auth = ("username", "password")

## Misc ##
client.session.headers.update({"Connection": "close"})


## Requests ##

# Node info (optional)
client.request("getinfo")
print()
# Check balance (optional)
wallet = client.request("getwalletinfo")
if wallet["encrypted"]:
    # try to decrypt
    res = client.request("walletpassphrase", "password", 60)
print()
wallet = client.request("getwalletinfo")
print()
res = client.request(
    "sendtoaddress",
    "a48c6d81951e404e305957ddd12464501b368d57db14191d48082df6",
    0,
    "Extra",
)
print(res)
