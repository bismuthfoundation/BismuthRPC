#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A basic Bismuth node.py client for the Json-RPRC gateway

@EggPool

"""

__version__ = '0.0.1'

class node:    
    """
    Connects to a node.py via socket of use local filesystem if needed to interact with a running bismuth node.
    """
     
    def __init__(self,config):
        self.config = config
        # TODO: raise error if missing critical info like bismuth node/path
 
