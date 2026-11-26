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
MIN_LEN = 4
MIN_COUNT = 2
MAX_RATIO = 50


def load_dictionary(path):
    with open(path, encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


def main():
    print(f"Reading {INPUT_FILE}")
    counts = count_words(INPUT_FILE)
    vocab = [w for w, c in counts.items() if c >= MIN_COUNT]
    print(f" {len(counts):,} unique words -> {len(vocab):,} kept (count >= {MIN_COUNT})")

    mid_caps = count_capitalized_mid_sentence(INPUT_FILE)
    dict_words = load_dictionary(DICT_FILE) if DICT_FILE else None

    rows = []
    num_candidates = 0
    num_valid_diffs = 0
    num_kept = 0
    num_hyphen = 0
    seen = set()

    # standard swap-based variants
    for word1, word2 in key_candidates(vocab):
        num_candidates += 1
        result = edit_with_diff(word1, word2)
        if result is None:
            continue
        dist, diffs = result

        if not diffs or not is_valid_alteration(diffs):
            continue
        num_valid_diffs += 1

        # put the LESS frequent word first
        if (counts[word2], word2) < (counts[word1], word1):
            word1, word2 = word2, word1
            diffs = [" vs. ".join(reversed(diff.split(" vs. "))) for diff in diffs]

        key = (word1, word2)
        if key in seen:
            continue
        seen.add(key)

        if not keep_pair(word1, word2, counts[word1], counts[word2], dist,
                         dict_words=dict_words, min_len=MIN_LEN, max_ratio=MAX_RATIO,
                         mid_caps=mid_caps):
            continue

        num_kept += 1
        rows.append((word1, word2, counts[word1], counts[word2], "; ".join(diffs)))

    # hyphen-only variants
    # we extract pairs where the two words are identical after removing hyphens.
    for word in vocab:
        if "-" not in word:
            continue
        stripped = word.replace("-", "")
        if stripped == word or stripped not in counts:
            continue

        # skip if too short after stripping
        if min(len(word), len(stripped)) < MIN_LEN:
            continue

        # skip if the pair is already in the output
        w1, w2 = (stripped, word) if (counts[stripped], stripped) < (counts[word], word) else (word, stripped)
        key = (w1, w2)
        if key in seen:
            continue
        seen.add(key)

        # proper-noun filter 
        r1 = mid_caps.get(w1, 0) / counts[w1] if counts[w1] > 0 else 0
        r2 = mid_caps.get(w2, 0) / counts[w2] if counts[w2] > 0 else 0
        if r1 > 0.5 or r2 > 0.5:
            continue

        num_hyphen += 1
        rows.append((w1, w2, counts[w1], counts[w2], "-"))

    print(f" {num_candidates:,} candidate pairs checked")
    print(f" {num_valid_diffs:,} passed alteration check")
    print(f" {num_kept:,} passed all filters (kept)")
    print(f" {num_hyphen:,} hyphen-only variants added")

    rows.sort(key=lambda r: r[2] + r[3], reverse=True)
    write_pairs_to_csv(OUTPUT_FILE, rows)
    print(f"Wrote {len(rows):,} total rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
