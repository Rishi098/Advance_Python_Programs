def coinChange(amount):
    l=[1, 2, 5, 10, 20, 50, 100, 200, 500, 2000]
    tc=0
    j=len(l)-1
    while amount>0:
        tc+=amount//l[j]
        amount=amount%l[j]
        j-=1
    return tc
