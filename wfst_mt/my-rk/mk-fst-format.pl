#!/usr/bin/env perl

# change to FST format
# Written by Ye Kyaw Thu,
# Visiting Professor,
# Language and Semantic Technology Research Team (LST), NECTEC, Thailand
#
# How to use:
# $ head -n 1 ./head.kc > input1.kc
# $ perl ./mk-fst-format.pl ./input1.kc > input1.txt

use strict;
use warnings;
use utf8;

binmode(STDIN, ":utf8");
binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");

open (my $inputFILE,"<:encoding(utf8)", $ARGV[0]) or die "Couldn't open input file $ARGV[0]!, $!\n";


while (!eof($inputFILE)) {

   my $line = <$inputFILE>;
   my $count=0; 
   if (($line ne '') & ($line !~ /^ *$/)) {
      chomp($line);
      my @word = split(/ /, $line);
         foreach (@word) {
            print("$count ", $count+1, " $_ $_\n");
            $count =$count+1;
         }
         print("$count ", $count+1," </s> </s>\n", $count+1);
   }
   print("\n");
}
close($inputFILE);

