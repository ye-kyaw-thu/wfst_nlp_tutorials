#!/bin/bash

# written by Ye Kyaw Thu, LU Lab., Myanmar
# Evaluation with BLEU Metric
# How to use: ./eval.sh reference-filename hypothesis-filename
# e.g. ./eval.sh ./test.rk hyp.txt.clean

ref=$1
hyp=$2

echo "Evaluation with BLEU score:";
#~/tool/moses-bin/ubuntu-17.04/moses/scripts/generic/multi-bleu.perl ./test.my < hyp.txt.clean
#~/tool/moses-bin/ubuntu-17.04/moses/scripts/generic/multi-bleu.perl $ref < $hyp
/home/ye/tool/mosesbin/ubuntu-17.04/moses/scripts/generic/multi-bleu.perl $ref < $hyp

echo "Evaluation with chrF++ score:";
python /home/ye/tool/chrF/chrF++.py -R $ref -H $hyp;
