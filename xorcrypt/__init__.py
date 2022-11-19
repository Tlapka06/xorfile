import argparse, sys, os
from getpass import *
from . import xor
def main():
    parser = argparse.ArgumentParser("xorcrypt")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s v0.2\ncopyright (c) 2022 RTranscriptase")
    parser.add_argument("-f", "--force", action="store_true", help="overwrite file without confirmation")
    parser.add_argument("-k", "--key", metavar="key", default="")
    parser.add_argument("-o", "--output", metavar="output_filename", default="")
    parser.add_argument("filename", default="-")
    args = parser.parse_args()
    key = args.key
    
    if not os.path.isfile(args.filename):
        print(f"Input file \"{args.filename}\" is not a regular file or does not exists!")
        return 1

    if key == "":
        key = getpass("key:")
    key = key.encode("ascii")

    if args.filename == "-":
        input_file = sys.stdin.buffer
    else:
        try:
            input_file = open(args.filename, "rb")
        except:
            print(f"Input file \"{args.filename}\" can not be opened!")
            return 1

    if args.output == "":
        output_file = sys.stdout.buffer
    else:
        if os.path.exists(args.output):
            if not args.force:
                choice = input(f"Output file \"{args.output}\" already exists! DO you want to overwrite it [y/N]]? ").lower()
                if not choice == "y":
                    print("Aborted.")
                    return 1
            print(f"Overwriting file \"{args.output}\".")
               
        try:
            output_file = open(args.output, "wb")
        except:
            print(f"Output file \"{args.output}\" can not be opened!")
            input_file.close()
            return 1

    try:
        output_file.write(xor.XorEncryptedData(key, input_file.read()).data)
    except:
        print("Some problem with reading/writing/crypting!")
        input_file.close()
        output_file.close()
        return 1

    input_file.close()
    output_file.flush()
    output_file.close()

if __name__ == "__main__":
    sys.exit(main())