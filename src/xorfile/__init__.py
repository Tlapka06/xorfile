import argparse, sys, os
from getpass import getpass
from . import xorfile
def main():
    parser = argparse.ArgumentParser("xorfile")
    parser.add_argument("-v", "--version", action="version", help="prints version info", version="xorfile v0.3 (c) 2022 RTranscriptase")
    parser.add_argument("-f", "--force", action="store_true", help="force overwrite")
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("-e", "--encrypt", action="store_const", dest="mode", const="e", help="select encrypt operation (must be used with --output)")
    mode_group.add_argument("-d", "--decrypt", action="store_const", dest="mode", const="d", help="select decrypt operation (must be used with --output)")
    parser.add_argument("-k", "--key", dest="key", help="specify key used in XOR cipher")
    parser.add_argument("infile", metavar="INFILE", help="specify input file")
    parser.add_argument("-o", "--output", dest="outfile", help="specify output file")
    args = parser.parse_args()

    mode = args.mode
    outfile = args.outfile

    if not mode:
        if args.infile[-4:] == ".xor":
            mode = "d"
            if not outfile:
                outfile = args.infile[:-4]
        else:
            mode = "e"
            if not outfile:
                outfile = args.infile + ".xor"
    elif not outfile:
        parser.error("--decrypt/--encrypt requires --output")

    if not args.key:
        key = getpass("key:").encode("ascii")
    else:
        key = args.key.encode("ascii")
    
    if mode == "d":
        with xorfile.XorFile(args.infile, "r", progress=True) as file:
            try:
                file.decrypt(key, outfile, overwrite=args.force)
            except FileExistsError:
                choice = input(f"File \"{outfile}\" already exists. Do you want to overwrite it [y/N]? ").lower()
                if choice == "y":
                    file.decrypt(key, outfile, overwrite=True)
            
    else:
        try:
            with xorfile.XorFile(outfile, "x" if not args.force else "w", progress=True) as file:
                file.write(key, args.infile)
        except FileExistsError:
            choice = input(f"File \"{outfile}\" already exists. Do you want to overwrite it [y/N]? ").lower()
            if choice == "y":
                with xorfile.XorFile(outfile, "w", progress=True) as file:
                    file.write(key, args.infile)

if __name__ == "__main__":
    sys.exit(main())