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
client = HTTPClient('http://username:password@127.0.0.1:8115/')



## AUTH ##

# Simple Auth - see http://docs.python-requests.org/en/master/user/authentication/
client.session.auth = ('username', 'password')

## Misc ##
client.session.headers.update({'Connection': 'close'})


## Requests ##

client.request('getinfo')

# New functions
# client.request('getblocksince', 1200000)

client.request('getaddresssince', 1200000, 1, "9ba0f8ca03439a8b4222b256a5f56f4f563f6d83755f525992fa5daf")

# client.request('importprivkey','-----BEGIN RSA PRIVATE KEY-----\nHERE_IS_THE_PRIVKEY\n-----END RSA PRIVATE KEY-----')
