#!/bin/bash

# making symbol files for both train.src and train.trg
# you should run two times (e.g. train.my, train.ro)
# *** this script should be run before running ./translate.sh
# Written by Ye Kyaw Thu, Visiting Professor, LST, NECTEC, Thailand
# How to run:
# ./mk-train-symbol.sh train.my
# ./mk-train-symbol.sh train.ro

# make uniq words
bash ./mk-uniq-word.sh ./$1 > $1.words
wc $1.words

# make symbol files
#perl ./mk-symbol.pl ./$1.words > $1.words.sym
python ./mk-symbol.py --input ./$1.words --output $1.words.sym
