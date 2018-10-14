# Python RPC server for Bismuth

WIP.  

Just sending mockup data right no, no connection to a real bismuth node.  
Only testing the service/client rpc protocol.

*Needs Python3.5 min*

## Install

See requirements.txt from upper dir.
`pip3 install -r requirements.txt`

## Config

Default config, that will always ship with the release, is 
> bismuthd.default.conf

Users can copy to
> bismuthd.conf

to define custom settings.  
You only need to define what changes, not everything.

## Run

```bash
python3 bismuthd.py
# With default configuration, testing can be done with something like:
curl -d '{ "jsonrpc": "2.0", "method":"getinfo", "id":0}' http://username:password@localhost:8115/ | jq
```


# DOC

All info and current state of working commands is in the [Commands.md file](Commands.md)
