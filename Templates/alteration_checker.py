#list of tuples containing the possible letters to consider sa variants
# added separately para ito nalang palitan if we come across more swap pairs
SWAP_PAIRS = [("o", "u"), ("e", "i"), ("d", "r")] 

# valid swaps allowed in the final output
ALLOWED_SWAPS = {frozenset(pair) for pair in SWAP_PAIRS}

# parang merges the letters in a pair para maging considered as isa like o and u just become a single o
NORMALIZE_TABLE = str.maketrans({b: a for a,b in SWAP_PAIRS})

def is_valid_alteration(diff_list):
    # returns True if every difference is an allowed swap
    for diff in diff_list:
        a, b = diff.split(" vs. ")

        # reject insertions/deletions ("-")
        if a == "-" or b == "-":
            return False

        # reject unapproved swaps
        if frozenset((a, b)) not in ALLOWED_SWAPS:
            return False

    return True