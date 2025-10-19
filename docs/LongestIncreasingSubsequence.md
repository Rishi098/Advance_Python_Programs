# Code
```python3 []
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:

        n = len(nums)
        l=[[-1]*n for i in range(len(nums))]
        def helper(index,prev_index):
            if index==len(nums):
                return 0
            
            if l[index][prev_index] != -1:
                return l[index][prev_index]

            not_take=helper(index+1,prev_index)
            take=0

            if prev_index==-1 or nums[index]>nums[prev_index] :
                take= 1+ helper(index+1,index)
            l[index][prev_index]=max(take,not_take)
            return l[index][prev_index]
        return helper(0,-1)
        
```

