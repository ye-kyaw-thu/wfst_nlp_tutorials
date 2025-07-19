#!/usr/bin/env python3
import sys
import math
import argparse
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser(description='Generate n-gram FST with backoff smoothing')
    parser.add_argument('--input', type=str, help='Input file (default: stdin)')
    parser.add_argument('--output', type=str, help='Output file (default: stdout)')
    parser.add_argument('--n', type=int, default=2, 
                       help='N-gram order (default: 2 for bigram)')
    parser.add_argument('--alpha', type=float, default=0.1,
                       help='Backoff smoothing weight (default: 0.1)')
    args = parser.parse_args()

    # Handle input/output streams
    infile = open(args.input, 'r') if args.input else sys.stdin
    outfile = open(args.output, 'w') if args.output else sys.stdout

    # Initialize data structures
    ngram_counts = [defaultdict(float) for _ in range(args.n)]
    context_counts = [defaultdict(float) for _ in range(args.n)]
    stateid = defaultdict(lambda: len(stateid))
    
    # Process input
    for line in infile:
        tokens = line.strip().split() + ["</s>"]
        history = ["<s>"] * (args.n - 1)
        
        for token in tokens:
            # Update counts for all n-gram orders
            for order in range(args.n):
                context = tuple(history[-(order):]) if order > 0 else ()
                ngram = context + (token,)
                
                # Update counts
                if order == 0:
                    context_counts[order][()] += 1
                else:
                    context_counts[order][context] += 1
                ngram_counts[order][ngram] += 1
            
            # Update history
            history.append(token)
            if len(history) > args.n - 1:
                history.pop(0)

    ALPHA = args.alpha

    # Print fallback transitions
    for order in range(1, args.n):
        for context in context_counts[order]:
            if context != ("<s>",) * order:  # Skip initial context
                src_state = stateid[context]
                backoff_context = context[1:] if len(context) > 1 else ()
                dest_state = stateid[backoff_context]
                print(f"{src_state} {dest_state} <eps> <eps> {-math.log(ALPHA):.4f}", file=outfile)

    # Print unigram transitions (order 0)
    for unigram in ngram_counts[0]:
        prob = ngram_counts[0][unigram] / context_counts[0][()]
        src_state = stateid[()]
        dest_state = stateid[unigram]
        token = unigram[0]  # Unigram is a 1-tuple
        print(f"{src_state} {dest_state} {token} {token} {-math.log(prob):.4f}", file=outfile)

    # Print higher-order n-gram transitions
    for order in range(1, args.n):
        for ngram in ngram_counts[order]:
            context = ngram[:-1]
            token = ngram[-1]
            
            # Calculate interpolated probability
            higher_order_prob = ngram_counts[order][ngram] / context_counts[order][context]
            lower_order_prob = ngram_counts[order-1][ngram[1:]] / context_counts[order-1][context[1:]] if context[1:] else (
                ngram_counts[0][(token,)] / context_counts[0][()])
            
            prob = (1 - ALPHA) * higher_order_prob + ALPHA * lower_order_prob
            
            src_state = stateid[context]
            dest_state = stateid[(token,)]  # Transition to unigram state
            print(f"{src_state} {dest_state} {token} {token} {-math.log(prob):.4f}", file=outfile)

    # Print final state
    print(stateid[("</s>",)], file=outfile)

    # Close files if we opened them
    if args.input:
        infile.close()
    if args.output:
        outfile.close()

if __name__ == "__main__":
    main()

