import socket
import sys
import dns
import dns.resolver
import json

def shorta_lookup(name, rank, lock, timeout):
    try:
        lookup = socket.gethostbyname(name)
        with lock:
            sys.stdout.write("%s,%s\n" % (lookup, name))
            sys.stdout.flush()
    except:
        pass
