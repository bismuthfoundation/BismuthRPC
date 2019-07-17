#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A bitcoind compatible rpc-server for Bismuth

@EggPool

"""

import sys
from tornado.ioloop import IOLoop
from tornado.web import Application

# custom modules
import rpcconfig
from nodeclient import Node
from tornado_jsonrpc import JSONRPCHandler

__version__ = "0.0.33"

if __name__ == "__main__":

    rpc_config = rpcconfig.Get()
    # add our current code version
    rpc_config.version = __version__

    # Temp testing
    # rpc_config.poll = True

    try:
        node = Node(rpc_config)
    except Exception as e:
        # At launch, it's ok to close if the node is not available.
        # TODO: once started, disconnects and reconnects have to be taken care of seemlessly.
        print("Unable to connect to node :", e)
        sys.exit()

    # see http://www.tornadoweb.org/en/stable/httpserver.html#http-server for ssl
    #  see http://www.tornadoweb.org/en/stable/web.html#tornado.web.Application.settings for logging and such
    # see also http://www.tornadoweb.org/en/stable/guide/structure.html#the-application-object
    app = Application([(r"/", JSONRPCHandler, dict(interface=node))])

    app.listen(rpc_config.rpcport)

    IOLoop.current().start()
