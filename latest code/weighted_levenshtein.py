from alteration_checker import ALLOWED_SWAPS as CHEAP_PAIRS
# para sa mga letters na commonly swapped
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

def edit_with_diff(s1, s2, max_len_diff=2):
    # if word lengths differ by more than 2, comparisons are disregarded
    # (we raised it from 1 to 2 kasi uw/w and iy/y swaps add 1 to the length)
    m, n = len(s1), len(s2)
    if abs(m - n) > max_len_diff:
        return None

    # creates the grid (row1 for word1, col1 for word2)
    # initialized to infinity so the min() calls work correctly
    dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = 0
    for i in range(1, m + 1):
        dp[i][0] = i
    for j in range(1, n + 1):
        dp[0][j] = j

    # code looks at three ways to get there, keeping the cheapest
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # standard 1-to-1 substitution
            cost = sub_cost(s1[i-1], s2[j-1])
            dp[i][j] = min(
                dp[i-1][j] + 1,           # deletion
                dp[i][j-1] + 1,           # insertion
                dp[i-1][j-1] + cost       # substitution
            )

            # check 2-to-1 swap (like if s1 has "uw", s2 has "w")
            if i > 1:
                pair = (s1[i-2:i], s2[j-1])
                if frozenset(pair) in CHEAP_PAIRS:
                    dp[i][j] = min(dp[i][j], dp[i-2][j-1] + 0.5)

            # check 1-to-2 swap (baliktad lang ng example sa taas)
            if j > 1:
                pair = (s1[i-1], s2[j-2:j])
                if frozenset(pair) in CHEAP_PAIRS:
                    dp[i][j] = min(dp[i][j], dp[i-1][j-2] + 0.5)

    # backtrace to recover the character differences
    # starts from bottom-right up until top-left
    diffs, i, j = [], m, n
    while i > 0 or j > 0:
        # check for 2-to-1 swap
        if i > 1 and j > 0:
            pair = (s1[i-2:i], s2[j-1])
            if frozenset(pair) in CHEAP_PAIRS and dp[i][j] == dp[i-2][j-1] + 0.5:
                diffs.append(f"{pair[0]} vs. {pair[1]}")
                i, j = i - 2, j - 1
                continue

        # check for 1-to-2 swap
        if i > 0 and j > 1:
            pair = (s1[i-1], s2[j-2:j])
            if frozenset(pair) in CHEAP_PAIRS and dp[i][j] == dp[i-1][j-2] + 0.5:
                diffs.append(f"{pair[0]} vs. {pair[1]}")
                i, j = i - 1, j - 2
                continue

        # standard moves
        cost = sub_cost(s1[i-1], s2[j-1]) if i > 0 and j > 0 else float('inf')

        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + cost:
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