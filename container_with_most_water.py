#Find two lines that together with the x-axis form a container, such that the container contains the most water.
#Return the maximum amount of water a container can store.
#using two-pointer approach and o(n) time complexity
#o(1) space complexity


def maximumArea(height):
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        width = right - left
        curr_height = min(height[left], height[right])
        curr_area = width * curr_height
        max_water = max(max_water, curr_area)

        #Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water


def main():
    #Example input
    height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    
    result = maximumArea(height)
    print("Maximum water that can be contained:", result)


if __name__ == "__main__":
    main()
