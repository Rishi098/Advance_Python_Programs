def numRescueBoats(people, limit):
    people.sort()
    i,k=0,len(people)-1
    c =0

    while i<=k:
        if (people[i]+people[k]<=limit):
            i+=1
            k-=1
            c+=1
        else:
            k-=1
            c+=1
    return c
