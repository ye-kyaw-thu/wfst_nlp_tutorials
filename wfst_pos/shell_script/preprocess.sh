#!/bin/bash

# input corpus ဖိုင်ကို word<TAB>Tag ဆိုတဲ့ ကော်လံနှစ်ခုခွဲပြီး ထောင်းလိုက်တွဲထားတဲ့ ပုံစံပြောင်းတာရယ်
# FSA, FST တွေဆောက်ဖို့အတွက် လိုအပ်တဲ့ သင်္ကေတဖိုင်တွေ ထုတ်ဖို့ run တဲ့ shell script ပါ။  

mkdir ../fst
# preprocess
python ../script/preprocess.py ../data/corpus.txt ../fst/pairs.txt ../fst/words.syms ../fst/tags.syms

