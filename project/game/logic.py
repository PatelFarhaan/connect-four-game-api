# <==================================================================================================>
#                                          STATIC VARAIABLES
# <==================================================================================================>
ROW_COUNT = 4
COLUMN_COUNT = 4


#<==================================================================================================>
#                                          GET BOARD
#<==================================================================================================>
def get_board(row, col):
    board = [[0 for j in range(col)] for i in range(row)]
    return board


#<==================================================================================================>
#                                          IS BOARD VALID
#<==================================================================================================>
def is_valid(board, col):
    return board[3][col] == 0


#<==================================================================================================>
#                                    GET CURRENT NULL LOCATION
#<==================================================================================================>
def get_current_null_position(board, col):
    for row in range(len(board)):
        if board[row][col] == 0:
            return row

#<==================================================================================================>
#                                          SET VALUES
#<==================================================================================================>
def set_value(board, row, col, player_id):
    board[row][col] = player_id
    return board


#<==================================================================================================>
#                                       CHECK WIN CONDITION
#<==================================================================================================>
def winning_move(board, piece):
    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Horizontal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True
