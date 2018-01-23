"""
Config file manager.
"""

import os.path as path


__version__ = '0.1.0'

class Get:
    
    # "param_name":["type"] or "param_name"=["type","property_name"]
    vars={"rpcuser":["str"],"rpcpassword":["str"],"loglevel":["str"],"verbose":["int"],"rpcport":["int"]}
 
    def __init__(self):
        self.verbose = 0
        self.rpcport = 8115
        return self.read()
 
    def load_file(self,filename):
        print("Loading",filename)
        for line in open(filename):
            if '=' in line:
                left,right = map(str.strip,line.rstrip("\n").split("="))
                if not left in self.vars:
                    # Warn for unknown param?
                    continue
                params = self.vars[left]
                if params[0] == "int":
                    right = int(right)
                elif params[0] == "list":
                    right = [item.strip() for item in right.split(",")]
                else:
                    # treat as "str"
                    pass 
                if len(params)>1:
                    # deal with properties that do not match the config name.
                    left = params[1]
                setattr(self,left,right)                
        if self.verbose:
            print(self.__dict__)           
                    
    def read(self):
        # first of all, load from default config so we have all needed params
        self.load_file("bismuthd.default.conf")
        # then override with optional custom config
        if path.exists("bismuthd.conf"):
            self.load_file("bismuthd.conf")
