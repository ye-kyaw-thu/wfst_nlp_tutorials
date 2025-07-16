#!/bin/bash

# Written by Ye Kyaw Thu, LU Lab., Myanmar
# Last updated: 10 July 2025
# How to run: time ./run_tagger.sh otest.txt words.syms tags.syms pos_tagger.fst > otest.hyp  

rm ../fst/tagged_output.txt; 

TEST_FILE="$1"
WORDS_SYMS="$2"
TAGS_SYMS="$3"
POS_TAGGER_FST="$4"

# Create temporary directory
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Sort the POS tagger FST once
fstarcsort --sort_type=ilabel "$POS_TAGGER_FST" > "$TMPDIR/pos_tagger_sorted.fst"

# Process each sentence individually
sentence_num=0
while read -r sentence; do
    if [ -z "$sentence" ]; then
        continue  # Skip empty lines
    fi
    
    # Store original sentence
    echo "$sentence" > "$TMPDIR/current_sentence.txt"
    
    # Create FST for current sentence
    python ../script/prepare_test_data.py "$TMPDIR/current_sentence.txt" "$TMPDIR/sentence.fst.txt" "$WORDS_SYMS"
    
    # Compile and sort sentence FST
    fstcompile --isymbols="$WORDS_SYMS" --osymbols="$WORDS_SYMS" \
        "$TMPDIR/sentence.fst.txt" | \
        fstarcsort --sort_type=olabel > "$TMPDIR/sentence.fst"
    
    # Compose with POS tagger and get raw results
    fstcompose "$TMPDIR/sentence.fst" "$TMPDIR/pos_tagger_sorted.fst" | \
        fstshortestpath | \
        fstprint --isymbols="$WORDS_SYMS" --osymbols="$TAGS_SYMS" > "$TMPDIR/raw_output.txt"
    
    # Use Python to reconstruct original order
    python3 -c "
import sys
from collections import OrderedDict

# Read original sentence
with open('$TMPDIR/current_sentence.txt', 'r', encoding='utf-8') as f:
    original_words = [word.split('/')[0] for word in f.read().strip().split()]

# Read FST output
tag_map = OrderedDict()
with open('$TMPDIR/raw_output.txt', 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 4 and parts[2] != '<eps>':
            tag_map[parts[2]] = parts[3]

# Output in original order
for word in original_words:
    print(f'{word}\t{tag_map.get(word, \"<unk>\")}')
print()  # Blank line between sentences
" >> ../fst/tagged_output.txt

    sentence_num=$((sentence_num + 1))
done < "$TEST_FILE"

if [ $sentence_num -eq 0 ]; then
    echo "Error: No valid sentences found in input file"
    exit 1
fi

#echo "Tagging completed. Processed $sentence_num sentences. Results:"
cat ../fst/tagged_output.txt

