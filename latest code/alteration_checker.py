# list of tuples containing the possible letters to consider sa variants
# added separately para ito nalang palitan if we come across more swap pairs
SWAP_PAIRS = [("o", "u"), ("e", "i"), ("d", "r"), ("uw", "w"), ("iy", "y"), ("c", "k")]

# valid swaps allowed in the final output
ALLOWED_SWAPS = {frozenset(pair) for pair in SWAP_PAIRS}

# only these swaps may appear MORE THAN ONCE in a pair
VOWEL_SWAPS = {frozenset(("o", "u")), frozenset(("e", "i"))}

# max number of difference segments in one pair
MAX_DIFFS = 2

# For NORMALIZE_TABLE, we ONLY use single-character swaps 
SINGLE_CHAR_PAIRS = [pair for pair in SWAP_PAIRS if len(pair[0]) == 1 and len(pair[1]) == 1]

# parang merges the letters in a pair para maging considered as isa like o and u just become a single o
# also drops hyphens so "pag-asa" and "pagasa" end up in the same bucket
NORMALIZE_TABLE = str.maketrans({**{b: a for a, b in SINGLE_CHAR_PAIRS}, ord("-"): None})

def is_valid_alteration(diff_list):
    # returns True if every difference is an allowed swap
    # AND multi-diff pairs use only vowel swaps

    # too many differences = probably not a spelling variant
    if len(diff_list) > MAX_DIFFS:
        return False

    swaps = []
    for diff in diff_list:
        a, b = diff.split(" vs. ")

        # reject insertions/deletions ("-")
        if a == "-" or b == "-":
            return False

        # reject unapproved swaps from SWAP_PAIRS
        if frozenset((a, b)) not in ALLOWED_SWAPS:
            return False

        swaps.append(frozenset((a, b)))

    # if more than 1 diff, all must be vowel swaps (o/u or e/i)
    if len(swaps) > 1 and not all(s in VOWEL_SWAPS for s in swaps):
        return False

    return True