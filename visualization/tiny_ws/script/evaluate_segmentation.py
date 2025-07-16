"""
Usage:
    python ./script/evaluate_segmentation.py --ref data/otest.nopipe.word --hyp open_test.hyp --top-k 10 > open_tesst_score.txt
    python ./script/evaluate_segmentation.py --ref data/ctest10.nopipe.word --hyp closed_test.hyp --top-k 10 > closed_test_score.txt
"""

import argparse
from collections import Counter
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        description="Boundary-based evaluation for word segmentation (Precision, Recall, F1 + Token-level Top-K Errors)"
    )
    parser.add_argument("--ref", type=str, required=True,
                        help="Path to reference (gold) word segmented file")
    parser.add_argument("--hyp", type=str, required=True,
                        help="Path to hypothesis file with line ID and segmented output")
    parser.add_argument("--top-k", type=int, default=10,
                        help="Top-K most frequent token-level segmentation errors to report (default: 10)")
    return parser.parse_args()

def load_reference(ref_path):
    ref_dict = {}
    with open(ref_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            tokens = line.strip().split()
            ref_dict[i] = tokens
    return ref_dict

def load_hypothesis(hyp_path):
    hyp_dict = {}
    with open(hyp_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '|||' not in line:
                continue
            idx_str, hyp = line.strip().split('|||', maxsplit=1)
            try:
                idx = int(idx_str.strip())
                tokens = hyp.strip().split()
                hyp_dict[idx] = tokens
            except ValueError:
                continue
    return hyp_dict

def get_boundaries(tokens):
    """Return set of character offset boundaries for token list"""
    boundaries = set()
    offset = 0
    for token in tokens[:-1]:  # No boundary after last token
        offset += len(token)
        boundaries.add(offset)
    return boundaries

def extract_token_level_errors_by_spans(ref_tokens, hyp_tokens):
    errors = []

    # Reconstruct original sentence
    ref_text = "".join(ref_tokens)
    hyp_text = "".join(hyp_tokens)

    if ref_text != hyp_text:
        # Can't compare if character sequences mismatch (e.g., decoding issues)
        return errors

    def get_spans(tokens):
        spans = []
        offset = 0
        for token in tokens:
            start = offset
            end = offset + len(token)
            spans.append((start, end, token))
            offset = end
        return spans

    ref_spans = get_spans(ref_tokens)
    hyp_spans = get_spans(hyp_tokens)

    hyp_span_set = {(start, end) for (start, end, _) in hyp_spans}
    hyp_span_map = {(start, end): token for (start, end, token) in hyp_spans}

    for (start, end, gold_token) in ref_spans:
        if (start, end) not in hyp_span_set:
            # Find predicted tokens that overlap this gold span
            merged_pred = ""
            for (h_start, h_end, h_token) in hyp_spans:
                if h_start >= end:
                    break
                if h_end <= start:
                    continue
                merged_pred += h_token
            errors.append((gold_token, merged_pred))

    return errors

def evaluate(ref_dict, hyp_dict):
    TP, FP, FN = 0, 0, 0
    error_counter = Counter()

    for idx, ref_tokens in ref_dict.items():
        ref_bounds = get_boundaries(ref_tokens)
        hyp_tokens = hyp_dict.get(idx)

        if hyp_tokens is None:
            FN += len(ref_bounds)
            continue

        hyp_bounds = get_boundaries(hyp_tokens)

        TP += len(ref_bounds & hyp_bounds)
        FP += len(hyp_bounds - ref_bounds)
        FN += len(ref_bounds - hyp_bounds)

        # Track token-level errors
        for ref_tok, hyp_tok in extract_token_level_errors_by_spans(ref_tokens, hyp_tokens):

            if ref_tok != hyp_tok:
                error_counter[(ref_tok, hyp_tok)] += 1

    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall    = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1, error_counter

def main():
    args = parse_args()

    ref_dict = load_reference(args.ref)
    hyp_dict = load_hypothesis(args.hyp)

    precision, recall, f1, error_counter = evaluate(ref_dict, hyp_dict)

    print("\n=== Word Segmentation Evaluation ===")
    print(f"Total Ref lines: {len(ref_dict)}")
    print(f"Total Hyp lines: {len(hyp_dict)}\n")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")

    print(f"\nTop-{args.top_k} Frequent Token-level Segmentation Errors:")
    for i, ((ref_tok, hyp_tok), count) in enumerate(error_counter.most_common(args.top_k), 1):
        print(f"[{i}] Count: {count}")
        print(f"  REF token:     {ref_tok}")
        print(f"  Predicted as:  {hyp_tok}\n")

if __name__ == "__main__":
    main()

