import argparse

from word_cleaner import count_words, count_capitalized_mid_sentence
from normalized_key import key_candidates
from weighted_levenshtein import edit_with_diff
from alteration_checker import is_valid_alteration
from false_positive_filter import keep_pair
from csv_writer import write_pairs_to_csv

INPUT_FILE = "Raw.txt"
OUTPUT_FILE = "variants.csv"
DICT_FILE = "tagalog_dict.txt"
MIN_FILE = None
MIN_LEN = 4 #shortest word the pwede
MAX_RATIO = 50 #max freq ratio between the two words

def load_dictionary(path):
    with open(path, encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}
    
def main():
    print(f"Reading {INPUT_FILE}")
    counts = count_words(INPUT_FILE)
    vocab = list(counts)
    print(f" {len(vocab):,} unique words, {sum(counts.values()):,} total")

    mid_caps = count_capitalized_mid_sentence(INPUT_FILE)
    print(f" {len(mid_caps):,} words seen capitalized mid-sentence")

    dict_words = load_dictionary(DICT_FILE) if DICT_FILE else None

    rows = []
    num_candidates = 0
    seen = set()

    for word1, word2 in key_candidates(vocab):
        num_candidates += 1

        result = edit_with_diff(word1, word2)
        if result is None:
            continue
        dist, diffs = result

        if not diffs or not is_valid_alteration(diffs):
            continue

        if counts[word2] > counts[word1]:
            word1, word2 = word2, word1
            diffs = [" vs. ".join(reversed(diff.split(" vs. "))) for diff in diffs]

        key = (word1, word2)
        if key in seen:
            continue
        seen.add(key)

        if not keep_pair(word1, word2, counts[word1], counts[word2], dist,
                         dict_words=dict_words,
                         min_len=MIN_LEN, max_ratio=MAX_RATIO,
                         mid_caps=mid_caps):
            continue

        rows.append((word1, word2, counts[word1], counts[word2], "; ".join(diffs)))
    
    print(f" {num_candidates:,} candidate pairs checked, {len(rows):,} kept")
    
    #writes the CSV file
    rows.sort(key=lambda r: r[2] + r[3], reverse=True)
    write_pairs_to_csv(OUTPUT_FILE, rows)
    print(f"Wrote {OUTPUT_FILE}")

if __name__ == "__main__":
    main()