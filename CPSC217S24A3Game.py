# DO NOT EDIT THE FOLLOWING LINES
# COURSE CPSC 217 July 2024
# INSTRUCTOR: Jonathan Hudson
# RNkY9dhladt8yUgc1YHi
# DO NOT EDIT THE ABOVE LINES (OR BELOW LINES UNLESS THIS IS YOUR BONUS VERSION OF FILE) (TAs will use their own version of this file for grading)

#
#  The location to insert your code is clearly marked with ###############################################################################
#

from SimpleGraphics import *
from typing import List, Tuple
from math import factorial, inf as infinity
from CPSC217S24A3Test import *
# TODO: You will have to rename this if you rename your CPSC217S24A3Board file (note you cannot use hyphens in your filename)
from CPSC217S24A3BoardFredella_Pang import *

##############################################################################
#
#  Code for drawing (IF YOU ARE READING THIS YOU BETTER NOT BE CHANGING CODE DOWN HERE)
#
##############################################################################


# TYPING ALIASES
Color = str
Board = List[List[int]]
Pixel = int
Row = int
Col = int
Piece = int
# WINDOW CONSTANTS
WIDTH = 600
HEIGHT = 600
# DRAWING CONSTANTS
X_O_PIXELS_BORDER = 15
BGD_COLOR = "white"
BOARD_COLOR = "black"
PIECE_COLOR = "black"
HINT_COLOR = "orange"
WIN_COLOR = "green"
LOSE_COLOR = "red"
TIE_COLOR = "blue"
# GAME CONSTANTS
MIN_BOARD_SIZE = 3
MAX_BOARD_SIZE = 5


def draw_x(x: Pixel, y: Pixel, size_x: Pixel, size_y: Pixel, color: Color = PIECE_COLOR) -> None:
    """
    Draw X with lines in box beginning at (x,y) with given square size and color
    Uses X_O_PIXELS_BORDER to create border to X
    :param x: The x pixel location of top left of box to draw X in
    :param y: The y pixel location of top left of box to draw X in
    :param size_x: The pixel width of the box to draw X in
    :param size_y: The pixel height of the box ot draw X in
    :param color: The color to draw the lines of the X in
    :return: None
    """
    setColor(color)
    setFill(None)
    line(x + X_O_PIXELS_BORDER, y + X_O_PIXELS_BORDER, x + size_x - X_O_PIXELS_BORDER, y + size_y - X_O_PIXELS_BORDER)
    line(x + size_x - X_O_PIXELS_BORDER, y + X_O_PIXELS_BORDER, x + X_O_PIXELS_BORDER, y + size_y - X_O_PIXELS_BORDER)


def draw_o(x: Pixel, y: Pixel, size_x: Pixel, size_y: Pixel, color: Color = PIECE_COLOR) -> None:
    """
    Draw O with lines in box beginning at (x,y) with given square size and color
    Uses X_O_PIXELS_BORDER to create border to O
    :param x: The x pixel location of top left of box to draw O in
    :param y: The y pixel location of top left of box to draw O in
    :param size_x: The pixel width of the box to draw O in
    :param size_y: The pixel height of the box ot draw O in
    :param color: The color to draw the lines of the O in
    :return: None
    """
    setColor(color)
    setFill(None)
    ellipse(x + X_O_PIXELS_BORDER, y + X_O_PIXELS_BORDER, size_x - X_O_PIXELS_BORDER * 2,
            size_y - X_O_PIXELS_BORDER * 2)


def draw_hint(board: Board, row: Pixel, col: Pixel, piece: Piece) -> None:
    """
    Draw hint information and X or O based on piece in given row, col of board
    :param board: The 2D list we will get number of rows/cols from
    :param row: The row in board to draw hint for
    :param col: The col in board to draw hint for
    :param piece: The piece to draw the hint as
    :return: None
    """
    setColor(HINT_COLOR)
    setFill(None)
    # Get size of a box
    row_pixel_size = int(HEIGHT / row_count(board))
    col_pixel_size = int(WIDTH / column_count(board))
    rect(col * col_pixel_size, row * row_pixel_size, col_pixel_size + 1, row_pixel_size + 1)
    if piece == X_PIECE:
        draw_x(col * col_pixel_size, row * row_pixel_size, col_pixel_size, row_pixel_size, HINT_COLOR)
    elif piece == O_PIECE:
        draw_o(col * col_pixel_size, row * row_pixel_size, col_pixel_size, row_pixel_size, HINT_COLOR)


def draw_board(board: Board, color: Color = BOARD_COLOR) -> None:
    """
    Draw the board in given color
    :param board: The 2D list we will get number of rows/cols from
    :param color: The color to draw the board squares in
    :return: None
    """
    # Clear board to white before redraw
    setColor(BGD_COLOR)
    setFill(BGD_COLOR)
    rect(0, 0, WIDTH, HEIGHT)
    # Get size of a box
    row_pixel_size = int(HEIGHT / row_count(board))
    col_pixel_size = int(WIDTH / column_count(board))
    # Now draw board in given colour
    setColor(color)
    setFill(None)
    # Draw horizontal lines
    for y in range(row_pixel_size, HEIGHT - 1, row_pixel_size):
        line(0, y, WIDTH, y)
    # Draw vertical lines
    for x in range(col_pixel_size, WIDTH - 1, col_pixel_size):
        line(x, 0, x, HEIGHT)
    # Draw any pieces played in board
    for row in range(row_count(board)):
        for col in range(column_count(board)):
            if board[row][col] == X_PIECE:
                draw_x(col * col_pixel_size, row * row_pixel_size, col_pixel_size, row_pixel_size, color)
            elif board[row][col] == O_PIECE:
                draw_o(col * col_pixel_size, row * row_pixel_size, col_pixel_size, row_pixel_size, color)


def setup_window() -> None:
    """
    Setup window and draw initial white line to make it resize
    :return: None
    """
    background(BGD_COLOR)
    setColor(BGD_COLOR)
    resize(WIDTH, HEIGHT)
    line(0, 0, 1, 1)


##############################################################################
#
#  Code for AI and hint for 3x3 tic-tac-toe (IF YOU ARE READING THIS YOU BETTER NO BE CHANGING CODE DOWN HERE)
#
##############################################################################


def open_moves(board: Board) -> List[Tuple[Row, Col]]:
    """
    Get all open moves in the board (i.e. BLANK spots)
    :param board: The 2D list board to get open moves from (playable spots)
    :return: A list of (row, col) move locations that are open to be played in
    """
    moves = []
    for row in range(row_count(board)):
        for col in range(column_count(board)):
            if can_play(board, row, col):
                moves.append((row, col))
    return moves


def evaluate(board: Board, player1: Piece, player2: Piece) -> int:
    """
    Evaluate the board, 1 for player 1 win, -1 for player 1 loses, 0 for neutral
    :param board: The 2D list board to evaluate
    :param player1: The piece of player 1, X/O
    :param player2: The piece of player 2, the other of X/O
    :return: The value 0 -> tied, 1 -> player 1 win, -1 -> player 1 loses
    """
    if won(board, player1):
        score = 1
    elif won(board, player2):
        score = -1
    else:
        score = 0
    return score


def minimax(board: Board, player1: Piece, player2: Piece, player: Piece, depth: int) -> List:
    """
    Minimax suggest of what row, col to play in for player1 as initial call, and player as current tree call
    :param board: 2D list which is board game is being played in
    :param player1: Player 1 piece, X/O
    :param player2: Player 2 piece, the other of X/O
    :param player: The player current playing
    :param depth: The depth of the minimax
    :return: The score of this path
    """
    # We will be either maximizing value if player1 called AI
    if player == player1:
        best = [None, None, -infinity]
    # Or minimizing if player2 did
    else:
        best = [None, None, +infinity]
    # If we run out of depth or game ends then get board state
    if depth == 0 or game_over(board):
        score = evaluate(board, player1, player2)
        return [None, None, score]
    # Get all open moves
    moves = open_moves(board)
    for move in moves:
        row, col = move[0], move[1]
        # Make play
        play(board, row, col, player)
        # Set next player to be other guy
        if player == player1:
            next_player = player2
        else:
            next_player = player1
        # Get score by exploring down tree
        score = minimax(board, player1, player2, next_player, depth - 1)
        score[0], score[1] = row, col
        # Undo the play
        play(board, row, col, EMPTY)
        # Depending on if we are currently on player1 or player 2 we update the best upwards, or downwards
        if player == player1:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score
    return best


def artificial_intelligence(board: Board, player1: Piece, player2: Piece, level: int) -> Tuple[Row, Col]:
    """
    Calling AI, if level 4 we do full recursive minimax, if not we recurse only to certain depth
    If level=0 AI we just pick random open spot
    :param board: The 2D list board in which game is being played
    :param player1: The piece of player1, X/O
    :param player2: The piece of player2, the other of X/O
    :param level: The difficultly level of AI
    :return: A (row, col) spot to play at
    """
    if player1 != X_PIECE and player1 != O_PIECE:
        raise ValueError(f"AI player1 should be X/O not {player1}")
    if player2 != X_PIECE and player2 != O_PIECE:
        raise ValueError(f"AI player2 should be X/O not {player2}")
    if player1 == X_PIECE and player2 != O_PIECE:
        raise ValueError(f"AI player1/player2 can't be X/X")
    if player1 == O_PIECE and player2 != X_PIECE:
        raise ValueError(f"AI player1/player2 can't be O/O")
    if level < 0 or level > 4:
        raise ValueError(f"AI level has to be 0 <= level <= 4")
    # Do unlimited lookahead if level >= 4
    if level >= 4:
        result = minimax(board, player1, player2, player1, row_count(board) * column_count(board) + 1)
        return result[0], result[1]
    # Otherwise multiply level by two (to get plays by each side for each level)
    elif level > 0:
        result = minimax(board, player1, player2, player1, level * 2)
        return result[0], result[1]
    # Otherwise random
    moves = open_moves(board)
    for move in moves:
        if can_play(board, move[0], move[1]):
            return move
    # There is no move to be made
    return -1, -1


##############################################################################
#
#  Main function (IF YOU ARE READING THIS YOU BETTER NOT BE CHANGING CODE DOWN HERE)
#
##############################################################################

def is_valid(value: str, start: int, end: int) -> bool:
    """
    Is this string a valid user input between start, and end integer inclusive
    :param value: The value to check
    :param start: The start integer
    :param end: The end integer inclusive
    :return: True if the value is in that range (inclusive start, end step size 1)
    """
    if value in map(str, list(range(start, end + 1))):
        return True
    return False


def get_user_rows() -> Row:
    """
    Re-prompt user until a valid row count is given
    :return: A valid int for row number
    """
    rows_s = None
    while not is_valid(rows_s, MIN_BOARD_SIZE, MAX_BOARD_SIZE):
        rows_s = input(f"Pick a board row size {list(range(MIN_BOARD_SIZE, MAX_BOARD_SIZE + 1))}: ").strip()
    return int(rows_s)


def get_user_columns() -> Col:
    """
    Re-prompt user until a valid column count is given
    :return: A valid int for column number
    """
    cols_s = None
    while not is_valid(cols_s, MIN_BOARD_SIZE, MAX_BOARD_SIZE):
        cols_s = input(f"Pick a board col size  {list(range(MIN_BOARD_SIZE, MAX_BOARD_SIZE + 1))}: ").strip()
    return int(cols_s)


DIFF_PROMPT_DEF = """Difficulties:
\t0\tAI plays randomly
\t1\tAI looks at its own and your next play
\t2\tAI looks two moves ahead for each player
\t3\tAI looks three moves ahead for each player"""
DIFF_PROMPT_3X3 = DIFF_PROMPT_DEF + """\n\t4\tAI looks ahead to end of game
\t\t(Note a difficulty of 4 uses an AI algorithm that may slow down some computers and you will have to wait."""
MIN_AI = 0
MAX_AI = 3
MAX_AI_3X3 = 4


def get_user_difficulty(row_count: Row, col_count: Col) -> int:
    """
    Get difficulty of AI for game from user
    :param row_count: The number of rows in board
    :param col_count: The number of columns in board
    :return: Integer difficulty from user
    """
    difficulty_string = None
    if row_count == col_count == 3:
        while not is_valid(difficulty_string, MIN_AI, MAX_AI_3X3):
            print(DIFF_PROMPT_3X3)
            difficulty_string = input("Pick a difficulty:").strip()
    else:
        while not is_valid(difficulty_string, MIN_AI, MAX_AI):
            print(DIFF_PROMPT_DEF)
            difficulty_string = input("Pick a difficulty:").strip()
    return int(difficulty_string)


def get_user_piece() -> Tuple[Piece, Piece]:
    """
    Get what piece the human and computer are, one is X, other is O
    :return: Either (X, O) or (O, X) for (human, computer) based on user choice
    """
    human_string = None
    while human_string != "X" and human_string != "O":
        human_string = input("Enter choice of X or O: ").strip()
    if human_string == "X":
        print("Human is X.")
        print("Computer is O.")
        return X_PIECE, O_PIECE
    else:
        print("Human is O.")
        print("Computer is X.")
        return O_PIECE, X_PIECE


def get_user_hint() -> str:
    """
    Get what type of hint to give user
    :return: "h" for winning hint, "" for no hint, "a" for hidden advanced AI hint
    """
    hint_string = input("Enter 'h' for game winning hints or <Enter> for None; ").strip()
    while hint_string != "h" and hint_string != "a" and hint_string != "":
        hint_string = input("Enter 'h' for game winning hints or <Enter> for None; ").strip()
    return hint_string


def find_and_draw_hint(board: Board, human: Piece, computer: Piece, h: str) -> None:
    """
    Based on hinting mode we will get and show hint on board for the game
    :param board: The 2D list board in which hint should be found
    :param human: The human piece
    :param computer: The computer piece
    :param h: The hint mode "h","a" or ""
    :return: None
    """
    if h == "h":
        print("Wait for hint")
        row1, col1 = hint(board, human)
        row2, col2 = hint(board, computer)
        if row1 != -1:
            print(f"Hint to win in row={row1} and col={col1}")
            draw_hint(board, row1, col1, human)
        elif row2 != -1:
            print(f"Hint to stop opponent win in row={row2} and col={col2}")
            draw_hint(board, row2, col2, human)
        else:
            print("No regular hint")
    elif h == "a":
        row1, col1 = hint(board, human)
        if row1 != -1:
            print("Wait for hint (quick)")
            row, col = row1, col1
        elif row_count == column_count == 3:
            print("Wait for hint (really slow!)")
            row, col = artificial_intelligence(board, human, computer, 4)
        else:
            print("Wait for hint (slow)")
            row, col = artificial_intelligence(board, human, computer, 3)
        if row != -1:
            print(f"Hint is row={row} and col={col}")
            draw_hint(board, row, col, human)
        else:
            print("No advanced hint")


def human_player_input(board: Board, human: Piece) -> None:
    """
    Plays the game via input() from user
    :param board: The board of game
    :param human: The human's piece
    :return: None
    """
    while True:
        row_s = None
        while not is_valid(row_s, 0, row_count(board) - 1):
            row_s = input(f"Enter row {str(list(range(0, row_count(board))))}: ").strip()
        col_s = None
        while not is_valid(col_s, 0, column_count(board) - 1):
            col_s = input(f"Enter col {str(list(range(0, column_count(board))))}: ").strip()
        row, col = int(row_s), int(col_s)
        print(row, col)
        if can_play(board, row, col):
            play(board, row, col, human)
            return
        else:
            print(f"Chosen location board row={row} col={col} is full!")


def human_player_mouse_input(board: Board, human: Piece) -> None:
    """
    Plays the game via GUI clicks from user
    :param board: The board of game
    :param human: The human's piece
    :return: None
    """
    while True:
        while not closed():
            if leftButtonPressed():
                mouse_x, mouse_y = mouseX(), mouseY()
                square_height = HEIGHT / row_count(board)
                square_width = WIDTH / column_count(board)
                row = int(mouse_y // square_height)
                col = int(mouse_x // square_width)
                if row < 0 or row > row_count(board) - 1:
                    continue
                if col < 0 or col > column_count(board) - 1:
                    continue
                if can_play(board, row, col):
                    play(board, row, col, human)
                    print(f"Human plays in row={row} and col={col}")
                    return


def test_arguments():
    failures = [["CPSC217S24A3.py"],
                ["CPSC217S24A3.py", "3"],
                ["CPSC217S24A3.py", "3", "3"],
                ["CPSC217S24A3.py", "3", "3", "0"],
                ["CPSC217S24A3.py", "4", "4", "0", "X", "anything"],
                ["CPSC217S24A3.py", "3", "3", "0", "X", "-a", "anything"],
                ["CPSC217S24A3.py", "3", "3", "0", "X", "-h", "anything"],
                ["CPSC217S24A3.py", "2", "3", "0", "X"],
                ["CPSC217S24A3.py", "6", "3", "0", "X"],
                ["CPSC217S24A3.py", "3", "2", "0", "X"],
                ["CPSC217S24A3.py", "3", "6", "0", "X"],
                ["CPSC217S24A3.py", "3", "3", "5", "X"],
                ["CPSC217S24A3.py", "4", "4", "4", "X"],
                ["CPSC217S24A3.py", "3", "3", "4", "Z"],
                ["CPSC217S24A3.py", "a", "3", "0", "X"],
                ["CPSC217S24A3.py", "3", "a", "0", "X"],
                ["CPSC217S24A3.py", "3", "3", "a", "X"]]
    print("Check those that should fail")
    for f in failures:
        if check_arguments(f):
            print(f)
            sys.exit(11)
    print("Check those that should fail DONE")
    successes = [["CPSC217S24A3.py", "3", "3", "0", "X"],
                 ["CPSC217S24A3.py", "4", "3", "0", "X"],
                 ["CPSC217S24A3.py", "3", "4", "0", "X"],
                 ["CPSC217S24A3.py", "4", "4", "0", "X"],
                 ["CPSC217S24A3.py", "3", "3", "1", "X"],
                 ["CPSC217S24A3.py", "3", "3", "2", "X"],
                 ["CPSC217S24A3.py", "3", "3", "3", "X"],
                 ["CPSC217S24A3.py", "3", "3", "4", "X"],
                 ["CPSC217S24A3.py", "3", "4", "1", "X"],
                 ["CPSC217S24A3.py", "3", "4", "2", "X"],
                 ["CPSC217S24A3.py", "3", "4", "3", "X"],
                 ["CPSC217S24A3.py", "4", "3", "1", "X"],
                 ["CPSC217S24A3.py", "4", "3", "2", "X"],
                 ["CPSC217S24A3.py", "4", "3", "3", "X"],
                 ["CPSC217S24A3.py", "4", "4", "1", "X"],
                 ["CPSC217S24A3.py", "4", "4", "2", "X"],
                 ["CPSC217S24A3.py", "4", "4", "3", "X"],
                 ["CPSC217S24A3.py", "3", "3", "0", "O"],
                 ["CPSC217S24A3.py", "3", "3", "0", "X", "-h"],
                 ["CPSC217S24A3.py", "3", "3", "0", "X", "-a"],
                 ["CPSC217S24A3.py", "3", "5", "0", "X"],
                 ["CPSC217S24A3.py", "5", "3", "0", "X"],
                 ["CPSC217S24A3.py", "4", "5", "0", "X"],
                 ["CPSC217S24A3.py", "5", "4", "0", "X"],
                 ["CPSC217S24A3.py", "5", "5", "0", "X"]]
    print("Check those that should succeed")
    for s in successes:
        if not check_arguments(s):
            print(s)
            sys.exit(1)
    print("Check those that should succeed DONE")


def check_arguments(args):
    if len(args) != 5 and len(args) != 6:
        print(f"Arguments {args}")
        print(
            "Usage: python CPSC217S24A3.py <rows> <cols> <difficulty> <piece> <optional -h hint -a advanced hint>")
        return False
    if not args[1].isdigit() or int(args[1]) not in [3, 4, 5]:
        print(f"Rows {args[1]} should be from [3,4,5]")
        return False
    if not args[2].isdigit() or int(args[2]) not in [3, 4, 5]:
        print(f"Columns {args[2]} should be from [3,4,5]")
        return False
    if int(args[1]) == int(args[2]) == 3:
        if not args[3].isdigit() or int(args[3]) not in [0, 1, 2, 3, 4]:
            print(f"Difficulty {args[3]} should be from [0=RANDOM,1=WINS,2=LOOK_AHEAD_1,3=LOOK_AHEAD_2,4=FULL_AI]")
            return False
    elif not args[3].isdigit() or int(args[3]) not in [0, 1, 2, 3]:
        print(f"Difficulty {args[3]} should be from [0=RANDOM,1=WINS,2=LOOKAHEAD1,3=LOOKAHEAD2]")
        return False
    if args[4] != "X" and args[4] != "O":
        print(f"Piece {args[4]} should be from [X,O]")
        return False
    if len(args) == 6:
        if args[5] != "-h" and args[5] != "-a":
            print(f"Hint {args[5]} should be from [-h,-a]")
            return False
    return True


def main() -> None:
    """
    Play a Tic-Tac-Toe game
    :return: None
    """
    if not run_tests():
        close()
        return
    # Check if argument parsing was designed correctly
    test_arguments()
    # If there are arguments then use those instead of prompting user for each input
    if len(sys.argv) > 1 and not check_arguments(sys.argv):
        close()
        return
    print("Setup a new game!")
    setup_window()
    # Get size of board from user
    # Create the 2D list that is the board
    if not len(sys.argv)> 1:
        board = create_board(get_user_rows(), get_user_columns())
    else:
        rows = int(sys.argv[1])
        cols = int(sys.argv[2])
        board = create_board(rows, cols)
    draw_board(board)
    # Get difficulty from the user (3x3 board allows full AI == 4)
    if not len(sys.argv)> 1:
        difficulty_input = get_user_difficulty(row_count(board), column_count(board))
    else:
        difficulty_input = int(sys.argv[3])
    # Get user choice of piece (X goes first so picking X means user goes first, picking O means computer goes first
    if not len(sys.argv)> 1:
        human, computer = get_user_piece()
    else:
        human = sys.argv[4]
        if human == "X":
            print("Human is X.")
            print("Computer is O.")
            human = X_PIECE
            computer = O_PIECE
        else:
            print("Human is O.")
            print("Computer is X.")
            human = O_PIECE
            computer = X_PIECE
    # Ask what type of hints to give player
    if not len(sys.argv)> 1:
        h = get_user_hint()
    else:
        if len(sys.argv) == 6 and sys.argv[5] == "-h":
            print("Regular hints")
            h = "h"
        elif len(sys.argv) == 6 and sys.argv[5] == "-a":
            print("Advanced hints")
            h = "a"
        else:
            print("No hints")
            h = ""
    # Now we can start the game?
    player = X_PIECE
    plays = 0
    print("Play a game!")
    gui_flag = False
    if len(sys.argv):
        from tkinter import messagebox
        msg_box = tk.messagebox.askquestion('Input', 'Mouse Input?', icon='warning')
        if msg_box == 'yes':
            gui_flag = True
    else:
        if input("Enter G to enter input with mouse, otherwise use shell") == "G":
            gui_flag = True
    while not game_over(board):
        value = (row_count(board) * column_count(board)) - plays
        if value > 0:
            complexity = factorial(value)
            print(f"Estimated complexity of current game: {complexity}")
        if human == player:
            print("Human player's turn.")
            # Get and draw hint
            find_and_draw_hint(board, human, computer, h)
            # Depending on flag get input for user playing via GUI or via input() prompts in shell
            if gui_flag:
                human_player_mouse_input(board, human)
            else:
                human_player_input(board, human)
            # Switch to other player
            player = computer
        else:
            row, col = artificial_intelligence(board, computer, human, difficulty_input)
            play(board, row, col, computer)
            print(f"AI plays in row={row} and col={col}")
            player = human
        draw_board(board)
        plays += 1
    game_over_draw(board, human)
    hande_exit()


def game_over_draw(board: Board, human: Piece) -> None:
    """
    This will draw colors when the game ends for the game-over state
    :param board: The 2D list board to draw for
    :param human: The human piece
    :return: None
    """
    setFont("Times", "50", "bold")
    if won(board, X_PIECE):
        if human == X_PIECE:
            draw_board(board, WIN_COLOR)
        else:
            draw_board(board, LOSE_COLOR)
        setColor("black")
        text(WIDTH / 2, HEIGHT / 2, "X won!")
    elif won(board, O_PIECE):
        if human == O_PIECE:
            draw_board(board, WIN_COLOR)
        else:
            draw_board(board, LOSE_COLOR)
        setColor("black")
        text(WIDTH / 2, HEIGHT / 2, "O won!")
    else:
        draw_board(board, TIE_COLOR)
        setColor("black")
        text(WIDTH / 2, HEIGHT / 2, "Board full. Draw.")


def hande_exit() -> None:
    """
    Will close the draw window when clicked on as game ends
    :return: None
    """
    # Sleep to let last play clicks stop
    sleep(1)
    # Then while still alive wait until clicked on
    while not closed():
        if leftButtonPressed():
            close()


# We will run main() in such a way that an exception will make us cleanup and close the window (but we will make sure to print the stack trace regardless
try:
    main()
except Exception as main_ex:
    sys.stderr.write(str(main_ex) + "\n")
    traceback.print_exc(file=sys.stderr)
    close()
    sys.exit(2)
