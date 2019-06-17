#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A basic Bismuth node.py client for the Json-RPRC gateway
Also handles wallet and accounts
@EggPool

"""

# Generic modules
#import socket, sys
#import re
import threading
import time

# Bismuth specific modules
from rpcconnections import Connection
from rpcwallet import Wallet
from ttlcache import Asyncttlcache

"""
Note: connections.py is legacy. Will be replaced by a "command_handler" class. WIP, see protobuf code.
"""

__version__ = '0.0.7'

# Interface versioning
API_VERSION = '0.1c'
"""
0.1c : add getaddresssince(since, minconf, address)
"""


class Node:
    """
    Connects to a node.py via socket of use local filesystem if needed to interact with a running bismuth node.
    """

    __slots__ = ("config", "wallet", "s", "connection", "stop_event", "last_height", "watchdog_thread", "poll")

    def __init__(self, config):
        self.config = config
        self.wallet = Wallet(verbose=config.verbose)
        self.stop_event = threading.Event()
        self.last_height = 0
        try:
            # config may not know of poll, that's ok.
            self.poll = self.config.poll
        except:
            self.poll = False
        # TODO: raise error if missing critical info like bismuth node/path
        node_ip, node_port = self.config.bismuthnode.split(":")
        self.connection = Connection((node_ip, int(node_port)), verbose=config.verbose)
        self.watchdog_thread = threading.Thread(target=self._watchdog)
        self.watchdog_thread.daemon = True
        self.watchdog_thread.start()

    def _poll(self):
        """
        Will ask the node for the new blocks/tx since last known state and run through filters
        :return:
        """
        print("Polling", self.last_height)
        blocks = self.connection.command("api_getblocksince", [self.last_height])
        self.last_height = blocks[:-1][0]
        for tx in blocks:
            print(tx)
            """
            [556649, 1521117120.4, '08acc82ebe8fce711191fd544331ce0ee24ce833a2ad36e3d15f8d94', '08acc82ebe8fce711191fd544331ce0ee24ce833a2ad36e3d15f8d94', 0, 
            'kYVj7Jb50ZwZPhia76tU0VDLSNVg7ba76OqngwYf03Y/yG5RF2z6SS+Lpz3aKGxjN1DFlT3oiwx/3OUg3sGn6F6yTHH5330NGMI/x3ai/IVdcwXwhiq96yvZdIOPuuYIkwrfCCTQF/7kXOcM1Df1+T1dbZ4434NjCDKwHGq1CikNjur3kUsQg0ps6XM3VSTB1Ro1SUfWGY+jRV7Y1YzCs27jf261j95VJCPbFbL8OgA7JiwGPCMlnnbB9H1lCb2OXF1RKk0uyiGNophC5ADUORBIv0QoBiQmn35dNkKxtw1W5S08vB3j3XsZaY9+TSPIitoiYEyj2F+daHiaexx7vTVtDgfFLLsGO8gqIZ94lY+cnGthVBjvE+IiWw4ye6bIKW4l+IR59FIy4tXFwP+mX0rEvxrALLCqh4giNeIZpZzqMzk6QpatmHScl6U2cNzosYeamUNDLatiUojPtFQInlT3xz5Y3VUG/3WBiNmOKsIiiYkDbTfoQRCVVgitmXikEXmH6GiSUWM4+4R0swMq+5Kk5wOfcHJ96Mjv80N8Ul5E4HRw75JsaW38Gf7eIbVCr0pyD2r5KRrFcZIKWcApdArIUBs2S7t5B/exTuqI6ErFZqoa+qu8AZbarSHaL5qT0Oq7feWWYn9nQxDSPZgsomx7YUq6XoDQo6MvFZnuWM8=', 
            'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQ0lqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FnOEFNSUlDQ2dLQ0FnRUFsVENvaXdiOVZQbXUrN2hwUDBRWQozVE5FQktaSFBxZ0FzUmcvRXNhUTZzTEVLVktjMFl6UnkzYU0yalQ1bDVNenpsd0h4TFZWT3JzdCs0WGlYM1NBClU1L3hKUUMrZVNsQlI3aFY3cFVYRnRMSWdZU29PaXhUN0Z4MzQ2R1NNeDcxWHhvS2UvRUFxOEsxTGNDcGNFKzkKc3laNmZhaVVzYVNBSkNvQWN6dU5PQ3NkaUdHSm1INFlld1RLVlhEQmxDZGJmUGpGOFB2VDF2UVZuSng5cWRQagpucW1lMlMyaTBXSWp3ZHZyR2U3NlY2dEFVWEFaQURIa3hoY2QwaWM5ZVpEcThOVmlkVGNBTURveDdpdWxESmhtCk5iMVZEenBLOFRYWFN0WmoxUE04ZWY5WTEvWWNHbDVtREx3OWgxeG9mLzRvYitnMC9mV1RpbVlyb053L2M5NGsKR3FhMmJibzkzbXY1U1pQRm1Qc0VPck56bnI4M2o2aGtVTG50VmhITmxwRy9wRHlVT1FZYVZERHYvT1MraDhGdwpDOUVCdW4yYWFBTGl1dUZudE1hL2pKVmw0RjJzT1N4MzNuUjY0cUkzamtwa0lCenVBTlI0MWZMYVBPZFl4NUV3CmdHOHRTODhvQ2tmV29BNnA5NVY2TStFT2s3NCtyRVdhTy9WaEpMNjU5ZTRGa2ZVcklqMHNIRnQyMHdySmJaR0QKUEdxOGZoVmwxd2FsamVZYnBtUEFsdHZoQjdOVzFnNDNJZ3F4VlN1NzBxejF2REhMQkdBVUgrMmZpbHBTZUp0NgpwR2RCYU1vQnZrR24vZ0RIWWh4UWxFNmxYK0ViSndrM3hEOFdBUUk5MktWRTJyaksrcmk1ZXFEKzlhU1hwdXF1CmV5enJiTm9xYmN5a21KY00wYzFZdTRNQ0F3RUFBUT09Ci0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ==', 
            'c0039d82b44abb22bda72f07c69119a780ae30b6bdca731fac76f1cd', 0, 14.443351, 0, '62ce921d000000007c6ffbed00000000']
            """

    def _ping_if_needed(self):
        """
        Sends a ping if 29 sec or more passed since last activity, to keep connection open
        :return:
        """
        if self.connection.last_activity < time.time()-29:
            #print("Sending Ping")
            ret = self.connection.command("api_ping")
            #print(ret)

    def _watchdog(self):
        """
        called in a thread to send ping and poll the node if needed.
        :return:
        """
        # Give it some time to start and do things
        time.sleep(10)
        while not self.stop_event.is_set():
            if self.poll:
                self._poll()
            self._ping_if_needed()
            # 10 sec is a good compromise.
            time.sleep(10)


    """
    All json-rpc calls are directly mapped to async methods here thereafter:
    As the mapping is auto, we can't conform to PEP and thus, no underscore in method names.
    """

    def stop(self, *args, **kwargs):
        """Clean stop the server"""
        print("Stopping Server")
        self.connection.close(self.s)
        # TODO: Close possible open files and db connection
        #
        # TODO: Signal possible threads to terminate and wait.
        self.stop_event.set()
        #self.watchdog_thread.join() It's a daemon thread, no need to wait, it can take up to 10 sec because of the sleep()
        return True
        # NOT So simple. Have to signal tornado app to close (and not leave the port open) see
        # https://stackoverflow.com/questions/5375220/how-do-i-stop-tornado-web-server
        # https://gist.github.com/wonderbeyond/d38cd85243befe863cdde54b84505784
        #sys.exit()

    @Asyncttlcache(ttl=10)
    async def getinfo(self, *args, **kwargs):
        """
        Returns a dict with the node info
        Could take a param like verbosity of returned info later.
        """
        # WARNING: getinfo is deprecated and will be fully removed in 0.16. Projects should transition to using getblockchaininfo, getnetworkinfo, and getwalletinfo before upgrading to 0.16
        # However we get all info in one go, and it can be cached for subsequent partial info requests from other listed commands.
        try:
            # TODO: connected check and reconnect if needed. But will be handled by the connection layer. Don't bother here.
            # Moreover, it's not necessary to keep a connection open all the time. Not all commands need one, so it just need to connect on demand if it is not.
            info = self.connection.command("statusjson")
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

    #@Asyncttlcache(ttl=10)
    async def getblockhash(self, *args, **kwargs):
        """
        Returns the hash of a given block_height
        """
        try:
            """
            self.connection.send("blockget")
            self.connection.send(str(args[1]))
            block = self.connection.receive()
            """
            block = self.connection.command('blockget',[str(args[1])])
            block = block[0][7]
        except Exception as e:
            block = {"version":self.config.version, "error":str(e)}
        return block

    @Asyncttlcache(ttl=10)
    async def getrawmempool(self, *args, **kwargs):
        """
        WIP
        """
        try:
            """
            self.connection.send("mempool")
            self.connection.send([])
            mempool = self.connection.receive()
            """
            mempool = self.connection.command('mempool',[[]])
            # WIP
        except Exception as e:
            mempool = {"version":self.config.version, "error":str(e)}
        return mempool

    @Asyncttlcache(ttl=10)
    async def getdifficulty(self, *args, **kwargs):
        """
        Returns the current network difficulty
        """
        try:
            info = await self.getinfo()
            diff = info["difficulty"]
        except Exception as e:
            diff = {"version":self.config.version, "error":str(e)}
        return diff

    async def getblocknumber(self, *args, **kwargs):
        """
        Deprecated. Removed in version 0.7. Use getblockcount.
        Returns the number of blocks in the longest block chain.
        """
        info = await self.getblockcount()
        return info

    # No need to cache since it's using cached getinfo()
    async def getblockcount(self, *args, **kwargs):
        """
        Returns the number of blocks in the longest block chain.
        """
        info = await self.getinfo()
        try:
            blocks = info['blocks']
            return blocks
        except Exception as e:
            error = {"version":self.config.version, "error":str(e)}
            return error

    async def getaccountaddress(self, *args, **kwargs):
        """(account)
        Returns the current bitcoin address for receiving payments to this account.
        If (account) does not exist, it will be created along with an associated new address that will be returned.
        """
        try:
            account = args[1] # 0 is self
            address = self.wallet.get_account_address(account)
            # address is a single string.
            return address
        except Exception as e:
            error = {"version":self.config.version, "error":str(e)}
        return error

    async def getaccount(self, *args, **kwargs):
        """(address)
        returns the name of the account associated with the given address.
        """
        try:
            address = args[1] # 0 is self
            return self.wallet.get_account(address)
        except Exception as e:
            error = {"version":self.config.version, "error":str(e)}
        return error

    async def dumpprivkey(self, *args, **kwargs):
        """(address)
        returns the private key corresponding to an address. (But does not remove it from the wallet.)
        """
        try:
            address = args[1] # 0 is self
            return self.wallet.dump_privkey(address)
        except Exception as e:
            error = {"version":self.config.version, "error":str(e)}
        return error

    async def importprivkey(self, *args, **kwargs):
        """(privkey, account, rescan)
        Imports the given privkey in the given account and save updated wallet
        returns Null on success
        """
        try:
            privkey = args[1] # 0 is self
            account_name = ''
            if len(args) > 2:
                account_name = args[2]
            rescan = False
            if len(args) > 3:
                rescan = args[3]
            return self.wallet.import_privkey(privkey, account_name, rescan)
        except Exception as e:
            error = {"version":self.config.version, "error":str(e)}
        return error

    async def getnewaddress(self, *args, **kwargs):
        """(account)
        Returns a new bitcoin address for receiving payments.
        If (account) is specified payments received with the address will be credited to (account).
        """
        try:
            account = args[1] # 0 is self
            address = self.wallet.get_new_address(account)
            # address is a single string.
            return address
        except Exception as e:
            error = {"version":self.config.version, "error":str(e)}
        return error

    async def backupwallet(self, *args, **kwargs):
        """(file_name)
        Backups the whole wallet directory in then given archive filename
        """
        try:
            file_name = args[1] # 0 is self
            return self.wallet.backup_wallet(file_name)
        except Exception as e:
            error = {"version":self.config.version, "error":str(e)}
        return error

    async def dumpwallet(self, *args, **kwargs):
        """(file_name)
        Sends all the priv keys from the wallet
        """
        try:
            file_name = args[1] # 0 is self
            return self.wallet.dump_wallet(file_name, self.config.version)
        except Exception as e:
            error = {"version":self.config.version, "error":str(e)}
        return error

    async def createrawtransaction(self, *args, **kwargs):
        """
        (fromaddress, toaddress, amount, optional data, optional timestamp)
         Bismuthd: Creates an unsigned transaction, output is a list, mempool compatible.
        The format and interface of this method are *NOT* bitcoind compatible because of structural differences.
        """
        try:
            from_address, to_address, amount = args[1:4] # 0 is self
            data = ''
            timestamp = 0
            if len(args)>4:
                data = args[4]
            if len(args)>5:
                timestamp = args[5]
            return self.wallet.make_unsigned_transaction(from_address, to_address, amount, data, timestamp)
        except Exception as e:
            return {"version": self.config.version, "error": str(e)}

    async def signrawtransaction(self, *args, **kwargs):
        """
        Bismuthd: Adds signature to a raw transaction and returns the resulting raw transaction.
        The "from" address has to be in our wallet. Key will be fetched and used to sign.
        The format and interface of this method are *NOT* bitcoind compatible because of structural differences.
        """
        try:
            return self.wallet.sign_transaction(args[1:])
        except Exception as e:
            #print(e)
            return {"version": self.config.version, "error": str(e)}

    async def getrawtransaction(self, *args, **kwargs):
        """
        (txid) (format)  -  Returns raw transaction representation for given transaction id, in json
        Bismuthd : kept format param for compatibility, but always returns a json output or Null if tx was not found.
        if format is False, then a simple list with only tx row is returned.
        if format is True, then a full featured json dict with extra info is given.
        """
        try:
            transaction = args[1]
            # check tx format?
            format = False
            if len(args)>2:
                format = args[2]
            """
            if not re.match('[a..zA..Z0..9\+/=]{56}', transaction):
                # broken regexp
                raise ValueError("Bad Transaction format")
            """
            return self.connection.command("api_gettransaction", [transaction, format])
        except Exception as e:
            #print(e)
            return {"version": self.config.version, "error": str(e)}

    async def sendfrom(self, *args, **kwargs):
        """
        Will send the given amount to the given address, ensuring the account has a valid balance using (minconf) confirmations. Returns the transaction ID if successful.
        * sendfrom  -  (fromaccount) (tobismuthaddress) (amount) (minconf=1) (comment) (comment-to)  -  (amount) is a real and is rounded to 8 decimal places. Will send the given amount to the given address, ensuring the account has a valid balance using (minconf) confirmations. Returns the transaction ID if successful (not in JSON object).
        sends from the first address of the given account.
        Bismuthd specifics: comment is converted to "openfield data" and will be part of the transaction. comment-to is ignored.
        Uses "mpinsert" node command internally , since "txsend" is not secure: it sends the private key to the node.
        TODO: mpinsert will have to return a proper boolean or message for Ok/Ko
        Could be worked on with mempool modularization
        """
        try:
            address, to_address, amount = args[1:4]
            minconf = 1
            if len(args) > 4:
                minconf = args[4]
            if minconf < 1:
                minconf = 1
            # TODO: minconf is ignored for now, we just transmit to the node.
            comment = ''
            if len(args) > 5:
                comment = args[5]
            # Create the raw transaction
            transaction = self.wallet.sign_transaction(self.wallet.make_unsigned_transaction(address, to_address, amount, comment))
            void = self.connection.command("mpinsert", [[transaction]])
            # TODO: when implemented node side, use returned status code
            #print("mpinsert res", void)
            txid = transaction[4][:56]
            return txid
        except Exception as e:
            return {"version":self.config.version, "error":str(e)}

    async def sendtoaddress(self, *args, **kwargs):
        """
        (bismuthaddress) (amount) (comment) (comment-to)  -  (amount) is a real and is rounded to 8 decimal places. Returns the transaction ID (txid) if successful.
        Sends from main account default address
        Bismuthd specifics: comment is converted to "openfield data" and will be part of the transaction. comment-to is ignored.
        Uses "mpinsert" node command internally , since "txsend" is not secure: it sends the private key to the node.
        TODO: mpinsert will have to return a proper boolean or message for Ok/Ko
        Could be worked on with mempool modularization
        """
        try:
            to_address, amount = args[1:3]
            # TODO: minconf is ignored for now, we just transmit to the node.
            comment = ''
            if len(args) > 3:
                comment = args[3]
            # defualt account address
            address = self.wallet.get_account_address('')
            # Create the raw transaction
            transaction = self.wallet.sign_transaction(self.wallet.make_unsigned_transaction(address, to_address, amount, comment))
            void = self.connection.command("mpinsert", [[transaction]])
            # TODO: when implemented node side, use returned status code
            #print("mpinsert res", void)
            txid = transaction[4][:56]
            return txid
        except Exception as e:
            return {"version":self.config.version, "error":str(e)}

    # @Asyncttlcache(ttl=10)
    async def getreceivedbyaddress(self, *args, **kwargs):
        """
        Takes a single address, a min conf count, and sends back the total received amount (!= balance).
        """
        try:
            minconf = 1
            if len(args) > 2:
                minconf = args[2]
            if minconf < 1:
                minconf = 1
            address = args[1]
            total = self.connection.command("api_getreceived", [[address], minconf])
            return total
        except Exception as e:
            info = {"version": self.config.version, "error": str(e)}
        return info

    # @Asyncttlcache(ttl=10)
    async def getreceivedbyaccount(self, *args, **kwargs):
        """
        Takes an account, a min conf count, and sends back the total received amount for addresses of this account (!= balance).
        """
        try:
            minconf = 1
            if len(args) > 2:
                minconf = args[2]
            if minconf < 1:
                minconf = 1
            account = args[1]
            addresses = await self.getaddressesbyaccount(self, account)
            total = self.connection.command("api_getreceived", [addresses, minconf])
            return total
        except Exception as e:
            info = {"version": self.config.version, "error": str(e)}
        return info

    # @Asyncttlcache(ttl=10)
    async def listreceivedbyaddress(self, *args, **kwargs):
        """
        Takes a single address, a min conf count, and sends back the total received amount (!= balance).
        """
        try:
            minconf = 1
            if len(args) > 1:
                minconf = args[1]
            if minconf < 1:
                minconf = 1
            includeempty = False
            if len(args) > 2:
                includeempty = args[2]
            addresses = self.wallet.get_all_addresses()
            # mockup: [{"address":"moPhStktszZGwtVjziE7eoQ76ATQqfhMtK","account":"","amount":10.00000000,"confirmations":1,"label":"","txids":["82790ce7d1fd0df0bc2ffd3cdfdd452e36a32b90885984213a9424f083f74df4"]}]
            all = self.connection.command("api_listreceived", [addresses, minconf, includeempty])
            return all
        except Exception as e:
            info = {"version": self.config.version, "error": str(e)}
        return info

    # @Asyncttlcache(ttl=10)
    async def listreceivedbyaccount(self, *args, **kwargs):
        """
        Takes a single address, a min conf count, and sends back the total received amount (!= balance).
        """
        try:
            minconf = 1
            if len(args) > 2:
                minconf = args[2]
            if minconf < 1:
                minconf = 1
            includeempty = False
            if len(args) > 3:
                includeempty = args[3]
            account = args[1]
            addresses = await self.getaddressesbyaccount(self, account)
            all = self.connection.command("api_listreceived", [addresses, minconf, includeempty])
            return all
        except Exception as e:
            info = {"version": self.config.version, "error": str(e)}
        return info

    # @Asyncttlcache(ttl=10)
    async def getbalance(self, *args, **kwargs):
        """
        Returns the balance of a specific account (default account if empty)
        """
        try:
            minconf = 1
            if len(args) > 2:
                minconf = args[2]
            if minconf < 1:
                minconf = 1
            print('getb args', args)
            account = args[1]
            addresses = await self.getaddressesbyaccount(self, account)
            print("getbalance", account, addresses, minconf)
            balance = self.connection.command("api_getbalance", [addresses, minconf])
            return balance
        except Exception as e:
            return {"version":self.config.version, "error":str(e)}

    async def getbalancebyaddress(self, *args, **kwargs):
        """
        Returns the total balance of a specific address
        This is an extra command, not included in default bitcoin json-rpc
        """
        try:
            minconf = 1
            if len(args) > 2:
                minconf = args[2]
            if minconf < 1:
                minconf = 1
            address = args[1]
            balance = self.connection.command("api_getbalance", [[address], minconf])
            return balance
        except Exception as e:
            return {"version":self.config.version, "error":str(e)}

    # @Asyncttlcache(ttl=10)
    async def listaccounts(self, *args, **kwargs):
        """
        List all accounts and balance of the wallet
        """
        try:
            minconf = 1
            if len(args)>1:
                minconf = args[1]
            if minconf < 1:
                minconf = 1
            accounts = self.wallet.list_accounts()
            balances= {}
            # TODO: better reuse the generator for rpcwallet and use dict comprehension, or pass getbalance as a callback
            for account in accounts:
                print("Account", account)
                # when called from here, self is not passed (but it is when called from the server, so we add it to keep args management coherent.
                balances[account] = await self.getbalance(self, account, minconf)
            return balances
        except Exception as e:
            return {"version":self.config.version, "error":str(e)}

    # @Asyncttlcache(ttl=10)
    async def validateaddress(self, *args, **kwargs):
        """
        Return information about bismuthaddress. https://bitcoin.org/en/developer-reference#validateaddress
        for Bismuth, returns a different info. TODO To be specified
        """
        try:
            address = args[1]
            # returns offline and local wallet info
            info = self.wallet.validate_address(address)
            # Then ask for online info like possible pubkey
            try:
                online = self.connection.command("api_getaddressinfo", [address])
                info.update(online)
            except Exception as e:
                pass
            return info
        except Exception as e:
            return {"version":self.config.version, "error":str(e)}

    @Asyncttlcache(ttl=10)
    async def getpeerinfo(self, *args, **kwargs):
        """
        Returns data about each connected node.
        See https://bitcoin.org/en/developer-reference#getpeerinfo
        """
        try:
            info = self.connection.command("api_getpeerinfo")
            return info
        except Exception as e:
            info = {"version": self.config.version, "error": str(e)}
        return info

    async def getblocksince(self, *args, **kwargs):
        """
        Returns the full blocks (including transactions) following a given block_height
        Returns at most 10 blocks (the most recent ones)
        """
        try:
            since = args[1]
            info = self.connection.command("api_getblocksince", [since])
            return info
        except Exception as e:
            info = {"version": self.config.version, "error": str(e)}
        return info

    async def getaddresssince(self, *args, **kwargs):
        """
        Returns the transactions following a given block_height
        Returns at most 720 blocks worth of data (the oldest ones)
        """
        try:
            since, minconf, address = args[1], args[2], args[3]
            info = self.connection.command("api_getaddresssince", [since, minconf, address])
            return info
        except Exception as e:
            info = {"version": self.config.version, "error": str(e)}
        return info

    async def getaddressesbyaccount(self, *args, **kwargs):
        """
        List the addresses of the provided account args[1]
        """
        try:
            account = args[1] # 0 is self
            return self.wallet.get_addresses_by_account(account)
        except Exception as e:
            return {"version":self.config.version, "error":str(e)}

    async def listsinceblock(self, *args, **kwargs):
        """
        List the transactions since the provided blockheight.
        """
        try:
            # TODO: mockup
            list_since_block = {"transactions":[{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":19,"generated":True,"blockhash":"1e60d7dba8bd93e99676dd72171e54eb8ffe35ebfb54439a646075c5a06eab11","blockindex":0,"blocktime":1516567237,"txid":"282ecec426b322698b6616f1cf70ebd767824645ea2b5526f38984fa78601b02","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":27,"generated":True,"blockhash":"2e6925dfb821aa90a5b0e8c9c921076158c79941e0e5a3153140cfb950c97c29","blockindex":0,"blocktime":1516567236,"txid":"5eaf83f5cb6b8f9b5bcf8f0ab0f2aa17ce3baf1d8d0e04467afbd2aba0a7b505","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":14,"generated":True,"blockhash":"39b09cc3bfbbf598bce6e00bc278be453a1d63940396dadb68a411a75e83c8e3","blockindex":0,"blocktime":1516567238,"txid":"eb213bfbb2e864c8b0d76d343b8bc3e05e952b467f264ad26ee94dbf3ad1380c","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":4,"generated":True,"blockhash":"570e1067a5d10485c707c352ef63c0f055c9c0080e7ec000a712b510a64fcbed","blockindex":0,"blocktime":1516567240,"txid":"5864254cb7ac736097257e31de0694afd98aac9286e0cf42458d414157acc70f","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":36,"generated":True,"blockhash":"13afa042517c9f7a367bf1a974344bcd59b91d60f622235172219bbbc5349bc0","blockindex":0,"blocktime":1516567234,"txid":"8fe36ed8d940405717b2c67bbc04dfa493a1764f67bdfcc0be074c350001a512","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":35,"generated":True,"blockhash":"0d942352ec5a8e504da1c3e62b7cf13422960210a13f4f5c39cbc628cb1cba69","blockindex":0,"blocktime":1516567235,"txid":"56d3a785f5d34c12fbdea4ce620b135d0efbdc673c68524b429afd6bffaa4313","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":11,"generated":True,"blockhash":"1427fea6b0fdfd0d2fbf64128fce1d00a6df311dc5c5cbc04513d472252aa5ae","blockindex":0,"blocktime":1516567239,"txid":"720871f16132ed9fb0146d4d2bba20b62b1e7838005132d765f18694d1790314","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":43,"generated":True,"blockhash":"499760ed4b9eb832c2cc236b3769f03809e46c5770233c3e6ff3c3808ef2cac4","blockindex":0,"blocktime":1516567233,"txid":"902fbbf636834c7ba3d9f1952ae0fdd368e349f369d47e1a061ab94c646f04f7","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":13,"generated":True,"blockhash":"374fc66965120c26f0d8270a5538ad4afc941e54591e500820ac454870e13a64","blockindex":0,"blocktime":1516567238,"txid":"636a2009aa80186685c00e60bec2b1cd99ff1d027e1ebf890f9791d1bf0a47fa","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"},{"account":"","address":"n2LAv7w2vG45gZSaFZBXQhTeaMndS1Y78W","category":"immature","amount":50.00000000,"vout":0,"confirmations":34,"generated":True,"blockhash":"44877e0fb2ccf89118079043fa7eaa5357c94a484724bd329c4bf99dcb5c6bd6","blockindex":0,"blocktime":1516567235,"txid":"0e62ce6d124ec07653341c7f3bd889f541b9f19bacca548d96e5cc941e7772fd","walletconflicts":[],"time":1516567222,"timereceived":1516567222,"bip125-replaceable":"no"}],"removed":[],"lastblock":"524e347f08e65c7d23bb7a24e6fae828f22db8a1d198bbe11aea655c18015a91"}
            return list_since_block
        except Exception as e:
            return {"version":self.config.version, "error":str(e)}

    """
    Here comes extra commands, that are *not* bitcoind compatible
    """

    async def reindexwallet(self, *args, **kwargs):
        """
        Force a reindex of the wallet accounts and addresses
        """
        try:
            return self.wallet.reindex()
        except Exception as e:
            return {"version":self.config.version, "error":str(e)}


if __name__ == "__main__":
    print("I'm a module, can't run!")
