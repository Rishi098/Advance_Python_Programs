class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        n = len(s)
        max_len = 0
        res = ""

        for i in range(n):
            for j in range(i, n):
                substring = s[i:j+1]
                if substring == substring[::-1]:
                    if len(substring) > max_len:
                        max_len = len(substring)
                        res = substring
        
        return res
