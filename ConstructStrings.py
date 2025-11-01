from collections import Counter
def canConstruct(s, k):
    if len(s)<k:
        return False
    freq = Counter(s)
    odd = sum(1 for count in freq.values() if count%2==1)
    return k>=odd
