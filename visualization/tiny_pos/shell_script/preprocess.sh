#!/bin/bash

mkdir ../fst
# preprocess
python ../script/preprocess.py ../data/corpus.raw.clean ../fst/pairs.txt ../fst/words.syms ../fst/tags.syms

