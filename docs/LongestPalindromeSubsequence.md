## Intuition
Let's see how we approach it on pen and paper we can see the subsequence forming longest palindrome easily especially if the length of string is short but for longer ones we can map the first and last chracters which are equal and cancel them out and then same till we reach at the same character or 2 consecutive characters.

## Approach
We will compare the first and last characters of the string and if they are equal then we will add 2 in our answer and call the function again for string after removing first and last characters.

If the characters do not match then we will make 2 functional calls one will be assuming that we will find the matching charactr to our first character and other will be same but hoping that we will find the match for our last character.

We will call the function for remaining string after removinf first character and one after removing last character.

Lastly the base case wil be us arriving on a same place or our pointers crossing each other.

## Why do we to add first and last characters if they are equal?
Because, if we do not include them into our answer then there are 3 possibilities:

- Skip the first character and call the function for remaining
- Skip the last character and call the function for remaining
- Skip the both characters and call the function for remaining
- Our approach is better than all of these cause we are adding 2 to our answer and then calling for remaining string which is better than 3rd option.

Now, for first and second approach we have to add them in the answer but when we will add them we had alredy wasted one character, which hadn't been wasted if have added the characters into our answer the first time we found them.

### Well this is the first time I'm uploading a solution so let me know what I need to improve !!!

Here is my solution on [Leetcode](https://leetcode.com/problems/longest-palindromic-subsequence/solutions/7253688/python-solution-with-dp-by-ambuj_vashist-v65k) also look at my [GitHub](https://github.com/ambujvashistha) I have decored it!!!

## Code

``` python
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        memo={}
        def helper(start,end):
            if start>=end:
                if start==end:
                    return 1
                return 0
            
            if (start,end) in memo:
                return memo[(start,end)]
            
            if s[start]==s[end]:
                memo[(start,end)]= 2+ helper(start+1,end-1)
            else:
                memo[(start,end)]= max(helper(start+1,end),helper(start,end-1))

            return memo[(start,end)]
        return helper(0,len(s)-1)
```
