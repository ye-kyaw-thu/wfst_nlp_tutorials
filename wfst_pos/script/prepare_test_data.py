import sys

def load_symbols(sym_file):
    """Load symbol-to-id mapping from a .syms file."""
    symbols = {}
    with open(sym_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                symbols[parts[0]] = parts[1]  # Keep as string
    return symbols

def convert_to_test_fst(input_file, output_fst_txt, words_syms):
    """Write FST using symbol strings (not IDs)"""
    word2id = load_symbols(words_syms)
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_fst_txt, 'w', encoding='utf-8') as fout:
        for line in fin:
            words = [word.split('/')[0] for word in line.strip().split()]
            for i, word in enumerate(words):
                word_sym = word if word in word2id else "<unk>"
                fout.write(f"{i} {i+1} {word_sym} {word_sym}\n")
            fout.write(f"{len(words)} 0\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python prepare_test_data.py <input_file> <output.fst.txt> <words.syms>")
        sys.exit(1)
    convert_to_test_fst(sys.argv[1], sys.argv[2], sys.argv[3])

