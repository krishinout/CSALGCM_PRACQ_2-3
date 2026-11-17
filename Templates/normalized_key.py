import re
from collections import defaultdict

def normalize_key(word):
    # changes o/u to o and e/i to e to group likely variants
    word = re.sub(r'[ou]', 'o', word)
    return re.sub(r'[ei]', 'e', word)

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