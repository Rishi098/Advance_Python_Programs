def countSubarraysWithSumK(arr, k):
    prefix_sum = 0
    prefix_count = {0: 1}  # To handle subarrays starting from index 0
    count = 0

    for num in arr:
        prefix_sum += num

        # Check if (prefix_sum - k) has been seen before
        count += prefix_count.get(prefix_sum - k, 0)

        # Update the prefix_count dictionary
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

    return count
