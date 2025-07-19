"""
mk_fst_format.py

Convert a space-separated sentence (one per line) into FST arc format.

Written by Ye Kyaw Thu
Last updated: 18 July 2025

Each token becomes an arc of the form:
  0 1 TOKEN TOKEN
  1 2 TOKEN TOKEN
  ...
Final arc:
  N N+1 </s> </s>
Final state:
  N+1

Example input line:
  အချိန် လဲ

Example output:
  0 1 အချိန် အချိန်
  1 2 လဲ လဲ
  2 3 </s> </s>
  3

Usage examples:
  python mk_fst_format.py --input input.kc --output input.txt
  cat input.kc | python mk_fst_format.py > input.txt
"""

import sys
import argparse
from typing import TextIO


def process_line(line: str, output_stream: TextIO):
    if not line.strip():
        output_stream.write("\n")
        return

    words = line.strip().split()
    state = 0
    for word in words:
        print(f"{state} {state + 1} {word} {word}", file=output_stream)
        state += 1
    print(f"{state} {state + 1} </s> </s>", file=output_stream)
    print(f"{state + 1}", file=output_stream)
    output_stream.write("\n")


def main():
    parser = argparse.ArgumentParser(
        description="Convert space-separated lines into FST format with input/output labels.\n\n"
                    "Each token becomes an arc: STATE STATE+1 WORD WORD\n"
                    "A final </s> </s> arc and end state is appended.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('--input', '-i', type=argparse.FileType('r', encoding='utf-8'), default=sys.stdin,
                        help="Input file (default: stdin)")
    parser.add_argument('--output', '-o', type=argparse.FileType('w', encoding='utf-8'), default=sys.stdout,
                        help="Output file (default: stdout)")
    parser.add_argument('--version', action='version', version='mk_fst_format 1.0')

    args = parser.parse_args()

    for line in args.input:
        process_line(line, args.output)


if __name__ == "__main__":
    main()

