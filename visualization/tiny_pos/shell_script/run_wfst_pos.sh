#!/bin/bash

# 3gram FST POS LM
./rebuild.sh 3

#POS tagging
time ./run_tagger.sh otest.txt words.syms tags.syms pos_tagger.fst > otest_3gram.hyp

# columne to line conversion
perl ./col2line.pl ./otest_3gram.hyp > otest_3gram.hyp.line

# evaluation
python2.7 ./evaluate.py otest.txt otest_3gram.hyp.line

