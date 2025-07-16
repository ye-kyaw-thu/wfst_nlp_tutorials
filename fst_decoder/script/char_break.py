#!/usr/bin/env python3
import sys
import argparse

def process_line(line):
    """Process a single line: remove spaces and separate characters"""
    line = line.replace(' ', '')
    return ' '.join(list(line)) + '\n'

def main():
    parser = argparse.ArgumentParser(
        description='Separate characters in each line with spaces',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--input', metavar='FILE',
                       help='Input file (default: stdin)',
                       type=argparse.FileType('r', encoding='utf-8'),
                       default=sys.stdin)
    parser.add_argument('--output', metavar='FILE',
                       help='Output file (default: stdout)',
                       type=argparse.FileType('w', encoding='utf-8'),
                       default=sys.stdout)
    
    args = parser.parse_args()

    try:
        for line in args.input:
            line = line.strip()
            processed = process_line(line)
            args.output.write(processed)
    except UnicodeDecodeError:
        sys.stderr.write("Error: Input contains invalid UTF-8 characters\n")
        sys.exit(1)
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

