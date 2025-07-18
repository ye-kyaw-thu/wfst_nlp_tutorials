#!/bin/bash -v

SOURCE=$1;
TARGET=$2;

time python2.7 /home/ye/tool/anymalign/anymalign.py  -i 5 -a 5 -w ./train.$SOURCE ./train.$TARGET > alignment-train.txt
wc ./alignment-train.txt

head ./alignment-train.txt
tail ./alignment-train.txt

cut -f1 ./alignment-train.txt > train-equal-smt.$SOURCE
cut -f2 ./alignment-train.txt > train-equal-smt.$TARGET

head ./train-equal-smt.$SOURCE
head ./train-equal-smt.$TARGET

tail ./train-equal-smt.$SOURCE
tail ./train-equal-smt.$TARGET

wc ./train-equal-smt.$SOURCE
wc ./train-equal-smt.$TARGET

echo "Alignment path:"
pwd;


