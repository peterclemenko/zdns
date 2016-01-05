import sys
import os.path
import argparse
import sys
import json

import subprocess
import multiprocessing
from multiprocessing import Pool

from mx import mx_lookup
from axfr import axfr_lookup
from spf import spf_lookup
from dmarc import dmarc_lookup

LOOKUP_FUNCTIONS = {
    "mx":mx_lookup,
#    "a":a_looup,
    "spf":spf_lookup,
    "dmarc":dmarc_lookup,
    "axfr":axfr_lookup
}

# this setup isn't particularly scalable. all names are loaded
# into memory immediately in order to be added to the queue.
# longterm, we probably want to load these in in batches

def run(lookup_fn, threads, in_file, timeout):
    pool = Pool(threads)
    manager = multiprocessing.Manager()
    # create lock around the output file so that we don't garble output
    lock = manager.Lock()
    results = []
    for line in in_file:
        line = line.rstrip()
        if "," in line:
            split = line.split(",")
            domain = split[0]
            rank = int(split[1])
        else:
            domain = line
            rank = None
        args = [domain, rank, lock, timeout]
        results.append(pool.apply_async(lookup_fn, args))
    for res in results:
        while True:
            try:
                res.get(timeout)
                break
            except multiprocessing.TimeoutError:
                pass

def lookup_function(name):
   if name not in LOOKUP_FUNCTIONS:
       raise argparse.ArgumentTypeError
   return LOOKUP_FUNCTIONS[name]

def uint16(s):
    x = int(s)
    if x < 0 or x > 65535:
        raise argparse.ArgumentTypeError
    return x

def readfile(path):
    if path == "-":
        return sys.stdin
    if not os.path.exists(path):
        ArgumentError("Invalid input path. %s does not exist" % path)
    return open(path, 'r')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--threads',
                        type=uint16, default=250)
    parser.add_argument('-T', '--timeout',
                        type=uint16, default=10)
    parser.add_argument("-i", "--input-file", type=readfile,
            default="-")
    parser.add_argument("command", type=lookup_function)
    args = parser.parse_args()

    run(args.command, args.threads, args.input_file, args.timeout)

if __name__ == "__main__":
    main()

