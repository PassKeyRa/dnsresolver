# DNS resolver

Multi-threaded DNS resolver to resolve ip addresses for lots of domains

## Usage

You can set the output file, output format, number of threds and quiet parameters. In case the default format `%IP%,%DOMAIN%` is not suitable for you it's possible to set the custom format. Quiet option will enable the quiet mode, when info and status are not printed, only results.

```
usage: getip.py [-h] [-o OUTFILE] [-f FORMAT] [-t THREADS] [-q] domain_list

DNS ip resolver

positional arguments:
  domain_list           File with domains

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Output file. Print to stdout if not specified
  -f FORMAT, --format FORMAT
                        Specify output format (e.g. '%IP%,%DOMAIN%' (default) or '%DOMAIN%,%IP%')
  -t THREADS, --threads THREADS
                        Number of threads [default: 100]
  -q, --quiet           Do not print anything except results
```

**Running example:**

```bash
python3 getip.py -o results.txt -t 50 domains.txt
```
