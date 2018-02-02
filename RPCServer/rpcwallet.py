#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Wallet class for Bismuth RJson-RPC Server

@EggPool

"""

import sys
import os
import json
import re

import rpckeys

__version__ = "0.0.1"


# TODO: maintain an inverted index of address:account and a re-index method.

class wallet:    
    """
    Handles a .wallet directory, with accounts, addresses, keys and wallet encryption/backup.
    Content is stored as json, within several dir to limit the files in each directory
    """
    # Warning: make sure this is thread safe as it will be called from multiple threads. Use queues and locks when needed.
    # TODO
    
    __slots__ = ('path', 'verbose', 'encrypted', 'locked', 'passphrase', 'IV','index', 'key');
    
    def __init__(self, path='.wallet', verbose=False):
        self.path = path
        self.verbose = verbose
        self.encrypted = False
        self.locked = False
        self.passphrase = ''
        self.IV = 16 * '\x00'
        self.index = None
        if not os.path.exists(path):
            if self.verbose:
                print(path,"does not exist, creating")
                os.mkdir(path)
        # Since keys will be used everywhere, let's have our instance ready to run.
        self.key = rpckeys.key(verbose=verbose)
        self.load()
        if self.verbose:
            print(self.index)
                
                
    def load(self):
        """
        Loads the current wallet state or init if the dir is empty.
        """
        # At this point the dir exists.
        index_fname = self.path+'/index.json'
        if not os.path.exists(index_fname):
            if self.verbose:
                print(index_fname,"does not exist, creating default")
                # Default index file
                self.index = {"version": __version__, "encrypted":False}
                with open(index_fname, 'w') as outfile:  
                    json.dump(self.index, outfile)
        else:
            with open(index_fname) as json_file:  
                self.index = json.load(json_file)
                

    def _check_account_name(self, account=""):
        """
        Raise an exception if account name does not comply
        An account is 2-128 characters long, and may only contains the Base64 Character set. 
        """
        if account == "":
            # empty if default account
            return True
        if len(account) < 2 or len(account) > 128:
            raise InvalidAccountName
        # Only b64 charset
        if re.search('[^a-zA-Z0-9\+\/]', account) :
            raise InvalidAccountName

                
    def _get_account(self, account=''):
        """
        Returns a dict with the given account info.
        """
        self._check_account_name(account)
        if '' == account:
            fname = self.path+'/default.json'
            path = self.path
        else:
            adir = account[:2]
            path = self.path+'/'+adir
            fname = path+'/'+account+'.json'
        if not os.path.isfile(fname):
            if self.verbose:
                print(fname,"does not exist, creating default")
                # Default account file
                self.key.generate() # This takes some time.
                res = {"encrypted":False, "addresses":[self.key.as_list]}
                # and save account
                if not os.path.exists(path):
                    os.mkdir(path)
                with open(fname, 'w') as outfile:  
                    json.dump(res, outfile)
        else:
            with open(fname) as json_file:  
                res = json.load(json_file)
        return res

        
    def _save_account(self, account_dict, account=''):
        """
        Saves account info back to disk
        """
        # TODO: lock
        self._check_account_name(account)
        if '' == account:
            fname = self.path+'/default.json'
            path = self.path
        else:
            adir = account[:2]
            path = self.path+'/'+adir
            fname = path+'/'+account+'.json'
        if not os.path.exists(path):
            os.mkdir(path)
        with open(fname, 'w') as outfile:  
            json.dump(account_dict, outfile)            
            
        return True


    def get_account_address(self, anaccount=""):
        """
        returns the default address of the given account
        """
        account = self._get_account(anaccount) # This will handle address creation if doesn't exists yet.
        addresses = account["addresses"][0]
        # Addresses is on fact [address,privkey,pubkey]
        # with privkey encrypted if wallet is.
        return addresses[0]


    def get_new_address(self, anaccount=""):
        """
        returns a new address for the given account
        """
        account_dict = self._get_account(anaccount) # This will handle address creation if doesn't exists yet.
        self.key.generate() # This takes some time.
        
        account_dict["addresses"].append(self.key.as_list)
        self._save_account(account_dict, account=anaccount)
        return self.key.address

        
    def get_addresses_by_account(self, anaccount=""):
        """
        returns the list of addresses of the given account
        """
        account = self._get_account(anaccount)        
        return [address[0] for address in account["addresses"]]
        
        
    def backup_wallet(self, afilename="bwallet.zip"):
        """
        Saves the whole wallet directory in a zip or tgz archive
        """
        
        # TODO - Help is welcome.
        
        """
        Wallet is a directory, referenced by self.path
        This backup shall archive all the files and current structure with only relative path info
        into an archive file.
        
        afilename is the full path and filename of where to save.

        Keep cross os compatibility to mind. The archive has to be readable on both Linux and Win.
        A Zip archive could be a simple choice.
        Only use of standard modules, or only lightweight ones would be appreciated.
        
        
        Please have a test setup and make sure code works before requesting PR.
        """
        
        print("TODO: Backup Wallet")
        
        # Should return True or raise an exception
        return True
        
        
    def dump_wallet(self):
        """
        Sends back a list of all privkeys for the wallet.
        """
        
        # TODO - Help is welcome.
        
        """
        Wallet is a directory, referenced by self.path
        each account is a json file, within a directory that is 2 chars long.
        account abcdef is abcedf.json and lies in dir "ab"
        
        This dump has to parse all wallet json files (including "default.json" right in .wallet)
        For each wallet, parse the "addresses" list and build the list of all addresses.
        (ony Bismuth addresses, not the full priv/pub list)
        
        Please have a test setup and make sure code works before requesting PR.
        """
        
        print("TODO: Dump Wallet")
        
        # Should return a list of string or raise an exception
        return ['TODO']        




"""
Custom exceptions
"""

class InvalidAccountName(Exception):
    code = -33001
    message = 'Invalid Account Name'
    data = None


if __name__ == "__main__":
    print("I'm a module, can't run!")
