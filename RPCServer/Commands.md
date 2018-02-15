# Bitcoin client API Command List

Here is the original list from https://en.bitcoin.it/wiki/Original_Bitcoin_client/API_calls_list
A more up to date reference is here : https://bitcoin.org/en/developer-reference

I'll edit along the way with what is supported or not (yet)

This list and comments are WIP and are valid for version 0.1b of this Bismuthd API only


## Accounts

An account roughly represents a user. An account may hold one or several addresses.  
An account is either an empty styring (default account) or 2-128 characters long, and may only contains the Base64 Character set.  
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

## Working on

* stop  -  Stop bismuthd server.

* getrawmempool  -   * version 0.7 Returns all transaction ids in memory pool 
  (@iyomisc)

* getbalance  -  (account) (minconf=1)  -  If (account) is not specified, returns the server's total available balance. If (account) is specified, returns the balance in the account.  
  bismuthd specifics: if account is not specified, returns the balance of the default '' account.  
  Needs a new node command. TODO: suggest api_* commands and module to node.py and matching rights management.  
  An account can have several addresses: send a list to the node, not just a single address.

* listaccounts  -  (minconf=1)  -  Returns Object that has account names as keys, account balances as values.   
  See caching or management of balance update.
  
* getreceivedbyaddress  -  (bismuthaddress) (minconf=1)  -  Returns the amount received by (bismuthaddress) in transactions with at least (minconf) confirmations. It correctly handles the case where someone has sent to the address in multiple transactions. Keep in mind that addresses are only ever used for receiving transactions. Works only for addresses in the local wallet, external addresses will always show 0.  
  Needs a new node command. TODO: suggest api_* commands and module to node.py and matching rights management.   

@iyomisc?
* getbestblockhash  -   * version 0.9 Returns the hash of the best (tip) block in the longest block chain. 
* getblock  -  (hash)  -  Returns information about the block with the given hash.  
  https://bitcoin.org/en/developer-reference#getblock
* getconnectioncount  -   * Returns the number of connections to other nodes. 


* getpeerinfo  -   * version 0.7 Returns data about each connected node.  
  See https://bitcoin.org/en/developer-reference#getpeerinfo  
  This will need some adjustments and a new command on node.py

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

* getreceivedbyaccount  -  (account) (minconf=1)  -  Returns the total amount received by addresses with (account) in transactions with at least (minconf) confirmations. If (account) not provided return will include all transactions to all accounts. (version 0.3.24) 
* listreceivedbyaccount  -  (minconf=1) (includeempty=false)  -  Returns an array of objects containing: "account"&nbsp;: the account of the receiving addresses, "amount"&nbsp;: total amount received by addresses with this account, "confirmations"&nbsp;: number of confirmations of the most recent transaction included
* listreceivedbyaddress  -  (minconf=1) (includeempty=false)  -  Returns an array of objects containing: "address"&nbsp;: receiving address, "account"&nbsp;: the account of the receiving address, "amount"&nbsp;: total amount received by the address, "confirmations"&nbsp;: number of confirmations of the most recent transaction included, To get a list of accounts on the system, execute listreceivedbyaddress 0 true

* sendfrom  -  (fromaccount) (tobismuthaddress) (amount) (minconf=1) (comment) (comment-to)  -  (amount) is a real and is rounded to 8 decimal places. Will send the given amount to the given address, ensuring the account has a valid balance using (minconf) confirmations. Returns the transaction ID if successful (not in JSON object).     
  sends from the first address of the given account.   
  Bismuthd specifics: comment id converted to "openfield data" and will be part of the transaction. comment-to is ignored.  
  Uses "mpinsert" node command, since "txsend" is not secure: it sends the private key to the node 
  
* sendmany  -  (fromaccount) {address:amount,...} (minconf=1) (comment)  -  amounts are double-precision floating point numbers  
  Bismuth does not support one to many transactions. Will be converted to many transactions, and return a list of transaction id.  
  Use of this command with bismuthd is better be avoided.
   
* sendtoaddress  -  (bismuthaddress) (amount) (comment) (comment-to)  -  (amount) is a real and is rounded to 8 decimal places. Returns the transaction ID (txid) if successful.   
  Sends from main account default address

* gettransaction  -  (txid)  -  Returns an object about the given transaction containing: "amount"&nbsp;: total amount of the transaction, "confirmations"&nbsp;: number of confirmations of the transaction,"txid"&nbsp;: the transaction ID, "time"&nbsp;: time associated with the transaction(1)., "details" - An array of objects containing:, "account","address", "category", "amount", "fee"  
  Needs additionnal command on node.py

* gettxout  -  (txid) (n) (includemempool=true)  -  Returns details about an unspent transaction output (UTXO) 
* gettxoutsetinfo  -   * Returns statistics about the unspent transaction output (UTXO) set 
* listsinceblock  -  (blockhash) (target-confirmations)  -  Get all transactions in blocks since block (blockhash), or all transactions if omitted. (target-confirmations) intentionally does not affect the list of returned transactions, but only affects the returned "lastblock" value.(1) 
* listtransactions  -  (account) (count=10) (from=0)  -  Returns up to (count) most recent transactions skipping the first (from) transactions for account (account). If (account) not provided it'll return recent transactions from all accounts.
* listunspent  -  (minconf=1) (maxconf=999999)  -  version 0.7 Returns array of unspent transaction inputs in the wallet. 

"rawtransaction" would be objects like line of mempool. Can contain a signature or not.  
Maybe implement with variations (use json instead of hexstring).  

* sendrawtransaction  -  (hexstring)  -  version 0.7 Submits raw transaction (serialized, hex-encoded) to local node and network. 
* decoderawtransaction  -  (hex string="")  -  version 0.7 Produces a human-readable JSON object for a raw transaction.
* getrawtransaction  -  (txid) (verbose=0)  -  version 0.7 Returns raw transaction representation for given transaction id.
 
  

* validateaddress  -  (bismuthaddress)  -  Return information about (bismuthaddress). 

* signmessage  -  (bismuthaddress) (message)  -  Sign a message with the private key of an address. 
* verifymessage  -  (bismuthaddress) (signature) (message)  -  Verify a signed message. 



## Specific Bismuthd commands

These commands are not known nor used by bitcoind

* reindexwallet - force a rebuild of the indexed index {address: account}  

* rescan - Scan whole blockchain for all accounts, addresses and updates all balances.  



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

## Won't implement

* setaccount  -  (bitcoinaddress) (account)  -  Sets the account associated with the given address. Assigning address that is already assigned to the same account will create a new address associated with that account.
  Deprecated 

* listaddressgroupings  -   * version 0.7 Returns all addresses in the wallet and info used for coincontrol. 
  https://bitcoin.org/en/developer-reference#listaddressgroupings

* move  -  (fromaccount) (toaccount) (amount) (minconf=1) (comment)  -  Move from one account in your wallet to another 

* getmemorypool  -  (data)  -  Replaced in v0.7.0 with getblocktemplate, submitblock, getrawmempool 

These commands may have no sense in the Bismuth context.

* setgenerate  -  (generate) (genproclimit)  -  (generate) is true or false to turn generation on or off.Generation is limited to (genproclimit) processors, -1 is unlimited. 
* getgenerate  -   * Returns true or false whether bitcoind is currently generating hashes 
* gethashespersec  -   * Returns a recent hashes per second performance measurement while generating. 
* invalidateblock  -  (hash)  -  Permanently marks a block as invalid, as if it violated a consensus rule.
* keypoolrefill  -   * Fills the keypool, requires wallet passphrase to be set. 
* settxfee  -  (amount)  -  (amount) is a real and is rounded to the nearest 0.00000001 






