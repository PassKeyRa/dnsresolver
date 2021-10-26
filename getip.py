#!/usr/bin/env python3

import argparse
import gevent
import time

from gevent import socket
from gevent.pool import Pool

resolved = []
num = 0
out_of = 0

def resolve(url):
    global resolved
    global num
    global out_of
    try:
        print(f'Resolving domain {num} out of {out_of}')
        with gevent.Timeout(20):
            data = [socket.gethostbyname(url), url]
            resolved.append(data)
    except:
        pass
    num += 1

def main():
    global num
    global resolved
    global out_of
    parser = argparse.ArgumentParser(description='DNS ip resolver')
    parser.add_argument('-o', '--outfile', default=None, help='Output file')
    #parser.add_argument('-f', '--format', default='ip,domain', help='Specify output format (e.g. \'ip,domain\' or \'domain,ip\')')
    parser.add_argument('-t', '--threads', type=int, default=100, help='Number of threads')
    parser.add_argument('domain_list', help='File with domains')
    args = parser.parse_args()

    ofile = args.outfile
    st = time.time()
    urls = []
    print('Reading file...')
    with open(args.domain_list, 'r') as f:
        for line in f:
            urls.append(line.strip())
    tt = time.time() - st
    print(f'Loaded data in {tt}')
    out_of = len(urls)
    
    st = time.time()
    pool = Pool(args.threads)
    try:
        for u in urls:
            pool.spawn(resolve, u)
        pool.join()
    except KeyboardInterrupt:
        pass
    if ofile:
        with open(ofile, 'w') as f:
            f.write('\n'.join([','.join(i) for i in resolved]))
    tt = time.time() - st
    print(f'Resolved {len(resolved)} in {tt}')
        

if __name__ == '__main__':
    main()
