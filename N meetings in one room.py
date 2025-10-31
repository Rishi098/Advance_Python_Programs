def max_meetings(start, end):
    c=1
    intervals = []
    for i in range(n):
        intervals.append([start[i],end[i]])
    intervals.sort(key=lambda x: x[1])
    past = intervals[0][1]

    for k in range(1,n):
        if past<intervals[k][0]:
            c+=1
            past = intervals[k][1]
    return c
