xorfile (v0.3)
==============

Simple file encryption software. 
For now, it only supports XOR encryption.

Installation
------------
`pip3 install xorfile`

Usage
-----
```
usage: xorfile [-h] [-v] [-f] [-e | -d] [-k KEY] [-o OUTFILE] INFILE

positional arguments:
  INFILE                specify input file

options:
  -h, --help                    show this help message and exit
  -v, --version                 prints version info
  -f, --force                   force overwrite
  -e, --encrypt                 select encrypt operation (must be used with --output)
  -d, --decrypt                 select decrypt operation (must be used with --output)
  -k KEY, --key KEY             specify key used in XOR cipher
  -o OUTFILE, --output OUTFILE  specify output file
  ```