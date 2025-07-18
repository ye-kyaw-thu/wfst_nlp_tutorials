"""
extract_column_symbols.py

Extract unique symbols from a specific column of an FST-formatted text file
and output a symbol table where each symbol is assigned a unique integer ID.

Written by Ye Kyaw Thu, LU Lab., Myanmar
Last Updated: 18 July 2025

Example usage:
  python extract_column_symbols.py --column 2 < align.txt > isyms.txt
  python extract_column_symbols.py --column 3 --input align.txt --output osyms.txt

Input file format:
  Each line must contain exactly 5 whitespace-separated fields:
    src_state dst_state input_label output_label weight

Output file format:
  A symbol table where each line contains:
    SYMBOL ID
  The first symbol is always <eps> with ID 0.
"""

import sys
import argparse
from collections import defaultdict
from typing import TextIO


def extract_symbols(input_stream: TextIO, column: int) -> dict:
    symbol_to_id = defaultdict(lambda: len(symbol_to_id))
    _ = symbol_to_id["<eps>"]  # always assign 0 to <eps>

    for line in input_stream:
        fields = line.strip().split()
        if len(fields) == 5:
            _ = symbol_to_id[fields[column]]
    return symbol_to_id


def write_symbol_table(symbol_to_id: dict, output_stream: TextIO):
    for symbol, idx in sorted(symbol_to_id.items(), key=lambda x: x[1]):
        print(f"{symbol} {idx}", file=output_stream)


def main():
    parser = argparse.ArgumentParser(
        description="Extract unique symbols from a column of FST-style text and build a symbol table.\n\n"
                    "Input format: 5-column whitespace-separated FST text:\n"
                    "  src_state dst_state input_label output_label weight\n\n"
                    "Output format: One line per symbol:\n"
                    "  SYMBOL ID\n"
                    "Always includes <eps> 0 as the first entry.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--input', '-i', type=argparse.FileType('r'), default=sys.stdin,
                        help="Input file (default: stdin)")
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), default=sys.stdout,
                        help="Output file (default: stdout)")
    parser.add_argument('--column', '-c', type=int, required=True,
                        help="Column index (0-based) to extract symbols from (e.g., 2 for input labels, 3 for output labels)")
    parser.add_argument('--version', action='version', version='extract_column_symbols 1.0')

    args = parser.parse_args()

    try:
        symbol_table = extract_symbols(args.input, args.column)
        write_symbol_table(symbol_table, args.output)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

