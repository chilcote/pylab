#!/usr/bin/python
#ref: https://gist.github.com/pudquick/c2800ffd06890f67af23

import socket

def default_interface():
    # 203.0.113.1 is reserved in TEST-NET-3 per RFC5737
    # Should never be local, essentially equal to "internet"
    # This should get the 'default' interface
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Uses UDP for instant 'connect' and port 9 for discard
        # protocol: http://en.wikipedia.org/wiki/Discard_Protocol
        s.connect(('203.0.113.1', 9))
        client = s.getsockname()[0]
    except socket.error:
        client = "Unknown IP"
    finally:
        del s
    return client

print default_interface()
