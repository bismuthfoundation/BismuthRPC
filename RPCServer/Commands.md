# Bitcoin client API Command List

Here is the original list from https://en.bitcoin.it/wiki/Original_Bitcoin_client/API_calls_list
A more up to date reference is here: https://bitcoin.org/en/developer-reference

I'll edit along the way with what is supported or not (yet)

This list and comments are WIP and are valid for version 0.1b of this Bismuthd API only


## Accounts

An account roughly represents a user. An account may hold one or several addresses.  
An account is either an empty string (default account) or 2-128 characters long, and may only contains the Base64 Character set.  
So, a numeric ID (in decimal or Hex form) is also ok.

## Implemented

(and working)

* getinfo - Returns an object containing various state info.  
  Compatible, plus extra info.

* getaccountaddress  -  (account)  -  Returns the current bismuth address for receiving payments to this account.  
  *If (account) does not exist, it will be created along with an associated new address that will be returned*.  
  Compatible.

* getaddressesbyaccount  -  (account)  -  Returns the list of addresses for the given account.  

* getaccount  -  (bismuthaddress)  -  Returns the account associated with the given address.  

* getnewaddress  -  (account)  -  Returns a new bismuth address for receiving payments. If (account) is specified payments received with the address will be credited to (account). 

* backupwallet  -  (destination)  -  Safely copies wallet.dat to destination, which can be a directory or a path with filename.  
  Thanks @rvanduiven

* dumpwallet  -  (filename)  -  version 0.13.0 Exports all wallet private keys to file.   
  Thanks @rvanduiven

* dumpprivkey  -  (bismuthaddress)  -  Reveals the private key corresponding to (bismuthaddress)

* importprivkey  -  (bismuthprivkey) (account) (rescan=true) * Adds a private key (as returned by dumpprivkey) to your wallet. This may take a while, as a rescan is done, looking for existing transactions. Optional (rescan) parameter added in 0.8.0.    
  Takes a private key, regenerates public key as well as address, add to an account and updates wallet.     
  https://bitcoin.org/en/developer-reference#importprivkey  
  Thanks @iyomisc

* createrawtransaction  -  (fromaddress, toaddress, amount, optional data, optional timestamp)  
  Bismuthd: Creates an unsigned transaction, output is a list, mempool compatible.  
  The format and interface of this method are *NOT* bitcoind compatible because of structural differences.
  
* signrawtransaction  -  (unsigned raw transaction)  
  Bismuthd: Adds signature to a raw transaction and returns the resulting raw transaction.  
  The "from" address has to be in our wallet. Key will be fetched and used to sign.
  The format and interface of this method are *NOT* bitcoind compatible because of structural differences.
   
* getblocknumber  -   * Deprecated in bitcoind version 0.7. Use getblockcount. Left for compatibility purposes. 

* getblockcount  -   * Returns the number of blocks in the longest block chain. 

* getblockhash  -  (index)  -  Returns hash of block in best-block-chain at (index); index 0 is the genesis block 
  Thanks @iyomisc
  
* getdifficulty  -   * Returns the proof-of-work difficulty as a multiple of the minimum difficulty. 
  Thanks @iyomisc
  
* gettransaction  -  (txid)  -  Returns an object about the given transaction containing:   
  "amount": total amount of the transaction, "confirmations": number of confirmations of the transaction,"txid": the transaction ID, 
  "time": time associated with the transaction(1)., "details" - An array of objects containing:, "account","address", "category", "amount", "fee"    
  This is almost like getrawtransaction but embeds extra info and splits the transaction into 2 pieces, like btc: details contains a "send" part and a "receive" one.  
  With Bismuth, this split is artificial since Bismuth is account based.  
  As a result, amount is the same in both transactions, and fee for "send" category is positive. "fee" + "amount" are deduced from sender balance.  
  "vout" is not significant, neither is "abandoned" nor "bip125-replaceable".  
  "timereceived" is an info we do not store, so block time is used instead.
  
example of `gettransaction`:  
```
Request:
{ "jsonrpc": "2.0", 
  "method": "gettransaction", 
  "params": ["hSU2QGPkILxPKajbTLYUI2AzjZqTRxl5PAdtK77CMompz6i30U13gInn"], 
  "id": 2
}

Response:
{
    "amount": 180,
    "fee": 0.01032,
    "confirmations": 154,
    "blockhash": "6db7f6ae22043caf7480175a8a0a8af30477e91b89b16b3e534d31de",
    "blockheight": 1278118,
    "blockindex": -1,
    "blocktime": 1564555312,
    "txid": "hSU2QGPkILxPKajbTLYUI2AzjZqTRxl5PAdtK77CMompz6i30U13gInn",
    "time": 1564555206,
    "timereceived": 1564555312,
    "bip125-replaceable": "no",
    "details": [
        {
            "address": "685e263b24a38c03478b40dbcdcb125f20a05f1e3c558d93287c85a6",
            "category": "send",
            "amount": 180,
            "label": "532d112700ed4d1b9a07dbe5763d5f7f",
            "vout": -1,
            "fee": 0.01032,
            "abandoned": false
        },
        {
            "address": "f6c0363ca1c5aa28cc584252e65a63998493ff0a5ec1bb16beda9bac",
            "category": "receive",
            "amount": 180,
            "label": "532d112700ed4d1b9a07dbe5763d5f7f",
            "vout": -1
        }
    ],
    "hex": ""
}
```

* getblock  -  (hash) (verbosity=1)  -  Returns information about the block with the given hash.  
  https://bitcoin.org/en/developer-reference#getblock
  
example of `getblock` (default verbosity=1):    
```
Request:
{ "jsonrpc": "2.0", 
  "method": "getblock", 
  "params": ["b809da2230790e6c7dd3aeb00f7117c0e33c94b0426d774900e61f70"], 
  "id": 2
}

Response:
{
    "hash": "b809da2230790e6c7dd3aeb00f7117c0e33c94b0426d774900e61f70",
    "confirmations": 540,
    "size": 4013,
    "strippedsize": 4013,
    "height": 1278276,
    "version": 1,
    "versionHex": "00000001",
    "tx": [
        "M6iaN/g8+WUth2C0ZNoXOocYX7jP6j6n/IH9JG4PerNVI21DDQrOTipd",
        "m6xOkdmUMeuOjYZ3NZdtIPfJ2R6wuBJAW9CnXCkDGtr0nlEonxtzWQ5J"
    ],
    "time": 1564563695,
    "nonce": "00000000000000000000000000000000000000000000000000001=64;?;38;0l105Z",
    "difficulty": 105,
    "chainwork": "00",
    "nTx": 2,
    "previousblockhash": "53c765b9c50a2d1da9711eb526f9b0c33cc5a4a5f845a2df3387f914",
    "nextblockhash": "ef8d35e00295f877039354d4cbcaa395616dc89763afa15d4374d838"
}  
```
  
## Implemented, need api handler in node but this node side code is already coded and successfully tested

* validateaddress  -  (bismuthaddress)  -  Return information about (bismuthaddress). 
  See https://bitcoin.org/en/developer-reference#validateaddress

* getbalance  -  (account) (minconf=1)  -  If (account) is not specified, returns the server's total available balance. If (account) is specified, returns the balance in the account.  
  bismuthd specifics: if account is not specified, returns the balance of the default '' account.  
  Does NOT includes transactions or fees from mempool. Minimum minconf value is 1.  
  An account can have several addresses: send a list to the node, not just a single address.

* getpeerinfo  -  Returns data about each connected node.  
  See https://bitcoin.org/en/developer-reference#getpeerinfo  
  This will need some adjustments.

* listaccounts  -  (minconf=1)  -  Returns Object that has account names as keys, account balances as values.   
  See caching or management of balance update.

* sendfrom  -  (fromaccount) (tobismuthaddress) (amount) (minconf=1) (comment) (comment-to)  -  (amount) is a real and is rounded to 8 decimal places. Will send the given amount to the given address, ensuring the account has a valid balance using (minconf) confirmations. Returns the transaction ID if successful (not in JSON object).     
  sends from the first address of the given account.   
  Bismuthd specifics: comment is converted to "openfield data" and will be part of the transaction. comment-to is ignored.  
  Uses "mpinsert" node command, since "txsend" is not secure: it sends the private key to the node.
  
* sendtoaddress  -  (bismuthaddress) (amount) (comment) (comment-to)  -  (amount) is a real and is rounded to 8 decimal places. Returns the transaction ID (txid) if successful.   
  Sends from main account default address
  
* getrawtransaction  -  (txid) (format=False)  - Returns raw transaction representation for given transaction id.
  if format is False, then a simple list with only tx row is returned.
  if format is True, then a full featured json dict with extra info is given.  

* getreceivedbyaccount  -  (account) (minconf=1)  -  Returns the total amount received by addresses with (account) in transactions with at least (minconf) confirmations. 
  If (account) not provided return will include transactions to default account only. 

* getreceivedbyaddress  -  (bismuthaddress) (minconf=1)  -  Returns the amount received by (bismuthaddress) in transactions with at least (minconf) confirmations. 
  It correctly handles the case where someone has sent to the address in multiple transactions. 
  Keep in mind that addresses are only ever used for receiving transactions. 
  bitcoin version: Works only for addresses in the local wallet, external addresses will always show 0.
  bismuthd version: Asks the node, so it works for any address     

## Implemented, need further work to be more bitcoind compatible

* listreceivedbyaccount  -  (minconf=1) (includeempty=false)  -  Returns an array of objects containing:   
  "account" : the account of the receiving addresses, "amount" : total amount received by addresses with this account, "confirmations": number of confirmations of the most recent transaction included

* listreceivedbyaddress  -  (minconf=1) (includeempty=false)  -  Returns an array of objects containing:  
  "address" : receiving address, "account" : the account of the receiving address, "amount" : total amount received by the address, "confirmations": number of confirmations of the most recent transaction included.  
  To get a list of accounts on the system, execute listreceivedbyaddress 0 true
  

## Implemented Specific Bismuthd commands

These commands are not known nor used by bitcoind

* reindexwallet - force a rebuild of the indexed index {address: account}  

* getbalancebyaddress  -  (bismuth address) (minconf=1)  -  Returns the total balance of the given address, with minconf confirmations.    
  Does NOT includes transactions or fees from mempool. Minimum minconf value is 1.

* rescan - Scan whole blockchain for all accounts, addresses and updates all balances.  
  Update: No need to, we ask the node the get updated balances, no need to cache and risk some divergence.

* getblocksince -  (block) - Returns the full blocks (with all transactions) following a given block_height  
  Returns at most 10 blocks (the most recent ones)  
  Used by the json-rpc server to poll and be notified of tx and new blocks.
  
* getaddresssince - (block) (minconf) (bismuth address) - Returns the transactions matching the given address, following a given block_height, with at least minconf confirmations.    
  Returns at most info from 720 blocks (the older ones)  
  Used by the json-rpc server to poll and be notified of tx and new blocks.

## Implemented proxy for native commands

* native - (native command) (args...) - 
This command is a proxy command for [NativeAPI](https://github.com/EggPool/BismuthAPI/blob/master/Doc/commands_reference.md). 

example of `blockgetjson`:  
```
request:
{
	"jsonrpc": "2.0",
	"id": 1,
	"method":"native",
	"params":["blockgetjson",1275724]
}
response
{
    "id": 17,
    "result": [
        {
            "block_height": 1275724,
            "timestamp": 1564400637.87,
            "address": "3d2e8fa99657ab59242f95ca09e0698a670e65c3ded951643c239bc7",
            "recipient": "3d2e8fa99657ab59242f95ca09e0698a670e65c3ded951643c239bc7",
            "amount": 0,
            "signature": "blr8I5sn9I5zF0WbSmtZJn0ObkUitv7I8D1QtYdYmZjyTnpsiGcbVLx+RoK4GJ32EXNNoR9LDqcT6Nnlc7Jf6oDvgyysZL3K81CXzPf7ttVMO9q2k1HLU/+9w3RZv0XYkyBRRO271vl1NsxCY8wan+N1zkn46Vql3AC3R3qeCvIZnfCgoNm+GjJ5VEDESqKhJuSVPN7j85P2Mym24rOfsvn3Nrpe+A0yVnYYf7SfOurd/MuLB4VFvH4Y/yVV73kI7DDBGko9fR1TqEYqzoVT7d9HbqVwQxjf0c+SLjaKHbz3i5DV/LD2GpX/0OIvzrqT5g2P1gluVJIPd46YkXk7t4lKLIl0T6+RL+HLFdLqWI29jK4mZ4o1IxnJYSLU2+M9En/t0Uj790z2oyhoxRBGxk7qjBwlvWn5paz651LdRe5/6Hx7Q2oSynjDS6z3OEYhfRN8P7KLcfsTMvwKSBSYspVLNEpjxP3d5qBwaTm5A+9Lo9LyDmKyNUSP8ZwehSDCk0RnitZOgMOnsE7N+euVX9bsYx+nlDdQYLU9Ygv+HdxoEImYufGqAJHanHo3DL+uKF/lthoG9KpgolLBU6lkc7O5YOYiddnGp71yM9E5hpGu00xqlxwoRT/UIz3tZIkX8CjJsQAcSq4UlR9RDeZN7ZRkB2FGADsiojVXJQQFnJ0=",
            "public_key": "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQ0lqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FnOEFNSUlDQ2dLQ0FnRUEwQXFkYkY0dGdtMTlpbUExSG5BUwpveFhqVkxpS2VlU0MrN0c2SG1kbmRaalVleEFJalN2b1NqTVYwNlRhK2pMeGJnTkVDbE11cUxieTdiOVB6ZlpCCjh5VFdwTkhjSVI5d3IvM1FWVk1LaEtZOWM0S3VhUHZYWlA2Q0NwYzlCdWJWY29LVkFueVNoeXp3VHFjV3dteXgKRG9DcGJIWktwcnh5QW5ueXlwbmxqZCswd3g5QXBidWFWdXQxYnBDMnFPanB4Z05uTkZCbENiTzFRaFczOE5yVgo4SDRaVUt5OGl2QWl0S1BvMWFtOXlnN0pwU2wwaGxYc2Z1eUJaNWhieDZnUHJRNGt5c3lNWEYybHJ5OTJXMTZmClpBWHY2VnlzRXJWdDdDblRmQWlYNUozdnVueXV6aDNaRFBUK3UwbmYxRVJJditwcmVZMDN3VVBQSXBCKzZ6NjIKdTkvVm8rK1VXKy9tUnl4ZmVTUWFhN1M0SDFHUllOdEZyQUpoK3JqbVNrNkpBREhMOXpWTUtpcDJRejVHZloxdwptaXIrZW0xbi90ZW9mRnhZWU5vSzJXVTFrV3FkTVViZlNJN1kwekhkRjJiWHBZemRYQk9Fa0MxZ0docklMOGdnCkFtTWlnbkVZekhaUmI5bmt5WFZlU3dJdGF1UTdPWkFZUmM0SkkzR3VqZnE2a2NTMDAxUnk5L0MwQ1VPVEZ0algKTSt4UUpPQks1MXROci9ZcExCRy9hYlN5Zi9Tc3Rsb3VZTGZOS0wyUXU4QzBHc2p1OTFuemxhbXFBTVRTWDhHRwpudXR2MDVxUFVNR3RsbGVlVzdhR1pkbFA4SXowYXM5Wkx4clJNWWhkeWM2eGV1TlpOT0xhN1VmRjhOK3pFSEVWCjZDU3lveWpTZkdNTjBMVk1MK29xL0trQ0F3RUFBUT09Ci0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ==",
            "block_hash": "270da10a4e176315fcae75a31b0159c988882a841c9d80a50dac0080",
            "fee": 0,
            "reward": 10.048552,
            "operation": "0",
            "openfield": "0000000000000000000000000000000000000000000000000000<41>87;8?1>Z;:2O"
        }
    ],
    "error": null,
    "jsonrpc": "2.0"
}
```

## Working on

* stop  -  Stop bismuthd server.

* getrawmempool  -   * Returns all transaction ids in memory pool 
  (@iyomisc)

@iyomisc?
* getbestblockhash  -   * version 0.9 Returns the hash of the best (tip) block in the longest block chain. 

* getconnectioncount  -   * Returns the number of connections to other nodes. 

* signmessage  -  (bismuthaddress) (message)  -  Sign a message with the private key of an address. 
* verifymessage  -  (bismuthaddress) (signature) (message)  -  Verify a signed message. 

* getmempoolinfo  -  returns information about the node’s current transaction memory pool.  
  https://bitcoin.org/en/developer-reference#getmempoolinfo

* getblocksincewhere - some black magic

## Postponing

See also new commands:

* getblockchaininfo https://bitcoin.org/en/developer-reference#getblockchaininfo  
  Will need some adjustments, see what is coherent in the data
* getnetworkinfo https://bitcoin.org/en/developer-reference#getnetworkinfo
* getwalletinfo https://bitcoin.org/en/developer-reference#getwalletinfo


## Help Appreciated

The following commands are self contained and should be OK to implement in a safe a independant way.
I can do it, but it's always nice not to be alone :)

The 4 following commands are to be coded in one go by the same person.
See rpckeys.py and try_keys.py for the encryption/decryption logic.
See also https://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto for background info

* encryptwallet  -  (passphrase)  -  Encrypts the wallet with (passphrase).  
  Bismuth uses a more secure encryption scheme, AES based, that uses also an IV.  
  This call returns the random IV used, that has to be stored with the passphrase. Both are needed to unlock the wallet.
* walletpassphrase  -  (passphrase) (timeout)  -  Stores the wallet decryption key in memory for (timeout) seconds.  
  passphrase is composed of the IV given by the encryptwallet or walletpassphrasechange call, plus the passphrase itself.
* walletpassphrasechange  -  (oldpassphrase) (newpassphrase)  -  Changes the wallet passphrase from (oldpassphrase) to (newpassphrase).  
  Bismuth uses a more secure encryption scheme, AES based, that uses also an IV.  
  This call returns the random IV used.
* walletlock  -   * Removes the wallet encryption key from memory, locking the wallet. After calling this method, you will need to call walletpassphrase again before being able to call any methods which require the wallet to be unlocked. 

The more the project move forward, the difficult it is to give small tasks for beginners.  
So I won't add more here, but you can look at the code, and if you understand and feel comfortable with it, then pick a function from "To be implemented" and give it a try.  
Tell me via an issue so I know tyou're working on it.

## To be implemented

* help  -  (command)  -  List commands, or get help for a command.

* listsinceblock  -  (blockhash) (target-confirmations)  -  Get all transactions affecting the wallet in blocks since block (blockhash), or all transactions if omitted. (target-confirmations) intentionally does not affect the list of returned transactions, but only affects the returned "lastblock" value.  
  https://bitcoin.org/en/developer-reference#listsinceblock 
* listtransactions  -  (account) (count=10) (from=0)  -  Returns up to (count) most recent transactions skipping the first (from) transactions for account (account). If (account) not provided it'll return recent transactions from all accounts.
* listunspent  -  (minconf=1) (maxconf=999999)  -  version 0.7 Returns array of unspent transaction inputs in the wallet. 
 
* clearbanned - The clearbanned RPC clears list of banned nodes.

## Undecided

* addnode  -  (node) (add remove="" onetry="")  -  version 0.8 Attempts add or remove (node) from the addnode list or try a connection to (node) once. 
* getaddednodeinfo  -  (dns) (node)  -  version 0.8 Returns information about the given added node, or all added nodes

* createmultisig  -  (nrequired) &lt;'("key,"key")'&gt;  -  Creates a multi-signature address and returns a json object  | 
* addmultisigaddress  -  (nrequired) &lt;'("key","key")'&gt; (account)  -  Add a nrequired-to-sign multisignature address to the wallet. Each key is a bitcoin address or hex-encoded public key. If (account) is specified, assign address to (account). Returns a string containing the address. 
* getblocktemplate  -  (params)  -  Returns data needed to construct a block to work on. See  BIP_0022 for more info on params.
* getmininginfo  -   * Returns an object containing mining-related information: blocks, currentblocksize,currentblocktx, difficulty,errors,generate,genproclimit,hashespersec,pooledtx, testnet
* submitblock  -  (hex data="") (optional-params-obj)  -  Attempts to submit new block to network. 
* getrawchangeaddress  -  (account) * version 0.9 Returns a new Bitcoin address, for receiving change. This is for use with raw transactions, NOT normal use. 
* getwork  -  (data)  -  If (data) is not specified, returns formatted hash data to work on:, "midstate"&nbsp;: precomputed hash state after hashing the first half of the data,  "data"&nbsp;: block data,  "hash1"&nbsp;: formatted hash buffer for second hash,  "target"&nbsp;: little endian hash target, If (data) is specified, tries to solve the block and returns true if it was successful.
* listlockunspent  -   * version 0.8 Returns list of temporarily unspendable outputs
* lockunspent  -  (unlock?) (array-of-objects)  -  version 0.8 Updates list of temporarily unspendable outputs

Not sure these are useful
* sendrawtransaction  -  (hexstring)  -  version 0.7 Submits raw transaction (serialized, hex-encoded) to local node and network. 
* decoderawtransaction  -  (hex string="")  -  version 0.7 Produces a human-readable JSON object for a raw transaction.



## Won't implement

* setaccount  -  (bitcoinaddress) (account)  -  Sets the account associated with the given address. Assigning address that is already assigned to the same account will create a new address associated with that account.
  Deprecated 

* listaddressgroupings  -   * version 0.7 Returns all addresses in the wallet and info used for coincontrol. 
  https://bitcoin.org/en/developer-reference#listaddressgroupings

* move  -  (fromaccount) (toaccount) (amount) (minconf=1) (comment)  -  Move from one account in your wallet to another 

* getmemorypool  -  (data)  -  Replaced in v0.7.0 with getblocktemplate, submitblock, getrawmempool 

* sendmany  -  (fromaccount) {address:amount,...} (minconf=1) (comment)  -  amounts are double-precision floating point numbers  
  Bismuth does not support one to many transactions. Will be converted to many transactions, and return a list of transaction id.  
  Deprecated for bitcoin, so won't implement.



## These commands may have no sense in the Bismuth context.

* gettxout  -  (txid) (n) (includemempool=true)  -  Returns details about an unspent transaction output (UTXO) 
* gettxoutsetinfo  -   * Returns statistics about the unspent transaction output (UTXO) set 

* setgenerate  -  (generate) (genproclimit)  -  (generate) is true or false to turn generation on or off.Generation is limited to (genproclimit) processors, -1 is unlimited. 
* getgenerate  -   * Returns true or false whether bitcoind is currently generating hashes 
* gethashespersec  -   * Returns a recent hashes per second performance measurement while generating. 
* invalidateblock  -  (hash)  -  Permanently marks a block as invalid, as if it violated a consensus rule.
* keypoolrefill  -   * Fills the keypool, requires wallet passphrase to be set. 
* settxfee  -  (amount)  -  (amount) is a real and is rounded to the nearest 0.00000001 






