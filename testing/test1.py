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

# a real bitcoind server with -regtest -rpcuser=username -rpcpassword=password
#client = HTTPClient('http://username:password@127.0.0.1:18332/')

# The test bismuthd.py server
client = HTTPClient('http://username:password@127.0.0.1:8115/')


# For json-rpc over SSL
#client.session.verify = '/path/to/certificate'

## AUTH ##

# Simple Auth - see http://docs.python-requests.org/en/master/user/authentication/
client.session.auth = ('username', 'password')
# Unique cookie
#client.session.auth = ('__cookie__', 'b16182fb2f0031f2fb2bafc01508a465b7bf52aeb584eff96deca07b9f0598ad')
# See rpcauth
#client.session.auth = ('alice', 'DONT_USE_THIS_YOU_WILL_GET_ROBBED_8ak1gI25KFTvjovL3gAM967mies3E=')

## Misc ##
client.session.headers.update({'Connection': 'close'})


## Requests ##

client.request('getinfo')
# or : client.send('{"method": "getinfo","params":[],"id":1,"jsonrpc":"2.0"}')
# WARNING: getinfo is deprecated and will be fully removed in 0.16. Projects should transition to using getblockchaininfo, getnetworkinfo, and getwalletinfo before upgrading to 0.16

# This one should be cached
client.request('getinfo')

client.request('getblockcount')


#time.sleep(11)
# but not this one
#client.request('getinfo')

client.request('getaccountaddress','')
#--> {"jsonrpc": "2.0", "id": 2, "method": "getaccountaddress", "params": [""]}
#<-- {"result":"n3pJ864fXxWvixHTUrbW3e3DyoJGsUEQtL","error":null,"id":2} (200 OK)


client.request('getaccountaddress','test')
#--> {"jsonrpc": "2.0", "id": 3, "method": "getaccountaddress", "params": ["test"]}
#<-- {"result":"myNA1B4xcELE8ENCFBW91b7bx6NqX8jgJ9","error":null,"id":3} (200 OK)

client.request('getaccountaddress','test2')

client.request('getaddressesbyaccount','')

#client.request('getnewaddress','')
client.request('getaddressesbyaccount','')


#client.request('getbalance')
"""
{"result":99.99996160,"error":null,"id":2}
"""

#client.request('listaccounts')
"""
{"result":{"":99.99996160},"error":null,"id":3}
"""


#client.request('getaccount','moPhStktszZGwtVjziE7eoQ76ATQqfhMtK') # no name for default account
"""
{"result":"","error":null,"id":4}
"""

#client.request('getaddressesbyaccount','') # no name for default account
"""
-->{"jsonrpc": "2.0", "params": [""], "id": 5, "method": "getaddressesbyaccount"}
{"result":["moPhStktszZGwtVjziE7eoQ76ATQqfhMtK","n4aNErEjyafirvMJNCKhFJgBUow9JZnXPk"],"error":null,"id":5}
"""

#client.request('listreceivedbyaddress')
"""
{"result":[{"address":"moPhStktszZGwtVjziE7eoQ76ATQqfhMtK","account":"","amount":10.00000000,"confirmations":1,"label":"","txids":["82790ce7d1fd0df0bc2ffd3cdfdd452e36a32b90885984213a9424f083f74df4"]}],"error":null,"id":6}
"""

#client.request('listsinceblock') 
"""
{"result":{"transactions":[{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":19,"generated":true,"blockhash":"1e60d7dba8bd93e99676dd72171e54eb8ffe35ebfb54439a646075c5a06eab11","blockindex":0,"blocktime":1516567237,"txid":"282ecec426b322698b6616f1cf70ebd767824645ea2b5526f38984fa78601b02","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":27,"generated":true,"blockhash":"2e6925dfb821aa90a5b0e8c9c921076158c79941e0e5a3153140cfb950c97c29","blockindex":0,"blocktime":1516567236,"txid":"5eaf83f5cb6b8f9b5bcf8f0ab0f2aa17ce3baf1d8d0e04467afbd2aba0a7b505","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":14,"generated":true,"blockhash":"39b09cc3bfbbf598bce6e00bc278be453a1d63940396dadb68a411a75e83c8e3","blockindex":0,"blocktime":1516567238,"txid":"eb213bfbb2e864c8b0d76d343b8bc3e05e952b467f264ad26ee94dbf3ad1380c","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":4,"generated":true,"blockhash":"570e1067a5d10485c707c352ef63c0f055c9c0080e7ec000a712b510a64fcbed","blockindex":0,"blocktime":1516567240,"txid":"5864254cb7ac736097257e31de0694afd98aac9286e0cf42458d414157acc70f","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":36,"generated":true,"blockhash":"13afa042517c9f7a367bf1a974344bcd59b91d60f622235172219bbbc5349bc0","blockindex":0,"blocktime":1516567234,"txid":"8fe36ed8d940405717b2c67bbc04dfa493a1764f67bdfcc0be074c350001a512","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":35,"generated":true,"blockhash":"0d942352ec5a8e504da1c3e62b7cf13422960210a13f4f5c39cbc628cb1cba69","blockindex":0,"blocktime":1516567235,"txid":"56d3a785f5d34c12fbdea4ce620b135d0efbdc673c68524b429afd6bffaa4313","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":11,"generated":true,"blockhash":"1427fea6b0fdfd0d2fbf64128fce1d00a6df311dc5c5cbc04513d472252aa5ae","blockindex":0,"blocktime":1516567239,"txid":"720871f16132ed9fb0146d4d2bba20b62b1e7838005132d765f18694d1790314","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},
{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":43,"generated":true,"blockhash":"499760ed4b9eb832c2cc236b3769f03809e46c5770233c3e6ff3c3808ef2cac4","blockindex":0,"blocktime":1516567233,"txid":"902fbbf636834c7ba3d9f1952ae0fdd368e349f369d47e1a061ab94c646f04f7","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":13,"generated":true,"blockhash":"374fc66965120c26f0d8270a5538ad4afc941e54591e500820ac454870e13a64","blockindex":0,"blocktime":1516567238,"txid":"636a2009aa80186685c00e60bec2b1cd99ff1d027e1ebf890f9791d1bf0a47fa","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":34,"generated":true,"blockhash":"44877e0fb2ccf89118079043fa7eaa5357c94a484724bd329c4bf99dcb5c6bd6","blockindex":0,"blocktime":1516567235,"txid":"0e62ce6d124ec07653341c7f3bd889f541b9f19bacca548d96e5cc941e7772fd","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"}],"removed":[],"lastblock":"524e347f08e65c7d23bb7a24e6fae828f22db8a1d198bbe11aea655c18015a91"}
"""


## FOR REFERENCE ONLY - Wiresharked

# bitcoin-cli -regest -getinfo
"""
POST / HTTP/1.1
Host: 127.0.0.1
Connection: close
Authorization: Basic X19jb29raWVfXzpiMTYxODJmYjJmMDAzMWYyZmIyYmFmYzAxNTA4YTQ2NWI3YmY1MmFlYjU4NGVmZjk2ZGVjYTA3YjlmMDU5OGFk
>> __cookie__:b16182fb2f0031f2fb2bafc01508a465b7bf52aeb584eff96deca07b9f0598ad
Content-Length: 40

{"method":"getinfo","params":[],"id":1}
HTTP/1.1 200 OK
Content-Type: application/json
Date: Mon, 22 Jan 2018 20:23:22 GMT
Content-Length: 531
Connection: close

{"result":{"deprecation-warning":"WARNING: getinfo is deprecated and will be fully removed in 0.16. Projects should transition to using getblockchaininfo, getnetworkinfo, and getwalletinfo before upgrading to 0.16","version":150100,"protocolversion":70015,"walletversion":139900,"balance":99.99996160,"blocks":102,"timeoffset":0,"connections":0,"proxy":"","difficulty":4.656542373906925e-10,"testnet":false,"keypoololdest":1516567161,"keypoolsize":2000,"paytxfee":0.00000000,"relayfee":0.00001000,"errors":""},"error":null,"id":1}
"""
# Warning: json does not validate schema (both result and error, even if error is null)

