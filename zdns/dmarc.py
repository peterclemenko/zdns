import sys
import dns
import dns.resolver
import json

def dmarc_lookup(name, rank, lock, timeout):
    retv = {}
    retv['domain'] = name
    if rank:
        retv['rank'] = rank
    dmarc = None
    to_lookup = ".".join(("_dmarc", name))
    try:
        answers = dns.resolver.query(to_lookup, 'TXT')
        for rdata in answers:
            for s in rdata.strings:
                dmarc = s
                break
            if dmarc:
                break
    except:
        pass
    retv["dmarc"] = dmarc
    with lock:
        sys.stdout.write(json.dumps(retv))
        sys.stdout.write("\n")
        sys.stdout.flush()

