#!/usr/bin/env python3

import argparse
import gevent
import time

from gevent import socket
from gevent.pool import Pool
from colorama import Fore, init
init(autoreset=True)

resolved = []
num = 0
out_of = 0

quiet = False

def print_q(s: str):
    if not quiet:
        print(s)

def resolve(url):
    global resolved
    global num
    global out_of
    try:
        print_q(Fore.YELLOW + f'[STATUS] Resolving domain {num} out of {out_of}')
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
    global quiet
    parser = argparse.ArgumentParser(description='DNS ip resolver')
    parser.add_argument('-o', '--outfile', default=None, help='Output file. Print to stdout if not specified')
    parser.add_argument('-f', '--format', default='%IP%,%DOMAIN%', help='Specify output format (e.g. \'%%IP%%,%%DOMAIN%%\' (default) or \'%%DOMAIN%%,%%IP%%\')')
    parser.add_argument('-t', '--threads', type=int, default=100, help='Number of threads [default: 100]')
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='Do not print anything except results')
    parser.add_argument('domain_list', help='File with domains')
    args = parser.parse_args()

    ofile = args.outfile
    quiet = args.quiet
    format_ = args.format
    st = time.time()
    urls = []
    print_q(Fore.YELLOW + '[STATUS] Reading file...')
    with open(args.domain_list, 'r') as f:
        for line in f:
            urls.append(line.strip())
    tt = time.time() - st
    print_q(Fore.YELLOW + f'[STATUS] Loaded data in {tt}')
    out_of = len(urls)
    
    st = time.time()
    pool = Pool(args.threads)
    try:
        for u in urls:
            pool.spawn(resolve, u)
        pool.join()
    except KeyboardInterrupt:
        pass

    output = ''
    for i in range(len(resolved)):
        ip = resolved[i][0]
        domain = resolved[i][1]
        output += format_.replace('%IP%', ip).replace('%DOMAIN%', domain)
        if i != len(resolved) - 1:
            output += '\n'
    if ofile:
        with open(ofile, 'w') as f:
            f.write(output)
    else:
        print_q('')
        print(output)
        print_q('')
    tt = time.time() - st
    print_q(Fore.GREEN + f'[INFO] Resolved {len(resolved)} in {tt}')
        

if __name__ == '__main__':
    main()
