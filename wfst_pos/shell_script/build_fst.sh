#!/bin/bash

## Written by Ye Kyaw Thu, LU Lab., Myanmar
## Last updated: 11 July 2025
## အရင်ဆုံး lexicon fst ဆောက်တယ်၊ ပြီးတော့ POS tag တွေနဲ့ LM ဆောက်တယ်။
## ပြီးမှ lexicon နဲ့ LM FST နှစ်ခုကို compose လုပ်ပြီး POS tagger FST ဆောက်တယ်။

# Default to bigram if not specified
NGRAM=${1:-2}

# Step 1: Build lexicon FST
python ../script/build_lexicon.py ../fst/pairs.txt ../fst/lexicon.fst.txt ../fst/words.syms ../fst/tags.syms
fstcompile --isymbols=../fst/words.syms --osymbols=../fst/tags.syms ../fst/lexicon.fst.txt ../fst/lexicon.fst

# Step 2: Build POS LM FST with specified ngram
python ../script/build_pos_lm.py ../fst/tags.syms ../fst/pairs.txt ../fst/pos_lm.fst.txt $NGRAM
fstcompile --isymbols=../fst/tags.syms --osymbols=../fst/tags.syms ../fst/pos_lm.fst.txt ../fst/pos_lm.fst

# Step 3: Compose lexicon and LM
fstarcsort --sort_type=olabel ../fst/lexicon.fst > ../fst/lexicon_sorted.fst
fstarcsort --sort_type=ilabel ../fst/pos_lm.fst > ../fst/pos_lm_sorted.fst
fstcompose ../fst/lexicon_sorted.fst ../fst/pos_lm_sorted.fst ../fst/pos_tagger.fst

echo "FST model built: pos_tagger.fst (using ${NGRAM}-gram POS LM)"

