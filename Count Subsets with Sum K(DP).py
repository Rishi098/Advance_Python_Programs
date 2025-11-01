def findWays(nums, k):
    MOD = 10**9 + 7
    dp = [0] * (k + 1)
    dp[0] = 1  

    for num in nums:
        for j in range(k, num - 1, -1): 
            dp[j] = (dp[j] + dp[j - num]) % MOD

    return dp[k]
