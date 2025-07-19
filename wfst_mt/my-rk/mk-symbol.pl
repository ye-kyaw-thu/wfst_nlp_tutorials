#!/usr/bin/env perl

# Myanmar sentence breaking based on syllable+potema list
# Written by Ye Kyaw Thu,
# Visiting Professor,
# Language and Semantic Technology Research Team (LST), NECTEC, Thailand
#
# How to use:
# $ perl
# e.g. ./mk-uniq-word.sh ./head.kc > ./head.kc.uniq
# perl ./mk-symbol.pl ./head.kc.uniq > bigram.ssym
# ./mk-uniq-word.sh ./head.my > ./head.my.uniq
# perl ./mk-symbol.pl ./head.my.uniq > bigram.ssym

use strict;
use warnings;
use utf8;

binmode(STDIN, ":utf8");
binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");

print("<s> 0\n");
print("NULL 1\n");

open (my $inputFILE,"<:encoding(utf8)", $ARGV[0]) or die "Couldn't open input file $ARGV[0]!, $!\n";

my $count=2; 
while (!eof($inputFILE)) {

   my $line = <$inputFILE>;
   if (($line ne '') & ($line !~ /^ *$/)) {
      chomp($line);
      print("$line $count\n");
      $count=$count+1;
   }
}

print("</s> $count\n");
close($inputFILE);

