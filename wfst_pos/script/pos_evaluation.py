"""
Evaluation for POS Tagging, NER Tagging etc.
Written by Ye Kyaw Thu, LU Lab., Myanmar.
Last Update: 10 July 2025
Usage:
    python ./pos_evaluation.py --ref ../data/otest.txt --hyp ../fst/otest.hyp.line --top-k 30
"""

import sys
import argparse
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser(description='Compare reference and hypothesis files for accuracy.')
    parser.add_argument('--ref', type=str, help='Reference file (default: stdin)')
    parser.add_argument('--hyp', type=str, help='Hypothesis file (default: stdin)')
    parser.add_argument('--top-k', type=int, default=10, 
                      help='Number of top mistakes to display (default: 10)')
    args = parser.parse_args()

    # Handle input files or stdin
    ref_file = sys.stdin if args.ref is None else open(args.ref, 'r', encoding='utf-8')
    hyp_file = sys.stdin if args.hyp is None else open(args.hyp, 'r', encoding='utf-8')

    mistakes = defaultdict(int)
    total = 0
    correct = 0

    for s0, s1 in zip(ref_file, hyp_file):
        s0 = s0.strip()
        s1 = s1.strip()
        a0 = s0.split()
        a1 = s1.split()

        if len(a0) != len(a1):
            print(f"Line lengths don't match:\n{' '.join(a0)}\n{' '.join(a1)}", file=sys.stderr)
            sys.exit(1)

        for w0, w1 in zip(a0, a1):
            # Remove everything after and including underscore
            w0_clean = w0.split('_')[0]
            w1_clean = w1.split('_')[0]
            
            total += 1
            if w0_clean == w1_clean:
                correct += 1
            else:
                mistake = f"{w0_clean} --> {w1_clean}"
                mistakes[mistake] += 1

    # Close files if they were opened (not stdin)
    if args.ref is not None:
        ref_file.close()
    if args.hyp is not None:
        hyp_file.close()

    # Calculate and print accuracy
    accuracy = (correct / total) * 100 if total > 0 else 0
    print(f"Accuracy: {accuracy:.2f}% ({correct}/{total})\n\nMost common mistakes:")

    # Print top mistakes
    for i, (mistake, count) in enumerate(sorted(mistakes.items(), key=lambda x: x[1], reverse=True)):
        if i >= args.top_k:
            break
        print(f"{mistake}\t{count}")

if __name__ == "__main__":
    main()

