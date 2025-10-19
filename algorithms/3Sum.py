"""
                            3Sum Problem

Problem Statement: Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.
Notice that the solution set must not contain duplicate triplets.  

Constraints:
3 <= nums.length <= 3000
-105 <= nums[i] <= 105      

"""
"""
Explanation:
    # Step 1: Sort the array so we can use the two-pointer technique easily
    # Step 2: Loop through each number, treating it as the first element of a triplet
    # we need at least 3 numbers
    # Skip duplicate elements to avoid repeating the same triplet
    # Step 3: Use two pointers for the rest of the array
    #left = i + 1 start just after i
    #right = n - 1 start from the end
    # If the sum is too small, move left pointer to increase total
    # If the sum is too large, move right pointer to decrease total
    # If the sum is exactly zero, we found a valid triplet!
    # Skip over duplicate numbers to keep results unique
    # Move both pointers to look for new pairs
"""
def threeSum(nums):
    nums.sort()
    result = []
    n = len(nums)
    for i in range(n - 2): 
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left = i + 1         
        right = n - 1          
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1 
    return result

# 🧠 Example Input
nums = [-1, 0, 1, 2, -1, -4]
# 🖨️ Output
print(threeSum(nums)) #Output: [[-1, -1, 2], [-1, 0, 1]]


#Time Complexity: O(n²)
# Space Complexity: O(1)

"""
Example 1:
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

Example 2:
Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:
Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.
"""