def numRescueBoats(people, limit):
    
    people.sort()
    i, j = 0, len(people) - 1
    boats = 0
    
    while i <= j:
        if people[i] + people[j] <= limit:
            i += 1  
        j -= 1
        boats += 1
    
    return boats
