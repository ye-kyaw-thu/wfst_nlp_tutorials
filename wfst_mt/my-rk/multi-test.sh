#!/bin/bash

# written by Ye Kyaw Thu, LU Lab., Myanmar
# e.g. $ ./multi-test.sh all.my all.ro head.my
# 

source=$1;
target=$2;
testdata=$3;

# Backup original hyp file
echo "mv hyp.txt hyp.old";
mv hyp.txt hyp.old

cat $testdata | while read -r line
do
    echo "Translation: "${line};
    echo ${line} > ./oneline-test
    #Ref: ./test.sh ./sl.my ./sl.ro ./oneline-tail.ro
#    ./test.sh $source $target ./oneline-test
    ./test-nofstdraw.sh $source $target ./oneline-test

    #Reordering
    tmpline=$(fstprint ./shortest-path.fst | tac | cut -f4 | tr '\n' ' ' | awk 'BEGIN {FS=" ";OFS=" "} {print $NF; for(i=1;i<NF-1;++i) print $i;}' | tr '\n' ' ')

    #writing to hyp.txt
    if test -z "$tmpline" 
    then
        echo ${line} >> hyp.txt
    else
        echo "$tmpline" >> hyp.txt
    fi

done

sed "s/ <\/s> //;" ./hyp.txt > hyp.txt.clean
echo "hypothesis file: hyp.txt.clean"
