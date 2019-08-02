# Python RPC server for Bismuth

*Needs Python3.6 min, Python 3.7 is recommended*

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
curl -d '{ "jsonrpc": "2.0", "method":"getinfo", "id":1}' http://username:password@localhost:8115/ | jq
```

> At first run, the bismuth daemon will create a wallet with one default address if none exists.

# DOC

All info and current state of working commands is in the [Commands.md file](Commands.md)
