from alteration_checker import NORMALIZE_TABLE
from collections import defaultdict

def normalize_key(word):
    # merges all the pairs to one letter for grouping
    return word.translate(NORMALIZE_TABLE)

def key_candidates(vocab):
    # groups pairs of words that share the same normalized key
    buckets = defaultdict(list)
    for w in vocab:
        buckets[normalize_key(w)].append(w)

    for bucket in buckets.values():
        if len(bucket) > 1:
            for i in range(len(bucket)):
                for j in range(i + 1, len(bucket)):
                    yield bucket[i], bucket[j]