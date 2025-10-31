def remove_overlapping(intervals):
    c = 0
    intervals.sort(key=lambda x: x[1])
    curr = intervals[0][1]

    for i in range(1,len(intervals)):
        if curr>intervals[i][0]:
            c+=1
        else:
            curr = intervals[i][1]
    return c
