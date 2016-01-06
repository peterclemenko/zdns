import sys
import json

import dns
import dns.resolver
import bisect
import dns.name
import dns.query
import dns.rdataclass
import dns.rdatatype
import dns.zone

def axfr_lookup(domain, rank, lock, timeout):
    retv = {}
    retv['domain'] = domain
    if rank:
        retv['rank'] = rank
    retv['servers'] = []
    try:
        ns_query = dns.resolver.query(domain, 'NS').rrset
    except Exception, e:
        retv["error"] = "no-ns"
        with lock:
            sys.stdout.write(json.dumps(retv))
            sys.stdout.write("\n")
            sys.stdout.flush()
        return
    for n in ns_query:
        ns = str(n).rstrip('.')
        if not ns:
            continue
        server = {"ns":ns, "axfr":False}
        zone_content = []
        try:
            axfr_rr = dns.query.xfr(ns, domain, lifetime=timeout)
            axfr_zone = dns.zone.from_xfr(axfr_rr)
        except Exception, e:
            server["error"] = str(e)
            retv["servers"].append(server)
            continue
        server["axfr"] = True
        for name, ttl, rdata in axfr_zone.iterate_rdatas():
            entry = {
                'name':    name.to_text(),
                'ttl':     ttl,
                'rdclass': rdata.rdclass,
                'rdtype':  rdata.rdtype,
                'rdata':   rdata.to_text()
            }
            try:
                entry['pretty_rdclass'] = dns.rdataclass.to_text(rdata.rdclass)
                entry['pretty_rdtype'] = dns.rdatatype.to_text(rdata.rdtype)
                parent = dns.name.Name(domain.split('.'))
                if name == dns.name.empty:
                    entry['pretty_name'] = parent.to_text()
                else:
                    entry['pretty_name'] = name.concatenate(parent).to_text()
            except Exception:
                pass
            zone_content.append(entry)
        server["records"] = zone_content
        retv["servers"].append(server)
    with lock:
        sys.stdout.write(json.dumps(retv))
        sys.stdout.write("\n")
        sys.stdout.flush()

