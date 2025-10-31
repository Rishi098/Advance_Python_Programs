def remove_overlapping(intervals):
    # Step 1: Sort by end time
    intervals.sort(key=lambda x: x[1])

    remove_count = 0
    end = float('-inf')

    # Step 2: Greedy selection
    for start, finish in intervals:
        if start >= end:
            end = finish   # keep this interval
        else:
            remove_count += 1  # overlapping, remove this one

    return remove_count
