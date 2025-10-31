def reverse_string(s):
    stacked = []
    for i in range(len(s)-1,-1,-1):
        stacked.append(s[i])
    return "".join(stacked)
