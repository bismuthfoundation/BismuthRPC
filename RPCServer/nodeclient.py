#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A basic Bismuth node.py client for the Json-RPRC gateway

@EggPool

"""

# Generic modules
import socket

# Bismuth specific modules
import connections
"""
Note: connections.py is legacy. Will be replaced by a "command_handler" class. WIP, see protobuf code.
"""

__version__ = '0.0.1'

class node:    
    """
    Connects to a node.py via socket of use local filesystem if needed to interact with a running bismuth node.
    """
    
    __slots__ = ("config", "s", "node_ipport");
    
    def __init__(self, config):
        self.config = config
        # TODO: raise error if missing critical info like bismuth node/path
        node_ip, node_port = self.config.bismuthnode.split(":")
        self.node_ipport = (node_ip, int(node_port))
        
        self.s = socket.socket()
        self.s.connect(self.node_ipport)
 
 
    def info(self):
        """
        Returns a dict with the node info
        Not a property, could take a param like verbosity of returned info later.
        """
        try:       
            connections.send(self.s, "statusjson")
            info = connections.receive(self.s)
            #print("status", data)
            """
            info = {"version":self.config.version, "protocolversion":"mainnet0016", "walletversion":data[7], "testnet":False, # config data
                    "balance":10.00, "blocks":data[5], "timeoffset":0, "connections":data[1], "difficulty":109.65, # live status
                    "errors":""} # to keep bitcoind compatibility
            """
            # add extra info
            info["version"] = self.config.version
            info["errors"] = ""

        except Exception as e:
            info = {"version":self.config.version, "error":str(e)}
                
        return info
        

