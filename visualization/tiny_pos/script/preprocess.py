import sys
from collections import defaultdict

def preprocess_corpus(input_file, output_pairs, words_file, pos_tags_file):
    """Convert a tagged corpus into word-POS pairs and extract vocabularies."""
    word_counts = defaultdict(int)
    pos_counts = defaultdict(int)
    pairs = []

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Split into word/tag tokens (handling multiple spaces/punctuation)
            tokens = line.strip().split()
            for token in tokens:
                if '/' in token:
                    word, tag = token.split('/', 1)
                    word = word.strip()
                    tag = tag.split('|')[0].strip()  # Take first tag if multiple (e.g., "n|v" → "n")
                    if word and tag:
                        pairs.append((word, tag))
                        word_counts[word] += 1
                        pos_counts[tag] += 1

    # Write word-POS pairs
    with open(output_pairs, 'w', encoding='utf-8') as f:
        for word, tag in pairs:
            f.write(f"{word}\t{tag}\n")

    # Write vocabulary files
    with open(words_file, 'w', encoding='utf-8') as f:
        f.write("<eps>\t0\n")  # OpenFST requires <eps> as first symbol
        f.write("<unk>\t1\n")  # OpenFST requires <eps> as first symbol
        for idx, word in enumerate(sorted(word_counts.keys()), 1):
            f.write(f"{word}\t{idx}\n")

    with open(pos_tags_file, 'w', encoding='utf-8') as f:
        f.write("<eps>\t0\n")
        f.write("<unk>\t1\n")  # Add <unk> as the first POS tag
        for idx, tag in enumerate(sorted(pos_counts.keys()), 2):  # Start indexing from 2
            f.write(f"{tag}\t{idx}\n")

    print(f"Preprocessing complete. Output files: {output_pairs}, {words_file}, {pos_tags_file}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python preprocess.py <input_corpus.txt> <output_pairs.txt> <words.syms> <pos_tags.syms>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_pairs = sys.argv[2]
    words_file = sys.argv[3]
    pos_tags_file = sys.argv[4]

    preprocess_corpus(input_file, output_pairs, words_file, pos_tags_file)

