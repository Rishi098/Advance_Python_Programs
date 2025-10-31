def countPartitions(nums, d):
    MOD = 10**9 + 7
    total = sum(nums)

    # Check feasibility
    if (total + d) % 2 != 0:
        return 0
    target = (total + d) // 2
    if target < 0 or target > total:
        return 0

    n = len(nums)
    # dp[i][j] = number of ways to form sum j using first i elements
    dp = [[0] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = 1  # Base case: one way to make sum=0 (empty subset)

    for i in range(1, n + 1):
        for j in range(target + 1):
            # Exclude current element
            dp[i][j] = dp[i-1][j]
            # Include current element if possible
            if nums[i-1] <= j:
                dp[i][j] = (dp[i][j] + dp[i-1][j - nums[i-1]]) % MOD

    return dp[n][target] % MOD
