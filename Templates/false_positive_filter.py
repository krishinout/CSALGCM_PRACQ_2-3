def keep_pair(w1, w2, c1, c2, dist, dict_words=None, min_len=4, max_ratio=50):
    # returns True if the pair should be kept
    
    # if too short
    if min(len(w1), len(w2)) < min_len:
        return False

    # if one word is way more frequent than the other
    if c1 > 0 and c2 > 0 and max(c1, c2) / min(c1, c2) > max_ratio:
        return False

    # if both are valid words in the dictionary
    if dict_words and w1 in dict_words and w2 in dict_words:
        return False

    return True
