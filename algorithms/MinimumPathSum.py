class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        n=len(grid)
        m=len(grid[0])
        memo={}

        def helper(i,j):
            if i+1==n and j+1==m:
                return grid[i][j]
            
            if (i,j) in memo:
                return memo[(i,j)]
            
            ch1,ch2=float("inf"),float("inf")

            if i+1<n:
                ch1=grid[i][j]+helper(i+1,j)
            if j+1<m:
                ch2=grid[i][j]+helper(i,j+1)
            
            memo[(i,j)]=min(ch1,ch2)
            return memo[(i,j)]
        return helper(0,0)
        
