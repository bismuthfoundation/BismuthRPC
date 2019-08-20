"""
Test with a regulat pbitcoin json rpc client.

needs
https://github.com/EggPool/python-bitcoinrpc
"""

import logging
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


rpc_user = 'username'
rpc_password = "password"

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

rpc_connection = AuthServiceProxy("http://{}:{}@127.0.0.1:8115".format(rpc_user, rpc_password), timeout=120)
getinfo = rpc_connection.getinfo()
print(getinfo)
