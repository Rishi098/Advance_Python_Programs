def lis_including_ith_element(dp,nums,i):
    if i==0:
        return 1

    if i in dp:
        return dp[i]

    ans = 1
    
    for j in range(i):
        if (nums[j]<nums[i]):
            ans = max(ans ,1 + lis_including_ith_element(dp,nums,j))
    

    dp[i] = ans
    return dp[i]

def lengthOfLIS(nums):
    ans = 0

    dp = {}

    for i in range(len(nums)):
        ans = max(ans,lis_including_ith_element(dp,nums,i))
    
    return ans
