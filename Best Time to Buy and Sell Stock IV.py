def maxProfit(k, prices):
    ans = 0
    memo = {}

    def helper(i,buy,count):
        if (i==len(prices) or count==k):
            return 0

        if ((i,buy,count) in memo):
            return memo[(i,buy,count)]

        if buy:
            ans = max(-prices[i]+helper(i+1,not buy,count),helper(i+1,buy,count))
        else:
            ans = max(helper(i+1,buy,count),prices[i] + helper(i+1,not buy,count+1))
        memo[(i,buy,count)] = ans
        return ans
    return helper(0,True,0)
return maxProfit(k,prices)
