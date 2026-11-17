# list of letters commonly swapped in spelling variants
CHEAP_PAIRS = {frozenset("ou"), frozenset("ei")}

"""
    Adds costs for alterations/ letter swaps
    1. same letter - 0
    2. common letter swaps in filipino (cheap) - 0.5
    3. other letter swaps - 1
"""

def sub_cost(a, b):
    if a == b:
        return 0
    return 0.5 if frozenset((a, b)) in CHEAP_PAIRS else 1

    """
    If word lengths differ by more than 1, 
    words are too different comparisons are disregarded
    """
def edit_with_diff(s1, s2, max_len_diff=1):
    m, n = len(s1), len(s2)
    if abs(m - n) > max_len_diff:          # early exit
        return None

    """
    Creates the grid (row1 for word1, col1 for word2)
    """
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # code looks at three ways to get there, keeping the cheapest
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = min(
                dp[i-1][j] + 1,                                  # deletion
                dp[i][j-1] + 1,                                  # insertion
                dp[i-1][j-1] + sub_cost(s1[i-1], s2[j-1]),       # substitution
            )

    # Backtrace to recover the character differences
    # starts from bottom-right up until top-left
    diffs, i, j = [], m, n
    while i > 0 or j > 0:
        # Start at the bottom-right corner and keep going until you reach the top-left.
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + sub_cost(s1[i-1], s2[j-1]):
            if s1[i-1] != s2[j-1]:
                diffs.append(f"{s1[i-1]} vs. {s2[j-1]}")
            i, j = i - 1, j - 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            diffs.append(f"{s1[i-1]} vs. -")
            i -= 1
        else:
            diffs.append(f"- vs. {s2[j-1]}")
            j -= 1

    return dp[m][n], diffs[::-1]

#sample
print(edit_with_diff("politiko", "pulitiko"))   # (0.5, ['o vs. u'])
print(edit_with_diff("opo", "upo"))             # (0.5, ['o vs. u'])