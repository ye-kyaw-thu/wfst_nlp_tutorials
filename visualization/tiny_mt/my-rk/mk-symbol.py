"""
# Symbol table generator
# Written by Ye Kyaw Thu, LU Lab., Myanmar
# Last updated: 18 July 2025
"""

#!/usr/bin/env python3

import sys
import argparse

def generate_symbol_table(input_stream, output_stream):
    count = 2
    seen = set()

    print("<s> 0", file=output_stream)
    print("NULL 1", file=output_stream)

    for line in input_stream:
        line = line.strip()
        if line and not line.isspace() and line not in seen:
            print(f"{line} {count}", file=output_stream)
            seen.add(line)
            count += 1

    print(f"</s> {count}", file=output_stream)

def main():
    parser = argparse.ArgumentParser(
        description="Generate a symbol table with <s>, NULL, and </s> tokens."
    )
    parser.add_argument('--input', '-i', type=argparse.FileType('r', encoding='utf-8'), default=sys.stdin,
                        help="Input file (default: stdin)")
    parser.add_argument('--output', '-o', type=argparse.FileType('w', encoding='utf-8'), default=sys.stdout,
                        help="Output file (default: stdout)")
    parser.add_argument('--version', action='version', version='mk-symbol 1.0')

    args = parser.parse_args()

    generate_symbol_table(args.input, args.output)


if __name__ == '__main__':
    main()

