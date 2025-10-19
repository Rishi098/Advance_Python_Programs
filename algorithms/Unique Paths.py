class Solution:
    def uniquePaths(self, m: int, n: int) -> int:

        memo={}
        def helper(r,c):
            if r==m or c==n:
                return 1
            if (r,c) in memo:
                return memo[(r,c)]
            choice=helper(r+1,c)+helper(r,c+1)
            memo[(r,c)]=choice
            return choice

        return helper(1,1)
        
