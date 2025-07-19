#!/bin/bash

# How to run:
# e.g. bash ./shortest-path-to-line.sh ./shortest-path.fst

fstprint $1 | tac | cut -f4 | tr '\n' ' ' | awk 'BEGIN {FS=" ";OFS=" "} {print $NF; for(i=1;i<NF-1;++i) print $i;}' | tr '\n' ' '
