from alteration_checker import NORMALIZE_TABLE

# english words na nagca-cause ng false positives (inspired by sir ocos paper doon sa limitation part kaya ginawan nalang siya small dict)
ENGLISH_WORDS = {
    "date", "tale", "pure", "hate", "male", "deal", "real", "dome", 
    "modal", "moral", "role", "rule", "will", "well", "hill", "hell", 
    "ring", "ding", "song", "sung", "long", "lung", "most", "must", 
    "bull", "boll", "bill", "bell", "nick", "neck", "tapi", "tape", 
    "name", "nami", "seda", "sida", "mime", "meme", "chick", "check", 
    "lute", "lote", "lomo", "lumo", "karo", "karu"
}

# pairs that pass the rules but mean different things (based from previous variants output the produced these pairs kahit mali sdhj)
NOT_VARIANTS = {
    frozenset(("mora", "moda")), frozenset(("mora", "mura")),
    frozenset(("muda", "moda")), frozenset(("muda", "mura")),
    frozenset(("dura", "duda")), frozenset(("raga", "daga")),
    frozenset(("dampa", "rampa")), frozenset(("sora", "sura")),
    frozenset(("turo", "toro")), frozenset(("todo", "toro")),
    frozenset(("mural", "moral")), frozenset(("rebate", "debate")),
    frozenset(("rental", "dental"))
}

# if yung word is wala doon sa dictionary na nakita natin sa git then we will try stripping common
# filipino prefixes/suffixes. Then after that If the stripped word is in the dictionary,
# we assume it's a valid filipino word.
def is_likely_filipino_word(w, dict_words):
    if w in dict_words:
        return True
    
    # normalize multi-letter swaps first
    wn = w.replace("uw", "w").replace("iy", "y").translate(NORMALIZE_TABLE)
    if wn in dict_words:
        return True

    prefixes = ["nag", "mag", "na", "ma", "pag", "pang", "i", "ka", "pa",
                "dum", "din", "naka", "maka", "ipag", "ipinag", "ika", "kin"]
    suffixes = ["an", "in", "hin", "han", "on", "ng", "s", "ing"]
    vowels = ["a", "e", "i", "o", "u"]

    for form in (wn, w):
        for p in prefixes:
            if form.startswith(p) and form[len(p):] in dict_words: return True
        for s in suffixes:
            if form.endswith(s) and form[:-len(s)] in dict_words: return True
        for p in prefixes:
            if not form.startswith(p): continue
            rest = form[len(p):]
            for s in suffixes:
                if rest.endswith(s) and rest[:-len(s)] in dict_words: return True
            for v in vowels:
                if rest.startswith(v) and rest[1:] in dict_words: return True
                if rest.startswith(v):
                    inner = rest[1:]
                    for s in suffixes:
                        if inner.endswith(s) and inner[:-len(s)] in dict_words:
                            return True
    return False

def keep_pair(w1, w2, c1, c2, dist, dict_words=None, min_len=4, max_ratio=50,
              mid_caps=None, proper_noun_ratio=0.5):
    
    if min(len(w1), len(w2)) < min_len:
        return False

    if c1 > 0 and c2 > 0 and max(c1, c2) / min(c1, c2) > max_ratio:
        return False

    # reject manually blacklisted semantic differences
    if frozenset((w1, w2)) in NOT_VARIANTS:
        return False

    # Reject cross-language pairs (one English, one Tagalog)
    if (w1 in ENGLISH_WORDS) != (w2 in ENGLISH_WORDS):
        return False

    if mid_caps is not None:
        r1 = mid_caps.get(w1, 0) / c1 if c1 > 0 else 0
        r2 = mid_caps.get(w2, 0) / c2 if c2 > 0 else 0
        if r1 > proper_noun_ratio or r2 > proper_noun_ratio:
            return False

    if dict_words is not None:
        if not (is_likely_filipino_word(w1, dict_words) or is_likely_filipino_word(w2, dict_words)):
            return False

    return True

def hyphen_variant(w1, w2):
    # returns True if w1 and w2 differ ONLY by hyphens  
    return w1.replace("-", "") == w2.replace("-", "")
