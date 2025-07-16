"""
Create lexicon FST from word list.
Written by Ye Kyaw thu, LU Lab., Myanmar.
Last updated: 11 July 2025
Usage:
    python mk_lexicon.py < train.vocab > lexicon.txt
"""

#!/usr/bin/env python3
import sys
import argparse
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser(description='Create lexicon FST from word list')
    parser.add_argument('--input', metavar='FILE',
                       help='Input word list file (default: stdin)',
                       type=argparse.FileType('r', encoding='utf-8'),
                       default=sys.stdin)
    parser.add_argument('--output', metavar='FILE',
                       help='Output FST file (default: stdout)',
                       type=argparse.FileType('w', encoding='utf-8'),
                       default=sys.stdout)
    
    args = parser.parse_args()

    newstate = 1
    
    try:
        for line in args.input:
            line = line.strip()
            if not line:
                continue
                
            # Prepare input symbols (characters + <w>)
            inputsym = list(line) + ['<w>']
            # Prepare output symbols (word + repeated <eps>)
            outputsym = [line] + ['<eps>'] * (len(inputsym) - 1)
            
            currstate = 0
            score = ' 1'
            
            while inputsym:
                nextstate = 0 if len(inputsym) == 1 else newstate
                if len(inputsym) > 1:
                    newstate += 1
                
                args.output.write(f"{currstate} {nextstate} {inputsym.pop(0)} {outputsym.pop(0)}{score}\n")
                currstate = nextstate
                score = ''
    
        # Write the special transitions
        args.output.write("0 0 <s> <s>\n")
        args.output.write("0\n")
        
    except IOError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
    finally:
        if args.input is not sys.stdin:
            args.input.close()
        if args.output is not sys.stdout:
            args.output.close()

if __name__ == '__main__':
    main()

