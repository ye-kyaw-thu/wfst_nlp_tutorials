"""
One-to-One Word Alignment Model
Written by Ye Kyaw Thu, LU Lab., Myanmar
Last updated: 18 July 2025
Input: Parallel corpus with pre-aligned sentences (one-to-one word mappings)
Output: FST format translation probabilities
"""

import sys
import math
import argparse
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser(description="One-to-One Word Alignment Model")
    parser.add_argument('--source', '-s', type=argparse.FileType('r'), 
                        help="Source language file (default: stdin)", default=sys.stdin)
    parser.add_argument('--target', '-t', type=argparse.FileType('r'), required=True,
                        help="Target language file (required)")
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), 
                        help="Output file (default: stdout)", default=sys.stdout)
    args = parser.parse_args()

    # Read input files (maintaining exact original reading logic)
    flines = [x.strip().split() for x in args.source.readlines()]
    elines = [x.strip().split() for x in args.target.readlines()]

    # Original counting logic
    fecount = defaultdict(lambda: 0)
    ecount = defaultdict(lambda: 0)
    for fl, el in zip(flines, elines):
        for f, e in zip(fl, el):
            fecount[f,e] += 1
            ecount[e] += 1

    # Original output logic (just redirected to args.output)
    for (f,e), val in fecount.items():
        print("0 0 %s %s %.4f" % (f, e, 0 if val == ecount[e] else -math.log(val/ecount[e])), file=args.output)
    print("0 0 </s> </s> 0", file=args.output)
    print("0", file=args.output)

if __name__ == '__main__':
    main()

