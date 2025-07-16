#!/bin/bash
set -e

# *** onetoone symbol file should covered both training and test data because of FST working nature (if not, you have to face Out of Symbol problem)
# e.g. (base) ye@ykt-pro:/media/ye/project1/tool/mtandseq2seq-code/21-wfst/my-name-exp$ ./test.sh ./all.my ./all.ro ./oneline-tail.ro

corpuse=$1;
corpusf=$2;
input=$3;

# Create a onetoone symbol file
python onetoone.py $corpuse $corpusf > onetoone.all.txt
python symbols.py 2 < onetoone.all.txt > onetoone.all.isym

# Prepare test data FST
perl ./mk-fst-format.pl $input > $input.formatted
inputfst=$input.formatted

# Formulate the input as a WFST
#fstcompile --keep_isymbols --keep_osymbols --isymbols=onetoone.isym --osymbols=onetoone.isym $input input.fst
fstcompile --keep_isymbols --keep_osymbols --isymbols=onetoone.all.isym --osymbols=onetoone.all.isym $inputfst ${inputfst%.*}.fst
#fstdraw --portrait --acceptor ${inputfst%.*}.fst ${inputfst%.*}.dot
#dot -Tps:cairo ${inputfst%.*}.dot > ${inputfst%.*}.ps
#ps2pdf ${inputfst%.*}.ps
#pdfcrop ${inputfst%.*}.pdf
#mv ${inputfst%.*}-crop.pdf ${inputfst%.*}.pdf
#evince ${inputfst%.*}.pdf

# Compose together into a search graph
fstcompose ${inputfst%.*}.fst composed.fst search.fst
#fstdraw --portrait search.fst search.dot
#dot -Tps:cairo search.dot > search.ps
#ps2pdf search.ps
#pdfcrop search.pdf
#mv search-crop.pdf search.pdf
#evince ./search.pdf

# Remove epsilons to make it easier to read
fstrmepsilon search.fst searchrmeps.fst
#fstdraw --portrait searchrmeps.fst searchrmeps.dot
#dot -Tps:cairo searchrmeps.dot > searchrmeps.ps
#ps2pdf searchrmeps.ps
#pdfcrop searchrmeps.pdf
#mv searchrmeps-crop.pdf searchrmeps.pdf
#evince ./searchrmeps.pdf

# Print the shortest path
fstshortestpath ./searchrmeps.fst > shortest-path.fst
#fstdraw --portrait --isymbols=onetoone.isym  --osymbols=onetoone.isym ./shortest-path.fst | dot -Tpdf -Gsize=6,3 -Eheadport=e -Etailport=w > shortest-path.pdf
#fstdraw --portrait --isymbols=onetoone.isym  --osymbols=$corpuse.words.sym ./shortest-path.fst | dot -Tpdf -Gsize=6,3 -Eheadport=e -Etailport=w > shortest-path.pdf

#evince ./shortest-path.pdf
