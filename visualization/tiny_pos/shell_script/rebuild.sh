#!/bin/bash

# Default to bigram, but allow override
NGRAM=${1:-2}

# Clean previous files
rm -f ../fst/*.fst ../fst/*.fst.txt

# Rebuild from scratch
./preprocess.sh
./build_fst.sh $NGRAM

