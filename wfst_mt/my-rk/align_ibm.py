"""
IBM Alignment Model-1
Written by Ye Kyaw Thu.
Last updated: 18 July 2025
"""

import math
import argparse
from collections import defaultdict
from typing import List, Tuple, TextIO


def read_parallel_corpus(src_file: TextIO, tgt_file: TextIO) -> Tuple[List[List[str]], List[List[str]]]:
    src_lines = [line.strip().split() for line in src_file]
    tgt_lines = [line.strip().split() for line in tgt_file]
    if len(src_lines) != len(tgt_lines):
        raise ValueError(f"Line count mismatch: source={len(src_lines)} target={len(tgt_lines)}")
    return src_lines, tgt_lines


def train_ibm_model_1(src_sents: List[List[str]], tgt_sents: List[List[str]]) -> Tuple[defaultdict, defaultdict]:
    joint_counts = defaultdict(int)
    tgt_counts = defaultdict(int)

    for src, tgt in zip(src_sents, tgt_sents):
        for f in src:
            for e in tgt:
                joint_counts[f, e] += 1
                tgt_counts[e] += 1

    return joint_counts, tgt_counts


def write_fst_output(joint_counts: defaultdict, tgt_counts: defaultdict, output: TextIO):
    for (f, e), count in joint_counts.items():
        prob = count / tgt_counts[e]
        logprob = 0 if prob == 1 else -math.log(prob)
        print(f"0 0 {f} {e} {logprob:.4f}", file=output)
    print("0 0 </s> </s> 0", file=output)
    print("0", file=output)


def main():
    parser = argparse.ArgumentParser(
        description="Train IBM Model 1 aligner and output in FST format."
    )
    parser.add_argument('--source', '-s', type=argparse.FileType('r'), required=True,
                        help="Source language file")
    parser.add_argument('--target', '-t', type=argparse.FileType('r'), required=True,
                        help="Target language file")
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), default='-',
                        help="Output file for FST format (default: stdout)")
    parser.add_argument('--model', '-m', choices=['1'], default='1',
                        help="IBM model version (only Model 1 supported)")
    parser.add_argument('--version', action='version', version='IBMAligner 1.0')

    args = parser.parse_args()

    try:
        src_sents, tgt_sents = read_parallel_corpus(args.source, args.target)
    except ValueError as e:
        print(f"[ERROR] {e}", file=args.output)
        exit(1)

    joint_counts, tgt_counts = train_ibm_model_1(src_sents, tgt_sents)
    write_fst_output(joint_counts, tgt_counts, args.output)


if __name__ == '__main__':
    main()

