from alteration_checker import NORMALIZE_TABLE
from collections import defaultdict

# skip buckets bigger than this (junk / over-merged keys)
MAX_BUCKET = 200

def normalize_key(word):
    # For multi-letter swaps, we manually map them to a single canonical form
    # before passing to the single-character NORMALIZE_TABLE.
    w = word.replace("uw", "w").replace("iy", "y")
    return w.translate(NORMALIZE_TABLE)

def key_candidates(vocab):
    # groups pairs of words that share the same normalized key
    buckets = defaultdict(list)
    for w in vocab:
        buckets[normalize_key(w)].append(w)

    for bucket in buckets.values():
        # skip oversized buckets (too many words share this key)
        if len(bucket) > MAX_BUCKET:
            continue

        if len(bucket) > 1:
            for i in range(len(bucket)):
                for j in range(i + 1, len(bucket)):
                    yield bucket[i], bucket[j]