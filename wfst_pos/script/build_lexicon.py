"""
for building FST lexicon
Written by Ye Kyaw Thu, LU Lab., Myanmar.
Last update: 10 July 2025
Usage:  
    python ./build_lexicon.py ../fst/pairs.txt ../fst/lexicon.fst.txt ../fst/words.syms ../fst/tags.syms
"""

import sys
from collections import defaultdict

def build_lexicon(pairs_file, lexicon_fst_file, words_syms, tags_syms):
    """Create a weighted lexicon FST (word -> POS) in OpenFST text format."""
    counts = defaultdict(lambda: defaultdict(int))
    
    # Read word-POS pairs and count (word, tag) frequencies
    with open(pairs_file, 'r', encoding='utf-8') as f:
        for line in f:
            word, tag = line.strip().split('\t')
            counts[word][tag] += 1

    # Write lexicon FST (weights = negative log probabilities)
    with open(lexicon_fst_file, 'w', encoding='utf-8') as f:
        for word, tags in counts.items():
            total = sum(tags.values())
            for tag, cnt in tags.items():
                weight = -1 * (cnt / total)  # Tropical semiring
                f.write(f'0 0 {word} {tag} {weight}\n')
        f.write('0 0\n')  # Final state

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python build_lexicon.py <pairs.txt> <lexicon.fst.txt> <words.syms> <tags.syms>")
        sys.exit(1)
    
    pairs_file = sys.argv[1]
    lexicon_fst_file = sys.argv[2]
    words_syms = sys.argv[3]
    tags_syms = sys.argv[4]
    
    build_lexicon(pairs_file, lexicon_fst_file, words_syms, tags_syms)

