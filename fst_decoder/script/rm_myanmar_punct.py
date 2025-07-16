"""
for removing two Myanmar puncutation characters.
Written by Ye Kyw Thu, LU Lab., Myanmar.
"""

#!/usr/bin/env python3
import argparse
import sys

def remove_myanmar_punctuation(text):
    """Remove Myanmar punctuation characters ၊ and ။ from text."""
    return text.replace('၊', '').replace('။', '')

def process_stream(input_stream, output_stream):
    """Process input stream and write to output stream."""
    for line in input_stream:
        # Remove Myanmar punctuation
        cleaned_line = remove_myanmar_punctuation(line)
        # Write to output
        output_stream.write(cleaned_line)

def main():
    parser = argparse.ArgumentParser(
        description='Remove Myanmar punctuation characters (၊ and ။) from text.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--input',
        type=str,
        help='Input file path (default: stdin)',
        default=None
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (default: stdout)',
        default=None
    )
    
    args = parser.parse_args()
    
    # Determine input source
    input_stream = open(args.input, 'r', encoding='utf-8') if args.input else sys.stdin
    
    # Determine output destination
    output_stream = open(args.output, 'w', encoding='utf-8') if args.output else sys.stdout
    
    try:
        process_stream(input_stream, output_stream)
    finally:
        # Close files if we opened them
        if args.input:
            input_stream.close()
        if args.output:
            output_stream.close()

if __name__ == '__main__':
    main()


