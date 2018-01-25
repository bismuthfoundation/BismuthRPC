"""
Bismuth default/legacy connection layer.
Json over sockets

This file can replace the one from official buismuth code if you install the server in the same dir as the node.
"""

import select, json, platform, time, sys
import socket

# Logical timeout
LTIMEOUT = 45
# Fixed header length
SLEN = 10


__version__ = '0.1.2'


def send(sdef, data, slen=SLEN):
    sdef.settimeout(LTIMEOUT)
    # Make sure the packet is sent in one call
    sdef.sendall(str(len(str(json.dumps(data)))).encode("utf-8").zfill(slen)+str(json.dumps(data)).encode("utf-8"))


def receive(sdef, slen=SLEN):
    sdef.settimeout(LTIMEOUT)
    try:
        data = sdef.recv(slen)
        if not data:
            raise RuntimeError("Socket EOF")
        data = int(data)  # receive length
    except socket.timeout as e:
            return "*"
    try:
        chunks = []
        bytes_recd = 0
        while bytes_recd < data:
            chunk = sdef.recv(min(data - bytes_recd, 2048))
            if not chunk:
                raise RuntimeError("Socket EOF2")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
            
        segments = b''.join(chunks).decode("utf-8")
        return json.loads(segments)
    except Exception as e:
        """
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        """
        raise RuntimeError("Connections: {}".format(e))

