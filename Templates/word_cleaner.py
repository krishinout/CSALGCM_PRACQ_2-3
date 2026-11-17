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

print(tokenize("Ang Politiko ay mag-aaral, 123 pulitiko!"))
# ['ang', 'politiko', 'ay', 'mag-aaral', 'pulitiko']