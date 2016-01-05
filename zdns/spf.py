import sys
import dns
import dns.resolver
import json

cache = {}

def spf_lookup(name, rank, lock, timeout):
    retv = {}
    retv['domain'] = name
    if rank:
        retv['rank'] = rank
    spf = None
    try:
        answers = dns.resolver.query(name, 'TXT')
        for rdata in answers:
            for s in rdata.strings:
                if s.startswith("v=spf1"):
                    spf = s
                    break
            if spf:
                break
    except:
        pass
    retv["spf"] = spf
    with lock:
        sys.stdout.write(json.dumps(retv))
        sys.stdout.write("\n")
        sys.stdout.flush()

