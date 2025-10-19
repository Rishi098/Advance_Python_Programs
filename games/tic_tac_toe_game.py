# Tic-Tac-Toe Game
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_win(board, player):
    # Check rows, columns and diagonals
    for i in range(3):
        if all([cell == player for cell in board[i]]):  # Row check
            return True
        if all([board[j][i] == player for j in range(3)]):  # Column check
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:  # Diagonal check
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:  # Reverse diagonal check
        return True
    return False

def is_full(board):
    return all(cell != " " for row in board for cell in row)

# Input and Output
def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    
    while True:
        print_board(board)
        row = int(input(f"Player {current_player}, enter row (0-2): "))
        col = int(input(f"Player {current_player}, enter column (0-2): "))
        
        if board[row][col] == " ":
            board[row][col] = current_player
        else:
            print("Cell already taken, try again!")
            continue
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        if is_full(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()
