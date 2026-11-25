import re
from collections import Counter

# A word = letters, optionally joined by a hyphen or apostrophe
# e.g. "mag-aral", "isa't" stay as single tokens
WORD_RE = re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*")

def tokenize(text):
    return WORD_RE.findall(text.lower())

def count_words(path):
    counts = Counter()
    with open(path, encoding="utf-8") as f:
        for line in f:
            counts.update(tokenize(line))
    return counts

def count_capitalized_mid_sentence(path):
    # counts how many times each word appears MID-SENTENCE and capitalized
    # (i.e. not the first word of a sentence/line)
    # returns dict: word_lower -> count
    mid_caps = Counter()
    with open(path, encoding="utf-8") as f:
        for line in f:
            # split into tokens WITH their original case
            tokens = WORD_RE.findall(line)
            for idx, tok in enumerate(tokens):
                # skip first token of the line (sentence-start ambiguous)
                if idx == 0:
                    continue
                # capitalized if first letter is uppercase and rest is lowercase
                if tok[0].isupper() and tok[1:].islower():
                    mid_caps[tok.lower()] += 1
    return mid_caps