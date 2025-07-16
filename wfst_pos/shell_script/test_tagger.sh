#!/bin/bash

# Convert input sentence to FST
echo "0 1 ဈေး ဈေး
1 2 လျှော့ လျှော့
2 3.0" > input.fst.txt
fstcompile --isymbols=words.syms --osymbols=words.syms input.fst.txt input.fst

# Run through the tagger
fstcompose input.fst pos_tagger.fst output.fst
fstshortestpath output.fst best_path.fst
fstprint --isymbols=words.syms --osymbols=tags.syms best_path.fst
