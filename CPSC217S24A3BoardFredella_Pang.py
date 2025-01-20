
# DO NOT EDIT THE FOLLOWING LINES
# COURSE CPSC 217 July 2024
# INSTRUCTOR: Jonathan Hudson
# RNkY9dhladt8yUgc1YHi
# DO NOT EDIT THE ABOVE LINES

# TODO: INFORMATION FOR YOUR TA
# Name: Fredella Pang
# UCID: 30247875
# Description: A library that supports a tic-tac-toe game with three or more rows and columns to be created and played.
# This library creates a board (2D list), checks if positions are empty, plays players pieces,
# determines whether a game has been finished (win/full) if it has three pieces of one type in any direction,
# and supports a hint feature.

# Constants for the game pieces
EMPTY = 0
X_PIECE = 1
O_PIECE = 2


def create_board(rows=3, columns=3):
    """
    Creates a two-dimensional list, to be used as a tic-tac-toe board.
    :param rows: (default is 3) Board contains rows(#) of internal lists.
    :param columns: (default is 3) Each internal list contains columns (#) of EMPTY constants.
    :return:  completed empty board (2D list)
    """
    list_board = []
    for i in range(rows):  # for every row
        list_row = [EMPTY] * columns  # create a list that has an EMPTY constant for each column
        list_board.append(list_row)  # add this list into the board
    return list_board


def row_count(board):
    """
    Counts the number of rows in a board.
    :param board: The board (2D list) to check
    :return: number of rows (integer)
    """
    return len(board)


def column_count(board):
    """
    Counts the number of columns in a board.
    :param board: The board (2D list) to check
    :return: number of columns (integer)
    """
    return len(board[0])


def can_play(board, row, column):
    """
    Determines whether a player can play a given position based on its row and column.
    :param board:The board to check
    :param row: The row of the position to check
    :param column: The column of the position to check
    :return: True if the position contains an EMPTY constant, False otherwise
    """
    is_empty = board[row][column] == EMPTY
    return is_empty


def play(board, row, column,piece):
    """
    Plays a given piece in a row and column.
    :param board:The board that is being played
    :param row: The row of the position to change/set
    :param column: The row of the position to change/set
    :param piece: The piece that is being played (human/computer)
    :return: None
    """
    board[row][column] = piece


def full(board):
    """
    Determines whether a board is full/has no empty locations remaining.
    :param board:The board to check
    :return: True if board has no EMPTY constants, False otherwise
    """
    for r in range(row_count(board)):  # for every row
        for c in range(column_count(board)):  # for every column
            if board[r][c] == EMPTY:  # check every position to find an EMPTY constant --> if there is an empty position
                return False  # return not full
    return True  # no EMPTY constants mean the board is full


def win_in_row(board, row, piece):
    """
    Determines whether a player wins in a given row and piece by having three pieces in a row.
    :param board:The board to check
    :param row: The row of the position to check
    :param piece: The piece that is being played (human/computer)
    :return: True if the player wins in the given row (three in a row consecutively), False otherwise
    """
    count = 0
    for c in range(column_count(board)):
        if board[row][c] == piece:  # if a piece is found, start checking
            count += 1
            if count == 3:  # if three consecutive pieces
                return True  # return win
        else:
            count = 0  # resets count when a piece is not found in consecutive order
    return False


def win_in_column(board, column, piece):
    """
    Determines whether a player wins in a given column and piece.
    :param board:The board to check
    :param column: The column of the position to check
    :param piece: The piece that is being played (human/computer)
    :return: True if the player wins in the given column (three in a column consecutively), False otherwise
    """
    count = 0
    for r in range(row_count(board)):
        if board[r][column] == piece:  # if a piece is found, start checking
            count += 1
            if count == 3:  # if three consecutive pieces
                return True  # return win
        else:
            count = 0  # resets count when a piece is not found in consecutive order
    return False


def win_in_diagonal_backslash(board, piece):
    """
    Determines whether a player wins in a diagonal backslash.
    i.e. [0,0], [1,1], [2,2] or [0,1], [1,2], [2,3] or [1,0], [2,1], [3,2] or ...
    :param board:The board to check
    :param piece: The piece that is being played (human/computer)
    :return: True if the player wins in the diagonal backslash (three consecutively), False otherwise
    """
    count = 0
    for r in range(row_count(board) - 2):  # check all rows except for the last two
        for c in range(column_count(board) - 2):  # check all columns except for the last two
            if board[r][c] == piece:  # if a piece is found, start checking
                for three in range(3):
                    if board[r+three][c+three] == piece:  # [r+three] progresses downwards, [c+three] progresses right
                        count += 1
                        if count == 3:  # if three consecutive pieces
                            return True  # return win
                    else:
                        count = 0
            count = 0  # reset count before next starting position is checked (so the count does not carry over)
    return False


def win_in_diagonal_forward_slash(board, piece):
    """
    Determines whether a player wins in a diagonal forward slash.
    :param board: The board to check
    :param piece: The piece that is being played (human/computer)
    :return: True if the player wins in a diagonal forward slash (three consecutively), False otherwise
    """
    count = 0
    for r in range(row_count(board)-2):  # check all rows except for the last two
        for c in range(2,column_count(board)):  # check all columns starting at the 3rd column
            if board[r][c] == piece:  # if a piece is found, start checking
                for three in range(3):
                    if board[r + three][c-three] == piece:  # [r+three] progresses downwards, [c-three] progresses left
                        count += 1
                        if count == 3:  # if three consecutive pieces
                            return True  # return win
                    else:
                        count = 0  # reset count
            count = 0  # reset count before next starting position is checked (so the count does not carry over)
    return False


def won(board, piece):

    """
    Determines whether a player won in a given piece.
    :param board: The board to check
    :param piece: The piece that is being played (human/computer)
    :return: True if the player won in a given piece by having three consecutive pieces in any direction, False otherwise
    """
    win = False
    # Check all rows for win:
    for r in range(row_count(board)):
        if win_in_row(board, r, piece):
            return True
    # Check all columns for win:
    for c in range(column_count(board)):
        if win_in_column(board, c, piece):
            return True
    # Check all diagonals for win
    if win_in_diagonal_backslash(board, piece) or win_in_diagonal_forward_slash(board, piece):
        return True
    return False


def hint(board, piece):
    """
    Algorithm temporarily plays player's piece type until it wins.
    If it cannot win, it will default to suggesting (-1,-1)
    :param board: The board that is being played
    :param piece: The piece that is being played
    :return: a row and column hint
    """
    for r in range(row_count(board)):  # for every row
        for c in range(column_count(board)):  # for every column
            if can_play(board, r, c):  # if this position is empty
                play(board, r, c, piece)  # play the player's piece in this position
                if won(board, piece):  # if this results in winning scenario
                    board[r][c] = EMPTY  # remove this piece
                    return r, c  # return position
                else:  # does not result in winning scenario
                    board[r][c] = EMPTY  # remove piece (proceed) to next column/row
    return -1, -1  # default hint if winning scenario/hint is not found


##############################################################################
#
# Code below is for testing student functions (IF YOU ARE READING THIS YOU BETTER NO_ BE CHANGING CODE DOWN HERE)
#                                                                     not even here ^ :(
##############################################################################
def game_over(board):
    """
    This function determines if the game is complete due to a win or tie by either player
    :param board: The 2D list board to check
    :return: True if game is complete, False otherwise
    """
    if full(board) or won(board, X_PIECE) or won(board, O_PIECE):
        return True
    return False


if __name__ == '__main__':
    print("File is being run directly so ask about running the tests.")
    if input("Enter Y to run tests:") == "Y":
        from CPSC217S24A3Test import *

        run_tests()
