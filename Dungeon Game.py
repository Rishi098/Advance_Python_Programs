def calculateMinimumHP(dungeon):
    n = len(dungeon)
    m = len(dungeon[0])
    memo = {}

    def min_hp(i, j):
        if i >= n or j >= m:
            return float('inf')

        if i == n - 1 and j == m - 1:
            return max(1, 1 - dungeon[i][j])


        if (i, j) in memo:
            return memo[(i, j)]
            
        right = min_hp(i, j + 1)
        down = min_hp(i + 1, j)

        need = min(right, down) - dungeon[i][j]
        memo[(i, j)] = max(1, need)

        return memo[(i, j)]

    return min_hp(0, 0)
