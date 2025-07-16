"""
for building FST LM
Written by Ye Kyaw Thu, LU Lab., Myanmar.
Last update: 10 July 2025
Usage:
    python ./build_pos_lm.py ../fst/tags.syms ../fst/pairs.txt ../fst/pos_lm.fst.txt 2
"""

import sys
from collections import defaultdict

def build_pos_lm(tags_syms, pairs_file, output_file, ngram=2):
    """Create POS ngram model (2-gram or 3-gram) from training data."""
    pos_counts = defaultdict(lambda: defaultdict(int))
    total = defaultdict(int)
    
    # Read POS sequences from pairs.txt
    with open(pairs_file, 'r', encoding='utf-8') as f:
        history = []  # For ngram history
        for line in f:
            _, tag = line.strip().split('\t')
            
            if ngram == 2:
                # Bigram model
                if len(history) == 1:
                    prev_tag = history[0]
                    pos_counts[prev_tag][tag] += 1
                    total[prev_tag] += 1
                history = [tag]
                
            elif ngram == 3:
                # Trigram model
                if len(history) == 2:
                    context = tuple(history)
                    pos_counts[context][tag] += 1
                    total[context] += 1
                history = history[-1:] + [tag] if len(history) > 0 else [tag]
    
    # Write POS ngram FST
    with open(output_file, 'w', encoding='utf-8') as f:
        if ngram == 2:
            # Bigram transitions
            for prev_tag, tags in pos_counts.items():
                f.write(f"0 1 {prev_tag} {prev_tag} 0\n")  # Initial transition
                for tag, count in tags.items():
                    prob = count / total[prev_tag]
                    f.write(f"1 1 {tag} {tag} {-1 * prob}\n")  # Transition
            f.write("1 0\n")  # Final state
            
        elif ngram == 3:
            # Trigram transitions
            state_id = 1
            context_map = {}  # Maps contexts to state IDs
            
            # Initial states for bigrams
            for context in pos_counts:
                context_map[context] = state_id
                f.write(f"0 {state_id} {context[0]} {context[0]} 0\n")
                state_id += 1
            
            # Trigram transitions
            for context, tags in pos_counts.items():
                src_state = context_map[context]
                for tag, count in tags.items():
                    prob = count / total[context]
                    new_context = (context[1], tag)
                    
                    if new_context not in context_map:
                        context_map[new_context] = state_id
                        state_id += 1
                    
                    f.write(f"{src_state} {context_map[new_context]} {tag} {tag} {-1 * prob}\n")
            
            # Final states
            for state in range(1, state_id):
                f.write(f"{state} 0\n")

if __name__ == "__main__":
    if len(sys.argv) not in [4,5]:
        print("Usage: python build_pos_lm.py <tags.syms> <pairs.txt> <pos_lm.fst.txt> [ngram=2]")
        print("  ngram: 2 for bigram (default), 3 for trigram")
        sys.exit(1)
    
    tags_syms = sys.argv[1]
    pairs_file = sys.argv[2]
    output_file = sys.argv[3]
    ngram = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    
    if ngram not in [2,3]:
        print("Error: ngram must be 2 or 3")
        sys.exit(1)
    
    build_pos_lm(tags_syms, pairs_file, output_file, ngram)

