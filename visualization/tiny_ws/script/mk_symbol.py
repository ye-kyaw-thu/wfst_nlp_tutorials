"""
Generate input and output symbol tables.
Written by Ye Kyaw Thu, LU Lab., Myanmar.
Last update: 11 July 2025
Usage:
    python ../script/mk_symbol.py --input ./lexicon.txt > char.sym
    python ../script/mk_symbol.py --output ./lexicon.txt > word.sym
"""

#!/""usr/bin/""env python3
import sys
import argparse
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser(description='Generate symbol table from FST files')
    parser.add_argument('--input', metavar='FILE', action='append', 
                       help='Input FST file(s) to read input symbols from')
    parser.add_argument('--output', metavar='FILE', action='append',
                       help='Output FST file(s) to read output symbols from')
    
    args = parser.parse_args()
    
    if not args.input and not args.output:
        parser.print_help()
        sys.exit(1)
    
    # Count the symbols to be printed
    toprint = defaultdict(int)
    
    special_symbols = ['<eps>', '<s>', '<unk>', '<w>']
    
    # Process input files
    if args.input:
        for fname in args.input:
            try:
                with open(fname, 'r', encoding='utf-8') as fstfile:
                    for line in fstfile:
                        line = line.strip()
                        arr = line.split()
                        if len(arr) >= 3:  # Ensure there's an input symbol (index 2)
                            toprint[arr[2]] += 1
            except IOError as e:
                sys.stderr.write(f"Error opening file {fname}: {e}\n")
                sys.exit(1)
    
    # Process output files
    if args.output:
        for fname in args.output:
            try:
                with open(fname, 'r', encoding='utf-8') as fstfile:
                    for line in fstfile:
                        line = line.strip()
                        arr = line.split()
                        if len(arr) >= 4:  # Ensure there's an output symbol (index 3)
                            toprint[arr[3]] += 1
            except IOError as e:
                sys.stderr.write(f"Error opening file {fname}: {e}\n")
                sys.exit(1)
    
    # Output symbols
    curr = 0
    for symbol in special_symbols:
        print(f"{symbol} {curr}")
        curr += 1
        toprint.pop(symbol, None)  # Remove if present
    
    # Output remaining symbols in sorted order
    for symbol in sorted(toprint.keys()):
        print(f"{symbol} {curr}")
        curr += 1

if __name__ == '__main__':
    main()

