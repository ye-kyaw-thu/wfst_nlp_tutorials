"""
for building word vocab from input text
written by Ye Kyaw Thu, LU Lab., Myanmar
Last updated: 11 July 2025
"""

#!/usr/bin/env python3
import sys
import argparse
from collections import defaultdict

def process_input(input_stream, vocab):
    """Process input stream and update vocabulary counts"""
    for line in input_stream:
        line = line.strip()
        if line:  # Skip empty lines
            for word in line.split():
                vocab[word] += 1

def main():
    parser = argparse.ArgumentParser(description='Build word vocabulary from input text')
    parser.add_argument('--input', metavar='FILE', 
                       help='Input text file (default: stdin)',
                       type=argparse.FileType('r', encoding='utf-8'),
                       default=sys.stdin)
    parser.add_argument('--output', metavar='FILE',
                       help='Output vocabulary file (default: stdout)',
                       type=argparse.FileType('w', encoding='utf-8'),
                       default=sys.stdout)
    
    args = parser.parse_args()

    # Build vocabulary
    vocab = defaultdict(int)
    
    try:
        process_input(args.input, vocab)
    except UnicodeDecodeError:
        sys.stderr.write("Error: Input contains invalid UTF-8 characters\n")
        sys.exit(1)
    except IOError as e:
        sys.stderr.write(f"Error reading input: {e}\n")
        sys.exit(1)

    # Output vocabulary (sorted)
    try:
        for word in sorted(vocab.keys()):
            args.output.write(f"{word}\n")
    except IOError as e:
        sys.stderr.write(f"Error writing output: {e}\n")
        sys.exit(1)

    # Close files if they were opened by argparse
    if args.input is not sys.stdin:
        args.input.close()
    if args.output is not sys.stdout:
        args.output.close()

if __name__ == '__main__':
    main()
