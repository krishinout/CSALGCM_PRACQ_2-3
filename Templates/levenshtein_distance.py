def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0 for _ in range(n+1)] for _ in range(m+1)]

    # Initialize base cases
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j

    # Fill the matrix
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(
                dp[i-1][j] + 1,      # deletion
                dp[i][j-1] + 1,      # insertion
                dp[i-1][j-1] + cost  # substitution
            )

    # Print the matrix (WILL REMOVE)
    print("Levenshtein Distance Matrix:")
    print("   ", "  ".join([" "] + list(s2)))
    for i in range(m+1):
        row = [s1[i-1] if i > 0 else " "]
        for j in range(n+1):
            row.append(str(dp[i][j]))
        print("  ".join(row))

    return dp[m][n]
