def countSubarraysWithSumK(arr, k):
    start = 0
    window_sum = 0
    count = 0
    n = len(arr)

    for end in range(n):
        window_sum += arr[end]

        # Shrink the window until sum <= k
        while window_sum > k and start <= end:
            window_sum -= arr[start]
            start += 1

        # If current window sum == k, count it
        if window_sum == k:
            count += 1

    return count
