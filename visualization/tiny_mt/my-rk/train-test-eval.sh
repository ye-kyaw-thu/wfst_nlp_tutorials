#!/bin/bash

# Prepare oneline test data
# head က ပုဒ်မ တစ်ခုတည်းဖြစ်နေလို့ tail ကို သုံးဖို့ ဆုံးဖြတ်လိုက်တယ်
tail -n 1 ./train-equal-smt.my > oneline.my

# Building Transducers with training data (i.e. language model, translation model, composing etc.)
time ./translate-nofstdraw.sh ./train-equal-smt.my ./train-equal-smt.rk oneline.my ./all.my ./all.rk ./all.rk

# Testing with WFST MT
time ./multi-test.sh ./all.my ./all.rk ./test.my 2>&1 | tee anymaTrainingDataOnly-test-myrk.log1

# Evaluation
time ./eval.sh ./test.rk hyp.txt.clean

