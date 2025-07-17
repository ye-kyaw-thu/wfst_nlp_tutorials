#!/bin/bash

sed 's/|/ /g' ../data/mypos-ver.3.0.shuf.txt > ../data/corpus.txt
sed 's/|/ /g' ../data/otest.1k.txt > ../data/otest.txt
