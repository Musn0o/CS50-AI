### Tic-Tac-Toe: `player(board)` Function Notes

The `player(board)` function determines whose turn it is (`X` or `O`) to make the next move on the given `board` state.

**Core Logic:**

Tic-Tac-Toe rules dictate that `X` always makes the first move. Subsequent turns alternate between `X` and `O`. Therefore, we can determine the current player by comparing the number of `X`'s and `O`'s already present on the board:

1. **Count Markers:** Count the total number of `X`'s and `O`'s on the board.
    
    - **Implementation Note:** We use `numpy` for an efficient way to count these. The board (a list of lists) is first converted into a NumPy array. Then, boolean indexing (`matrix == "X"`) creates a boolean array, and `.sum()` on this array effectively counts the `True` values (i.e., the occurrences of "X").
        
2. **Determine Turn:**
    
    - If the count of `X`'s is equal to the count of `O`'s, it means `X` has either not made a move yet (empty board) or has just finished their previous turn, leaving an equal number of markers. In either case, it is `X`'s turn.
        
    - If the count of `X`'s is greater than the count of `O`'s, it indicates that `X` has already made one more move than `O`. Therefore, it is `O`'s turn to play.
        

**Code Snippet (Conceptual):**

```python
def player(board):
	"""
	Returns player who has the next turn on a board.
	"""
	# Convert board to a NumPy array for easier counting
	matrix = np.array(board)
	
	# Count 'X' and 'O' markers on the board
	x_count = (matrix == X).sum()
	o_count = (matrix == O).sum()
	
	# X goes first, so if counts are equal, it's X's turn
	# If X has more moves, it's O's turn
	if x_count == o_count:
		return X
	else:
		return O
```

---
### Tic-Tac-Toe: `actions(board)` Function Notes

The `actions(board)` function identifies all the possible moves that can be made on the current `board` state. In Tic-Tac-Toe, a valid "action" means placing a marker (`X` or `O`) into an empty cell.

**Core Logic:**

The function's goal is to return a `set` of `(row, column)` tuples, where each tuple represents the coordinates of an empty cell on the board.

1. **Identify Empty Cells:**
    
    - We convert the input `board` (a list of lists) into a NumPy array. This allows us to efficiently use NumPy's array operations.
        
    - `np.where(arr == EMPTY)`: This powerful NumPy function is used to locate all elements in the array that match our `EMPTY` constant (representing an unoccupied cell). It returns a tuple of arrays, with the first array containing all row indices and the second containing all column indices of the empty cells.
        
2. **Format as Tuples:**
    
    - We then use a **set comprehension** to iterate through the paired row and column indices obtained from `np.where`.
        
    - `zip(none_indices[0], none_indices[1])`: This combines the separate row and column index arrays into pairs.
        
    - `(int(row), int(col))`: Each pair is then cast to integers and formed into a `(row, column)` tuple.
        
    - `return { ... }`: The set comprehension collects all these unique tuples into a `set`, which is the standard return type for possible actions in this project. Using a `set` inherently handles uniqueness if by some strange means `np.where` produced duplicates (though it typically wouldn't in this context).
        

**Advantages of this Approach:**

- **Conciseness:** Replaces potentially verbose nested loops with a single line leveraging NumPy.
    
- **Efficiency:** NumPy operations are highly optimized, making this approach generally faster for larger boards (though less critical for a 3x3 Tic-Tac-Toe board).
    
- **Readability:** Once familiar with NumPy, `np.where` clearly communicates the intent of finding specific element locations.
    

**Code Snippet (Conceptual):**

```python
import numpy as np

def actions(board):
    # Convert the board to a NumPy array
    arr = np.array(board)

    # Find the row and column indices where the board is EMPTY
    none_indices = np.where(arr == EMPTY)

    # Use a set comprehension to create a set of (row, col) tuples for empty cells
    # Convert numpy integers to standard Python integers for consistency
    return {(int(row), int(col)) for row, col in zip(none_indices[0], none_indices[1])}
```

---
### Tic-Tac-Toe: `result(board, action)` Function Notes

The `result(board, action)` function simulates a player making a move on the Tic-Tac-Toe board. It's crucial for the AI's ability to "think ahead" by exploring hypothetical game states.

**Core Requirements:**

1. **Immutability:** The most critical requirement is that this function **must not modify the original `board`**. Instead, it should return a _brand new board_ representing the state after the `action`. This is fundamental for algorithms like Minimax, which need to explore many different paths without changing the base state.
    
2. **Validity Check:** It must first validate the `action` (the proposed move). If the `action` is invalid, the function should raise an `Exception` (e.g., `ValueError`).
    
3. **Apply Move:** If the `action` is valid, it applies the move to the new board.
    
---
#### Detailed Breakdown of Steps:

**1. Unpack and Validate the `action`:**

- **Understanding `action`:** The `action` parameter represents a single move and will be a **tuple** like `(row, col)`, for example, `(0, 1)` for the top-middle cell. It is _not_ a list of moves.
    
- **Unpacking:** To access the row and column values from the `action` tuple, use **tuple unpacking**:
    
```Python
    row, col = action
    ```

- **Common Pitfall to AVOID:** Do **NOT** use `zip(*action)` here. `zip(*iterable)` is for "unzipping" a list of tuples (e.g., `[(1, 'a'), (2, 'b')]` into `(1, 2)` and `('a', 'b')`). When given a single tuple like `(0, 1)`, `zip(0, 1)` will result in an error because integers are not iterable.
    
- **Validation Checks:** Before proceeding, verify that the `action` is legitimate:
    - **Bounds Check:** Ensure that `row` and `col` are within the valid range for a 3x3 board (0, 1, or 2).
    ```python
if not (0 <= row <= 2 and 0 <= col <= 2):
    raise ValueError(f"Action {action} is out of bounds.")
```
- **Occupancy Check:** Ensure that the cell at `board[row][col]` is currently `EMPTY`. If it's already occupied by 'X' or 'O', the move is invalid.
```python
if board[row][col] != EMPTY:
    raise ValueError(f"Cell {action} is already occupied.")
```
- _Why Validate?_ This prevents errors later in the code and ensures that only legal moves are ever attempted.

**2. Create a Deep Copy of the `board`:**

- **Why a Copy?** As mentioned, the original `board` must remain unchanged. This function's purpose is to _predict_ the next state, not alter the current one.
    
- **Why a _Deep_ Copy?** Your `board` is a "list of lists" (a 2D list).
    
    - A **shallow copy** (like `new_board = list(board)` or `new_board = board[:]`) would create a new outer list, but the inner lists (the rows themselves) would _still refer to the same row objects_ as the original board. If you modify an element in `new_board[r][c]`, it would also change `board[r][c]`. This is BAD for Minimax.
        
    - A **deep copy** creates completely new, independent copies of all nested structures. This means changes to `new_board` will _never_ affect `board`.
        
- **How to Deep Copy:** Use the `copy` module's `deepcopy` function.
```python
import copy # Make sure this is at the top of your file!
new_board = copy.deepcopy(board)
```

- _Self-Correction Note:_ My previous solution used `[row[:] for row in board]`. While this works for a simple list of lists containing _immutable_ elements (like strings and `None`), `copy.deepcopy()` is the universal and safest method for truly independent copies of any nested Python data structure. Get into the habit of using `deepcopy` for nested mutable objects.

**3. Determine the `current_player`:**

- You already have a function for this! Call your `player(board)` function to find out whose turn it is to place a mark.
```python
current_player = player(board) # This calls the player function you just wrote!
```

**4. Apply the Move to the `new_board`:**

- Using the `row` and `col` obtained from unpacking the `action`, and the `current_player`, update the specific cell on the `new_board`.

```python
new_board[row][col] = current_player
```

**5. Return the `new_board`:**

- Finally, return the modified deep copy.
```python
return new_board
```

--- 

**Code Snippet (Conceptual):**

```python
import copy
# Assuming player(board) and EMPTY are defined elsewhere

def result(board, action):
    # Unpack the action tuple into row and column
    row, col = action

    # 1. Validate the action
    # Check if the move is within the board's bounds (0-2 for both row and col)
    if not (0 <= row <= 2 and 0 <= col <= 2):
        raise ValueError(f"Action {action} is out of bounds (rows/cols must be 0, 1, or 2).")

    # Check if the chosen cell is currently empty
    if board[row][col] != EMPTY:
        raise ValueError(f"Cell {action} is already occupied. Choose an empty cell.")

    # 2. Create a deep copy of the original board
    # This is critical to ensure the original board is NOT modified
    new_board = copy.deepcopy(board)

    # 3. Determine whose turn it is to place a mark
    current_player = player(board)

    # 4. Apply the move to the new board
    new_board[row][col] = current_player

    # 5. Return the new, modified board state
    return new_board
```

---
### Tic-Tac-Toe: `winner(board)` Function Notes

The `winner(board)` function determines if there is a winner in the current `board` state. If 'X' has won, it returns 'X'. If 'O' has won, it returns 'O'. If no winner is found (game is a tie or still in progress), it returns `None`.

**Core Logic:**

A player wins by getting three of their markers in a row, column, or diagonal. The function systematically checks all these possibilities for both 'X' and 'O'.

---

#### Detailed Breakdown of Steps and Techniques:

The solution leverages helper functions and NumPy's `transpose` for efficiency and conciseness.

**1. Helper Function: `check_rows(board_segment)`**

- **Purpose:** This helper function checks if any single row within a given `board_segment` (which could be the actual board, or a transposed version of it) constitutes a win.
    
- **Mechanism (`len(set(row)) == 1`):**
    
    - It iterates through each `row` in the `board_segment`.
        
    - `set(row)`: Converts the current row into a Python `set`. A set only stores unique elements.
        
    - If `len(set(row)) == 1`, it means all elements in that `row` are identical. For example, `set(['X', 'X', 'X'])` becomes `{'X'}` (length 1).
        
- **Crucial `EMPTY` Handling:**
    
    - **Common Pitfall:** If a row is entirely `[EMPTY, EMPTY, EMPTY]`, `set([EMPTY, EMPTY, EMPTY])` would result in `{EMPTY}`, which also has a length of 1. This would incorrectly declare `EMPTY` as a winner.
        
    - **Correction:** We must add an explicit check: `and row[0] != EMPTY`. This ensures that the identical elements are indeed 'X' or 'O', not just empty spaces.
        
- **Return Value:** If a winning row is found (e.g., all 'X's or all 'O's), it returns `row[0]` (which will be 'X' or 'O'). Otherwise, it returns `None`.
    

**2. Helper Function: `check_diagonals(board)`**

- **Purpose:** This helper explicitly checks the two diagonal lines for a win. `numpy.transpose` cannot directly simplify diagonal checks in the same way it does for rows/columns.
    
- **Main Diagonal (Top-Left to Bottom-Right):**
    
    - It constructs a list of elements from `board[i][i]` for `i` from 0 to `len(board)-1`.
        
    - It then applies the same `len(set(diagonal_list)) == 1 and diagonal_list[0] != EMPTY` logic to check for a win.
        
- **Anti-Diagonal (Top-Right to Bottom-Left):**
    
    - It constructs a list of elements from `board[i][len(board) - i - 1]` for `i` from 0 to `len(board)-1`. `len(board) - i - 1` correctly calculates the column index for the anti-diagonal.
        
    - Again, it applies the `len(set(anti_diagonal_list)) == 1 and anti_diagonal_list[0] != EMPTY` logic.
        
- **Return Value:** If either diagonal forms a win, it returns the winning player. Otherwise, it returns `None`.
    

**3. Main `winner(board)` Function Logic:**

- **Initial Setup:**
    
    - It first converts the `board` into a NumPy array (`np_board = np.array(board)`). This is necessary because `numpy.transpose` operates on NumPy arrays, not standard Python lists of lists.
        
- **Checking Rows and Columns Efficiently:**
    
    - It iterates through two versions of the board: `[np_board, np.transpose(np_board)]`.
        
    - **First Iteration (`np_board`):** When `check_rows` is called on the original `np_board`, it identifies any horizontal (row) wins.
        
    - **Second Iteration (`np.transpose(np_board)`):** `np.transpose(np_board)` swaps rows and columns. When `check_rows` is called on this transposed board, it effectively checks for **vertical (column) wins** on the _original_ board. This clever use of transpose eliminates the need for a separate function to check columns.
        
    - `if result:`: If `check_rows` returns 'X' or 'O', it means a horizontal or vertical winner has been found, and that player is immediately returned.
        
- **Checking Diagonals:**
    
    - If no horizontal or vertical winner is found after the loop, the function then calls `check_diagonals(board)` (passing the original board, not the transposed one).
        
    - `if diag_result:`: If a winner is found diagonally, that player is returned.
        
- **No Winner:**
    
    - If, after checking all rows, columns, and diagonals, no winner has been determined, the function returns `None`. This indicates either a tie or a game still in progress (which the `terminal` function will later distinguish).

**Code Snippet (Conceptual):**

```python
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
```

---
### Tic-Tac-Toe: `terminal(board)` Function Notes

The `terminal(board)` function determines if the game is over in the current `board` state. A game is considered over if either a player has won or if the board is completely full (resulting in a tie).

**Core Logic:**

The function returns `True` if the game has concluded and `False` if the game is still in progress.

**Implementation Details:**

```python
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # The game is over if:
    # 1.There is a winner (as determined by the winner(board) function)
    # OR
    # 2.There are no more possible moves left (meaning the board is full,
    #    and if no winner was found, it's a tie).
    if winner(board) or not (actions(board)):
        return True
    return False
```

**Explanation:**

- **`winner(board)`:** This part of the condition checks if the `winner` function returns 'X' or 'O'. In Python, non-empty strings are considered "truthy". If `winner(board)` returns a player, the first part of the `or` condition is `True`, and the function immediately returns `True`, indicating the game is over.
    
- **`not (actions(board))`:** This part handles the tie condition.
    
    - Your `actions(board)` function returns a `set` of all possible valid moves (empty cells).
        
    - If the board is completely full, there are no empty cells, and `actions(board)` will return an **empty set (`{}`)**.
        
    - In Python, an empty set is considered "falsy". Therefore, `not (actions(board))` will evaluate to `True` when the board is full.
        
    - If `winner(board)` was `None` (no winner) AND `actions(board)` returns an empty set (board is full), then `False or True` evaluates to `True`, and the function returns `True`, correctly indicating a tie.
        
- **`return False`:** If neither a winner is found nor the board is full (meaning `winner(board)` is `None` AND `actions(board)` is a non-empty set), the game is still in progress, and the function returns `False`.
    

This solution is concise, efficient, and correctly handles both winning and tie conditions by leveraging the truthiness of Python objects.

---

### Tic-Tac-Toe: `utility(board)` Function Notes

The `utility(board)` function assigns a numerical value to a **terminal** game state. This value represents the "score" of that state from the perspective of the maximizing player (typically 'X').

**Core Requirements:**

- Returns `1` if 'X' has won the game.
    
- Returns `-1` if 'O' has won the game.
    
- Returns `0` if the game is a tie.
    

**Important Note:** The `utility` function is designed to be called **only on terminal states**. In the Minimax algorithm, this function provides the base values for the recursive evaluation.

**Implementation Details:**

```python
# Assuming X, O, winner(board), and terminal(board) are defined elsewhere

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # First, confirm that the board is indeed a terminal state.
    # This is a good defensive check, though Minimax typically calls utility
    # only after terminal(board) has been confirmed True.
    if terminal(board):
        # Determine who, if anyone, won the game.
        # winner(board) will return X, O, or None (for a tie).
        winning_p = winner(board)

        # Assign utility value based on the winner
        if winning_p == X:
            return 1  # X wins, favorable outcome for X
        elif winning_p == O:
            return -1 # O wins, unfavorable outcome for X

	# If terminal is True but winner(board) is None, it's a tie.
	return 0  # Tie, neutral outcome
```

**Explanation and Why it's Simple Now:**

The simplicity of this `utility` function is a direct result of the robust and correct implementation of the preceding functions:

1. **`terminal(board)`:** This function accurately identifies if the game is over (either by a win or a tie). By wrapping the core logic within `if terminal(board):`, we ensure that `utility` only attempts to assign a score to a game that has actually ended.
    
2. **`winner(board)`:** This function precisely identifies the winning player ('X' or 'O') or returns `None` if there is no winner.
    

By leveraging these pre-existing, well-defined functions, `utility` becomes a straightforward mapping:

- If `winner(board)` returns `X`, the utility is `1`.
    
- If `winner(board)` returns `O`, the utility is `-1`.
    
- If `winner(board)` returns `None` (meaning `terminal(board)` was `True` due to a full board, but no one won), the utility is `0`.
    

This modular approach makes the code clean, readable, and easy to debug. The "difficulty" of `utility` often comes from trying to embed the win/tie logic directly within it, which is now handled by its dependencies.


---

### Tic-Tac-Toe: `minimax(board)` Function Notes

The `minimax(board)` function is the "brain" of your AI. Its job is to figure out the **absolute best move** the current player can make on the `board` to achieve the best possible outcome, assuming the opponent also plays perfectly. It returns the `(row, col)` tuple representing this optimal `action`.

**The Big Idea Behind Minimax:**

Minimax is a **recursive decision-making algorithm** for two-player games. It works by looking ahead at _all possible future moves_ and their outcomes, building a "game tree" in its mind (or memory!).

- **Maximizing Player (e.g., 'X'):** Wants to choose the move that leads to the _highest possible score_ for themselves.
    
- **Minimizing Player (e.g., 'O'):** Wants to choose the move that leads to the _lowest possible score_ for the maximizing player (which is effectively minimizing 'X's gain, or maximizing 'O's gain).
    

It's called "Minimax" because the maximizing player wants to maximize the score, but they assume the opponent will play optimally to _minimize_ that score.

---

#### Detailed Breakdown of `minimax` Function:

`minimax` function has two main parts: an inner helper function (`get_value`) that does the recursive score calculation, and the outer part that uses `get_value` to pick the best _action_.

**Part 1: The Recursive Helper Function `get_value(state, is_maximizing)`**

This function's sole purpose is to calculate the **numerical value** of a given `state` (board configuration). It's the core of the recursion.

- **`state`**: The current board you're evaluating.
    
- **`is_maximizing`**: A boolean (`True` if it's currently the maximizing player's turn in this recursive call, `False` if it's the minimizing player's turn).
    

1. **Base Case (Stopping the Recursion):**
	```python
if terminal(state):
	return utility(state)
```
	
	- **Meaning:** If the `state` is a game-over situation (a win or a tie), the recursion stops. We don't need to look any further.
        
    - **Action:** We simply return the final score of that `state` using your `utility(state)` function (which returns `1`, `-1`, or `0`).
        
2. **Recursive Step (Exploring Future Moves):**
    
    - **If `is_maximizing` (Current Player is 'X'):**
    
    ```python
value = float("-inf") # Initialize with the worst possible score for X
for action in actions(state):
    # Simulate the next move by X, creating a new_state
    new_state = result(state, action)
    # Recursively get the value of this new_state.
    # IMPORTANT: It's now O's turn (minimizing player), so we call with is_maximizing=False
    score_if_this_action_taken = get_value(new_state, False)
    # X wants to find the HIGHEST score from all possible next moves
    value = max(value, score_if_this_action_taken)
return value
```
	
	- **`value = float("-inf")`:** We start with negative infinity because 'X' wants to find the _highest_ value, so any real game score will be better than this initial worst-case.
        
    - **`for action in actions(state):`:** 'X' considers every possible legal move they can make from this `state`.
        
    - **`get_value(result(state, action), False)`:** This is the recursive call. After 'X' makes a move (`result`), it's 'O's turn. So, we ask `get_value` what the score will be if 'O' plays perfectly (meaning `is_maximizing` is `False`).
        
    - **`value = max(value, ...)`:** 'X' will choose the action that leads to the best possible future score. So, `value` is updated to be the maximum score found so far among all immediate moves.
        
- **If `not is_maximizing` (Current Player is 'O'):**

```python
value = float("inf") # Initialize with the best possible score for X (worst for O)
for action in actions(state):
    # Simulate the next move by O, creating a new_state
    new_state = result(state, action)
    # Recursively get the value of this new_state.
    # IMPORTANT: It's now X's turn (maximizing player), so we call with is_maximizing=True
    score_if_this_action_taken = get_value(new_state, True)
    # O wants to find the LOWEST score from all possible next moves (to minimize X's gain)
    value = min(value, score_if_this_action_taken)
return value
```

- **`value = float("inf")`:** We start with positive infinity because 'O' wants to minimize the opponent's score. Any real game score will be worse (lower) than this initial best-case for X.
    
- **`for action in actions(state):`:** 'O' considers every possible legal move they can make.
    
- **`get_value(result(state, action), True)`:** After 'O' makes a move (`result`), it's 'X's turn. So, we ask `get_value` what the score will be if 'X' plays perfectly (meaning `is_maximizing` is `True`).
    
- **`value = min(value, ...)`:** 'O' will choose the action that leads to the worst possible future score for 'X'. So, `value` is updated to be the minimum score found so far.

---

**Part 2: The Main `minimax(board)` Function (Finding the Optimal _Action_)**

This is the entry point. It calls `get_value` to figure out the scores, but its job is to return the specific `action` (e.g., `(0, 0)`) that leads to that optimal score.

1. **Identify Current Player:**
```python
current_player = player(board)
is_maximizing = current_player == X # True if X, False if O
```

-  This tells you whether you're trying to maximize or minimize.
        
2. **Initialize `best_action` and `best_value`:**

```python
best_action = None
best_value = float("-inf") if is_maximizing else float("inf")
```

- You need to keep track of the action that gives you the best score.
    
- `best_value` is initialized to negative infinity for 'X' (because X wants higher values) and positive infinity for 'O' (because O wants lower values).

3. **Evaluate Each _First_ Move:**

```python
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
        best_value = value     # Update the best score found
        best_action = action   # Store the action that led to this score
```

-  This loop considers all immediate possible moves from the current `board`.
        
    - For each `action`, it simulates the `result` and then calls `get_value` (which recursively explores the rest of the game) to find out what score that `action` eventually leads to.
        
    - It then compares that `value` to the `best_value` found so far and updates both `best_value` and `best_action` if a better move is found.
        
4. **Return the Optimal Action:**

```python
return best_action
```

- After checking all immediate possible moves, `best_action` will hold the move that leads to the optimal outcome.

**Full Code for MiniMax**:

```python
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
```
