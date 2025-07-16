#!/bin/bash

cat $1 | sed "s/ /\n/g" | LC_ALL=C sort | uniq
