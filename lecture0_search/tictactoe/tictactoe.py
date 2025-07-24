"""
Tic Tac Toe Player
"""

import copy
import numpy as np
from typing import Union

X = "X"
O = "O"  # noqa: E741
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Convert to numpy array
    matrix = np.array(board)

    # Count X's and O's
    x_count = (matrix == X).sum()
    o_count = (matrix == O).sum()

    # X goes first, so if counts are equal, it's X's turn
    # If X has more moves, it's O's turn
    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Convert the board to a NumPy array
    arr = np.array(board)

    # Find the row and column indices where the board is EMPTY
    none_indices = np.where(arr == EMPTY)

    # Use a set comprehension to create a set of (row, col) tuples for empty cells
    # Convert numpy integers to standard Python integers for consistency
    return {(int(row), int(col)) for row, col in zip(none_indices[0], none_indices[1])}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Unpack the single action tuple
    row, col = action

    # 1. Validate the action
    # Validate bounds
    if not (0 <= row <= 2 and 0 <= col <= 2):
        raise ValueError(f"Action {action} is out of bounds.")

    # Validate cell is empty
    if board[row][col] != EMPTY:
        raise ValueError(f"Cell {action} is already occupied.")

    # 2. Create a deep copy of the board
    new_board = copy.deepcopy(board)

    # 3. Determine whose turn it is
    current_player = player(board)  # Assuming player(board) is defined

    # 4. Apply the move to the new board
    new_board[row][col] = current_player

    # 5. Return the new board
    return new_board


def check_rows(board):
    for row in board:
        # Check if all elements in the row are the same AND not EMPTY
        if len(set(row)) == 1 and row[0] != EMPTY:
            return row[0]
    return None


def check_diagonals(board):
    # Check main diagonal
    main_diag = [board[i][i] for i in range(len(board))]
    if len(set(main_diag)) == 1 and main_diag[0] != EMPTY:
        return main_diag[0]

    # Check anti-diagonal
    anti_diag = [board[i][len(board) - i - 1] for i in range(len(board))]
    if len(set(anti_diag)) == 1 and anti_diag[0] != EMPTY:
        return anti_diag[0]

    return None


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows (and columns via transpose)
    # Convert board to numpy array for transpose to work if it's a list of lists
    np_board = np.array(board)
    for current_check_board in [np_board, np.transpose(np_board)]:
        result = check_rows(current_check_board)
        if result:
            return result

    # Check diagonals (only on the original board, as transpose doesn't simplify them)
    diag_result = check_diagonals(board)
    if diag_result:
        return diag_result

    # No winner found
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or not (actions(board)):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        winning_p = winner(board)
        if winning_p == X:
            return 1
        elif winning_p == O:
            return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    def get_value(state, is_maximizing) -> Union[float, int]:
        if terminal(state):
            return utility(state)

        if is_maximizing:
            value = float("-inf")
            for action in actions(state):
                new_state = result(state, action)
                score_if_this_action_taken = get_value(new_state, False)
                value = max(value, score_if_this_action_taken)
        else:
            value = float("inf")
            for action in actions(state):
                new_state = result(state, action)
                score_if_this_action_taken = get_value(new_state, True)
                value = min(value, score_if_this_action_taken)
        return value

    current_player = player(board)
    is_maximizing = current_player == X
    best_action = None
    best_value = float("-inf") if is_maximizing else float("inf")

    for action in actions(board):
        # 1. Simulate the action
        new_board = result(board, action)

        # 2. Get the value of the resulting board (from the *next* player's perspective)
        # If it's X's turn now, the next player is O (minimizing).
        # If it's O's turn now, the next player is X (maximizing).
        value = get_value(new_board, not is_maximizing)

        # 3. Compare this move's value to the best found so far
        if (is_maximizing and value > best_value) or (
            not is_maximizing and value < best_value
        ):
            best_value = value
            best_action = action

    return best_action
