def longestValidParentheses(S):
    stack = []
    lst = list(S)
    maxxi = 0
    
    for i,char in enumerate(S):
        if char=="(":
            stack.append(i)

        else:
            if stack:
                stack.pop()
            if stack:
                maxxi = max(maxxi, i- stack[-1])
            else:
                stack.append(i)
    return maxxi
