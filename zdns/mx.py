import sys
import dns
import dns.resolver
import json

cache = {}

def mx_lookup(name, rank, lock, timeout):
    retv = {}
    retv['domain'] = name
    if rank:
        retv['rank'] = rank
    retv['exchanges'] = []
    try:
        answers = dns.resolver.query(name, 'MX')
    except Exception:
        retv["error"] = "no-mx"
        with lock:
                sys.stdout.write(json.dumps(retv))
                sys.stdout.write("\n")
                sys.stdout.flush()
        return
    for rdata in answers:
        exchange = str(rdata.exchange)
        mx = {
            "exchange":exchange,
            "preference":rdata.preference,
            "ips":[]
        }
        if exchange in cache:
            ips = cache[exchange]
        else:
            ips = set()
            try:
                for ip in dns.resolver.query(rdata.exchange, 'A'):
                    ips.add(ip.address)
                cache[exchange] = list(ips)
            except Exception:
                mx["error"] = "no-A-for-exch"
        mx["ips"] = list(ips)
        retv["exchanges"].append(mx)
    with lock:
        sys.stdout.write(json.dumps(retv))
        sys.stdout.write("\n")
        sys.stdout.flush()

