import struct
from gevent import pool
from gevent.dns import resolve_ipv4

# Should be a file with one hostname per line
with open('wildcards.txt.sub') as fin:
    urls = fin.read().split('\n')

def func(host):
    try:
        print 'Resolving %s' % host
        return resolve_ipv4(host)[1]
    except:
        return []

p = pool.Pool(100)
results = p.map(func, urls)

unpacked = []
for r in results:
    out = ['.'.join(str(s) for s in struct.unpack('!BBBB', o)) for o in r]
    unpacked.append(out)

matches = []
# The ip we're trying to find
to_match = '64.70.56.99'
for host, ips in izip(urls, unpacked):
    if to_match in ips:
        print '%s => %s' % (host, ips)
        matches.append(host)
