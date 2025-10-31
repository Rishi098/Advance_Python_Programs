def deleteMid(s, N):
    lst = list(s)
    mid = ((len(lst)-1)//2)
    lst.pop(mid)
    return lst
