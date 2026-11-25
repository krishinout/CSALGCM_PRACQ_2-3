
def keep_pair(w1, w2, c1, c2, dist, dict_words=None, min_len=4, max_ratio=50,
              mid_caps=None, proper_noun_ratio=0.5):
    # returns True if the pair should be kept

    # if too short
    if min(len(w1), len(w2)) < min_len:
        return False

    # if one word is way more frequent than the other
    if c1 > 0 and c2 > 0 and max(c1, c2) / min(c1, c2) > max_ratio:
        return False

    # if BOTH words look like proper nouns, reject
    # (a proper noun = capitalized mid-sentence more than proper_noun_ratio of the time)
    if mid_caps is not None:
        r1 = mid_caps.get(w1, 0) / c1 if c1 > 0 else 0
        r2 = mid_caps.get(w2, 0) / c2 if c2 > 0 else 0
        if r1 > proper_noun_ratio and r2 > proper_noun_ratio:
            return False

   # keep lang kung at least one word ay real word sa dictionary
    if dict_words is not None:
        if w1 not in dict_words and w2 not in dict_words:
            return False

    return True

