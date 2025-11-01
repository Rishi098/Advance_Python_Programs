def longestPalindromeSubseq(s):
    n = len(s)
    memo = [[-1] * n for _ in range(n)]

    def helping(i,j):
        if i>j:
            return 0
        if i==j:
            return 1

        if memo[i][j]!= -1:
            return memo[i][j]

        if s[i]==s[j]:
            memo[i][j] = 2+helping(i+1,j-1)
        else:
            memo[i][j] = max(helping(i+1,j),helping(i,j-1))
        return memo[i][j]
    return helping(0,n-1)
