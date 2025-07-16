#!/bin/bash
set -e

# written by Ye Kyaw Thu, LU Lab., Myanmar
# before running this shell script, you have to run "mk-train-symbol.sh" for both source and target trainining files
# Build FST Translation Model and test witn one line example:
# $ ./translate-nofstdraw.sh ./train.my ./train.ro ./oneline.my ./all.my ./all.ro

corpuse=$1;
corpusf=$2;
input=$3;

# open testing လုပ်တဲ့အခါမှာ symbol တွေက မရှိရင် error တက်လို့ ...
allsource=$4;
alltarget=$5;

# Create symbol file for target language
echo "Create symbol file for target language ...";
./mk-uniq-word.sh $corpusf > $corpusf.words
perl ./mk-symbol.pl ./$corpusf.words > $corpusf.words.sym

# Create symbol file
#echo "Create symbol file for source language ...";
#./mk-uniq-word.sh $corpuse > $corpuse.words
#perl ./mk-symbol.pl ./$corpuse.words > $corpuse.words.sym

# Prepare test data FST
perl ./mk-fst-format.pl $input > $input.formatted
inputfst=$input.formatted
echo "Preparing test data FST finished!"

# Create a bigram language model from the corpus
python bigram.py < $corpusf > bigram.txt
python symbols.py 2 < bigram.txt > bigram.isym

fstcompile --keep_isymbols --keep_osymbols --isymbols=bigram.isym --osymbols=bigram.isym bigram.txt bigram.fst
echo "fstcompile for the bigram language model FST finished!"
#fstdraw --portrait --acceptor --show_weight_one --ssymbols=$corpuse.words.sym bigram.fst bigram.dot
#dot -Tps:cairo bigram.dot > bigram.ps
#ps2pdf bigram.ps
#pdfcrop bigram.pdf
#mv bigram-crop.pdf bigram.pdf
#evince ./bigram.pdf

# Create a one-to-one translation model
#python onetoone.py $corpuse $corpusf > onetoone.txt
#python symbols.py 2 < onetoone.txt > onetoone.isym
#python symbols.py 3 < onetoone.txt > onetoone.osym

# for translation model
python onetoone.py $corpuse $corpusf > onetoone.txt
# try to cover open test symbol ... 
python onetoone.py $allsource $alltarget > all_src_trg.txt
python symbols.py 2 < all_src_trg.txt > onetoone.isym
python symbols.py 3 < all_src_trg.txt > onetoone.osym

fstcompile --keep_isymbols --keep_osymbols --isymbols=onetoone.isym --osymbols=onetoone.osym onetoone.txt onetoone.fst
echo "fstcompile for the translation model FST finished!"
#fstdraw --portrait --acceptor --show_weight_one onetoone.fst onetoone.dot
#dot -Tps:cairo onetoone.dot > onetoone.ps
#ps2pdf onetoone.ps
#pdfcrop onetoone.pdf
#mv onetoone-crop.pdf onetoone.pdf
#evince onetoone.pdf

# Compose together a translation model and languge model
#fstcompile --keep_isymbols --keep_osymbols --isymbols=train.my.words.sym --osymbols=bigram.isym onetoone.txt | fstarcsort --sort_type=olabel > onetoone.fst
#fstcompose onetoone.fst bigram.fst composed.fs	t
fstcompile --keep_isymbols --keep_osymbols --isymbols=onetoone.isym --osymbols=bigram.isym onetoone.txt | fstarcsort --sort_type=olabel > onetoone.fst
echo "compile success!!";

fstcompose onetoone.fst bigram.fst composed.fst
echo "fstcompose together a translation model and language model finished!"
#fstdraw --portrait --show_weight_one composed.fst composed.dot
#dot -Tps:cairo composed.dot > composed.ps
#ps2pdf composed.ps
#pdfcrop composed.pdf
#mv composed-crop.pdf composed.pdf
#evince composed.pdf

# Formulate the input as a WFST
#fstcompile --keep_isymbols --keep_osymbols --isymbols=onetoone.isym --osymbols=onetoone.isym $input input.fst
#fstcompile --keep_isymbols --keep_osymbols --isymbols=onetoone.isym --osymbols=onetoone.isym $inputfst ${inputfst%.*}.fst
fstcompile --keep_isymbols --keep_osymbols --isymbols=onetoone.isym --osymbols=onetoone.isym $inputfst ${inputfst%.*}.fst

echo "fstcompile for the input sentence finished!"
#fstdraw --portrait --acceptor ${inputfst%.*}.fst ${inputfst%.*}.dot
#dot -Tps:cairo ${inputfst%.*}.dot > ${inputfst%.*}.ps
#ps2pdf ${inputfst%.*}.ps
#pdfcrop ${inputfst%.*}.pdf
#mv ${inputfst%.*}-crop.pdf ${inputfst%.*}.pdf
#evince ${inputfst%.*}.pdf

# Compose together into a search graph
fstcompose ${inputfst%.*}.fst composed.fst search.fst
echo "fstcompose together into a search graph finished!"
#fstdraw --portrait search.fst search.dot
#dot -Tps:cairo search.dot > search.ps
#ps2pdf search.ps
#pdfcrop search.pdf
#mv search-crop.pdf search.pdf
#evince ./search.pdf

# Remove epsilons to make it easier to read
fstrmepsilon search.fst searchrmeps.fst
echo "fstrmepsilon finished!"
#fstdraw --portrait searchrmeps.fst searchrmeps.dot
#dot -Tps:cairo searchrmeps.dot > searchrmeps.ps
#ps2pdf searchrmeps.ps
#pdfcrop searchrmeps.pdf
#mv searchrmeps-crop.pdf searchrmeps.pdf
#evince ./searchrmeps.pdf

# Print the shortest path
fstshortestpath ./searchrmeps.fst > shortest-path.fst
echo "finding the shortest path finished!"
#fstdraw --portrait --isymbols=onetoone.isym  --osymbols=onetoone.isym ./shortest-path.fst | dot -Tpdf -Gsize=6,3 -Eheadport=e -Etailport=w > shortest-path.pdf
#fstdraw --portrait --isymbols=train.my.words.sym  --osymbols=train.ro.words.sym ./shortest-path.fst | dot -Tpdf -Gsize=6,3 -Eheadport=e -Etailport=w > shortest-path.pdf
fstdraw --portrait --isymbols=onetoone.isym  --osymbols=$corpusf.words.sym ./shortest-path.fst | dot -Tpdf -Gsize=6,3 -Eheadport=e -Etailport=w > shortest-path.pdf

evince ./shortest-path.pdf

# Shortest-path to normal sentence
bash ./shortest-path-to-line.sh ./shortest-path.fst

