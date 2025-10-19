def solveNQueens(n):
    col = set()
    pos_diag = set()
    neg_diag = set()
    res = []
    board = [["."] * n for _ in range(n)]

    def backtrack(r):
        if r == n:
            res.append(["".join(row) for row in board])
            return
        for c in range(n):
            if c in col or (r + c) in pos_diag or (r - c) in neg_diag:
                continue
            col.add(c)
            pos_diag.add(r + c)
            neg_diag.add(r - c)
            board[r][c] = "Q"

            backtrack(r + 1)

            col.remove(c)
            pos_diag.remove(r + c)
            neg_diag.remove(r - c)
            board[r][c] = "."

    backtrack(0)
    return res

n = int(input("Enter the size of the board (n): "))
solutions = solveNQueens(n)
print(len(solutions))
for sol in solutions:
    for row in sol:
        print(row)
    print() 
