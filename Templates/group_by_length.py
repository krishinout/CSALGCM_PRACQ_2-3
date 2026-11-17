from collections import defaultdict
from itertools import combinations

def length_blocks(vocab):
    blocks = defaultdict(list)
    for w in vocab:
        blocks[len(w)].append(w)
    return blocks

def length_candidates(vocab, max_len_diff=1, min_len=4):
    blocks = length_blocks(vocab)
    for length in sorted(blocks):
        if length < min_len:
            continue

        # 1. pairs with the same length
        for w1, w2 in combinations(blocks[length], 2):
            yield w1, w2

        # 2. pairs where the second word is longer by 1..max_len_diff
        for d in range(1, max_len_diff + 1):
            longer = blocks.get(length + d)
            if longer:
                for w1 in blocks[length]:
                    for w2 in longer:
                        yield w1, w2

vocab = {"politiko", "pulitiko", "polittico", "bahay", "opo", "upo"}
print(list(length_candidates(vocab)))