import sys
import dns
import dns.resolver
import json

def a_lookup(name, rank, lock, timeout):
    retv = {}
    retv['domain'] = name
    if rank:
        retv['rank'] = rank
    retv['ips'] = []
    try:
        answers = dns.resolver.query(name, 'A')
    except Exception:
        retv["error"] = "no-mx"
        with lock:
                out_file.write(json.dumps(retv))
                out_file.write("\n")
                out_file.flush()
        return
    retv["ips"] = map(lambda x: str(x), answers)
    with lock:
        sys.stdout.write(json.dumps(retv))
        sys.stdout.write("\n")
        sys.stdout.flush()

