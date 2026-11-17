# valid swaps allowed in the final output
ALLOWED_SWAPS = {frozenset("ou"), frozenset("ei")}

def is_valid_alternation(diff_list):
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