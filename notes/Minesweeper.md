## Minesweeper AI Project: Implementation Notes

### I. Overall Goal

The goal of the Minesweeper AI project is to create an intelligent agent that can play Minesweeper by using logical inference. The AI should deduce the location of mines and safe cells based on the numbers revealed on the board, rather than guessing randomly (unless no logical moves are available).

### II. `Sentence` Class

The `Sentence` class represents a single logical statement about the Minesweeper board. A sentence is defined by a `set` of `cells` and a `count` representing how many mines are among those specific cells.

**1. `__init__(self, cells, count)`**

- **Purpose:** Initializes a new `Sentence` object.
    
- **Implementation:**
    
    - `self.cells`: Store the input `cells` as a `set`. This ensures uniqueness and allows for efficient set operations (like `issubset`, `remove`, `-`).
        
    - `self.count`: Store the integer `count`.
        
- **Code:**

```python
def __init__(self, cells, count):
    self.cells = set(cells)
    self.count = count
```

**2. `__eq__(self, other)`**

- **Purpose:** Defines how two `Sentence` objects are compared for equality. This is crucial for checking if a new inferred sentence already exists in `knowledge`.
    
- **Implementation:** Two sentences are equal if they contain the exact same set of cells AND the same count.
    
- **Code:**

```python
def __eq__(self, other):
    return self.cells == other.cells and self.count == other.count
```

**3. `__str__(self)`**

- **Purpose:** Provides a human-readable string representation of the sentence, helpful for debugging.
    
- **Implementation:** Format the set of cells and the count.
    
- **Code:**

```python
def __str__(self):
    return f"{self.cells} = {self.count}"
```

**4. `known_mines(self)`**

- **Purpose:** Identifies cells that _must_ be mines based _solely_ on this sentence.
    
- **Logic:** If the number of unknown cells in the sentence (`len(self.cells)`) is exactly equal to the `count` of mines in those cells, then all those cells must be mines.
    
- **Implementation:** Return `self.cells` if the condition is met, otherwise an empty set.
    
- **Code:**

```python
def known_mines(self):
    if len(self.cells) == self.count and self.count != 0: # Note: removed "and self.count != 0" in review, but if it passed with it, it means the other logic compensates. Standard is without.
        return self.cells
    else:
        return set()
```

_Self-correction note from previous review_: The `and self.count != 0` check in `known_mines` is usually not needed. If `len(self.cells) == self.count` and both are 0, it means `{} = 0`, which has no mines, correctly returning `set()`. If it passed with it, it's harmless, but logically redundant.

**5. `known_safes(self)`**

- **Purpose:** Identifies cells that _must_ be safe based _solely_ on this sentence.
    
- **Logic:** If the `count` of mines in the sentence is `0`, then all cells in that sentence must be safe.
    
- **Implementation:** Return `self.cells` if the condition is met, otherwise an empty set.
    
- **Code:**

```python
def known_safes(self):
    if self.count == 0:
        return self.cells
    else:
        return set()
```

**6. `mark_mine(self, cell)`**

- **Purpose:** Updates the sentence's internal state when a specific `cell` is externally known to be a mine. This is a crucial step for **constraint propagation**.
    
- **Logic:** If the known mine `cell` is part of this sentence:
    
    1. Remove `cell` from `self.cells`.
        
    2. Decrement `self.count` by 1.
        
- **Implementation:** Check if `cell` is in `self.cells` before performing updates.
    
- **Code:**

```python
def mark_mine(self, cell):
    if cell in self.cells:
        self.cells.remove(cell)
        self.count -= 1
```

**7. `mark_safe(self, cell)`**

- **Purpose:** Updates the sentence's internal state when a specific `cell` is externally known to be safe. Also crucial for **constraint propagation**.
    
- **Logic:** If the known safe `cell` is part of this sentence:
    
    1. Remove `cell` from `self.cells`. The `count` does not change because `cell` was known not to be a mine.
        
- **Implementation:** Check if `cell` is in `self.cells` before performing updates.
    
- **Code:**

```python
def mark_safe(self, cell):
    if cell in self.cells:
        self.cells.remove(cell)
```

### III. `MinesweeperAI` Class

The `MinesweeperAI` class manages the overall knowledge of the game and decides the next move.

**1. `__init__(self, height=8, width=8)`**

- **Purpose:** Initializes the AI's core data structures.
    
- **Implementation:**
    
    - `self.height`, `self.width`: Board dimensions.
        
    - `self.moves_made`: `set` of cells already clicked.
        
    - `self.mines`: `set` of cells known to be mines.
        
    - `self.safes`: `set` of cells known to be safe.
        
    - `self.knowledge`: `list` of `Sentence` objects representing the AI's current logical understanding.
        
- **Code:**

```python
def __init__(self, height=8, width=8):
    self.height = height
    self.width = width
    self.moves_made = set()
    self.mines = set()
    self.safes = set()
    self.knowledge = []
```

**2. `mark_mine(self, cell)`**

- **Purpose:** Adds a `cell` to the AI's overall `mines` set and propagates this new knowledge to all existing sentences.
    
- **Implementation:**
    
    1. Add `cell` to `self.mines`.
        
    2. Iterate through `self.knowledge` and call `sentence.mark_mine(cell)` for each sentence. This ensures all sentences are updated with this new definitive mine location.
        
- **Code:**

```python
def mark_mine(self, cell):
    self.mines.add(cell)
    for sentence in list(self.knowledge): # Iterate over a copy to handle modifications within loop
        sentence.mark_mine(cell)
```

**3. `mark_safe(self, cell)`**

- **Purpose:** Adds a `cell` to the AI's overall `safes` set and propagates this new knowledge to all existing sentences.
    
- **Implementation:**
    
    1. Add `cell` to `self.safes`.
        
    2. Iterate through `self.knowledge` and call `sentence.mark_safe(cell)` for each sentence.
        
- **Code:**

```python
def mark_safe(self, cell):
    self.safes.add(cell)
    for sentence in list(self.knowledge): # Iterate over a copy
        sentence.mark_safe(cell)
```

**4. `add_knowledge(self, cell, count)`**

- **Purpose:** This is the core reasoning engine. It takes new information from the board (a `cell` that was clicked and its `count` of neighboring mines) and uses it to update the AI's knowledge base, deduce new facts, and infer new sentences.
    
- **Implementation Steps:**
    
    - **Step 1: Mark the cell as a move made.**
		```python
self.moves_made.add(cell)
```
	- **Step 2: Mark the cell as safe.**
	
		- Crucially, this `self.mark_safe(cell)` call will also update all existing sentences in `self.knowledge`.
		```python
		self.mark_safe(cell)
```
	-  **Step 3: Add a new sentence to the AI's knowledge base.**

		- This new sentence is derived from the clicked `cell` and its `count`. It refers to the **unknown** neighbors of the clicked `cell`.
		    
		- You must find all neighbors of `cell`.
		    
		- Adjust the `count` by subtracting any neighbors already known to be mines.
		    
		- The new sentence should only include neighbors whose status (mine/safe) is still unknown.
		```python
# Collect neighbors for the new sentence and adjust count
new_sentence_cells = set()
mines_around_clicked_cell = 0
for i in range(cell[0] - 1, cell[0] + 2):
    for j in range(cell[1] - 1, cell[1] + 2):
        if (i, j) == cell: # Skip the clicked cell itself
            continue
        if 0 <= i < self.height and 0 <= j < self.width: # Check board boundaries
            neighbor = (i, j)
            if neighbor in self.mines:
                mines_around_clicked_cell += 1
            elif neighbor not in self.safes:
                new_sentence_cells.add(neighbor)

new_sentence = Sentence(new_sentence_cells, count - mines_around_clicked_cell)

# Add the new sentence only if it's not a duplicate and not an empty/trivial sentence (e.g., {} = 0)
if new_sentence not in self.knowledge and (new_sentence.cells or new_sentence.count > 0):
    self.knowledge.append(new_sentence)
```
	- **Step 4 & 5: Iterative Deduction and Inference Loop.**

		- This is the most critical part. Deductions (known mines/safes) and inferences (new sentences from subsets) can cascade. You must repeatedly apply them until no new information can be gained in a full pass.
		    
		- Use a `while something_changed:` loop. `something_changed` should be `True` at the start of each iteration and reset to `False` if no new facts or sentences are added in that iteration.

		```python
something_changed = True
while something_changed:
    something_changed = False

# --- Step 4.1: Apply known_safes/known_mines from existing sentences ---
    newly_identified_safes = set()
    newly_identified_mines = set()

    # Gather all known safes/mines from current sentences
    for sentence in list(self.knowledge): # Iterate over a copy
        newly_identified_safes.update(sentence.known_safes())
        newly_identified_mines.update(sentence.known_mines())

    # Mark newly identified cells as safe/mine (this calls self.mark_safe/mark_mine)
    for safe_cell in newly_identified_safes:
        if safe_cell not in self.safes: # Only mark if truly new to AI's safes set
            self.mark_safe(safe_cell)
            something_changed = True

    for mine_cell in newly_identified_mines:
        if mine_cell not in self.mines: # Only mark if truly new to AI's mines set
            self.mark_mine(mine_cell)
            something_changed = True

    # --- Step 4.2: Remove redundant sentences (e.g., empty sentences with count 0) ---
    # This is important after mark_mine/mark_safe update sentences, as some may become trivial.
    sentences_to_remove = []
    for sentence in list(self.knowledge): # Iterate over a copy
        if not sentence.cells and sentence.count == 0:
            sentences_to_remove.append(sentence)
        # Also, remove sentences whose count is negative (implies contradiction, though should ideally not happen)
        # or where count > len(cells)
        elif sentence.count < 0 or sentence.count > len(sentence.cells):
            sentences_to_remove.append(sentence)

    for sentence in sentences_to_remove:
        if sentence in self.knowledge: # Check if still present
            self.knowledge.remove(sentence)
            something_changed = True

    # --- Step 5: Infer new sentences from existing knowledge (subset rule) ---
    newly_inferred_sentences = []
    for s1 in list(self.knowledge): # Iterate over copies
        for s2 in list(self.knowledge):
            if s1 == s2:
                continue # Don't compare a sentence to itself

            # If s1 is a subset of s2, a new sentence can be inferred
            # The rule: (A + B = X) and (A = Y) implies (B = X - Y)
            if s1.cells.issubset(s2.cells):
                inferred_cells = s2.cells - s1.cells
                inferred_count = s2.count - s1.count

                # Ensure validity of the new sentence
                if inferred_count < 0: # Indicates logical inconsistency (should not happen if logic is sound)
                    continue
                if inferred_cells and inferred_count == 0 and len(inferred_cells) > 0: # Example of a common scenario
                    # This means all cells in inferred_cells are safe. Mark them safe.
                    for cell_in_inferred in inferred_cells:
                        if cell_in_inferred not in self.safes:
                            self.mark_safe(cell_in_inferred)
                            something_changed = True
                    continue # Don't add this sentence if its cells are all marked safe

                new_s = Sentence(inferred_cells, inferred_count)

                # Add new sentence only if not already in knowledge and not trivial (e.g., {} = 0)
                if new_s not in self.knowledge and (new_s.cells or new_s.count > 0):
                    newly_inferred_sentences.append(new_s)
                    something_changed = True

    # Add all truly new inferred sentences to the knowledge base
    for new_s in newly_inferred_sentences:
        if new_s not in self.knowledge: # Double check to avoid duplicates if added by another part of loop
            self.knowledge.append(new_s)

    # If no changes were made across all steps in this loop iteration, break
    if not something_changed:
        break
```

**5. `make_safe_move(self)`**

- **Purpose:** Finds and returns a safe, unmade move.
    
- **Logic:** Returns any cell from `self.safes` that is not in `self.moves_made`.
    
- **Implementation:** Use set difference.
    
- **Code:**

```python
def make_safe_move(self):
    safe_moves = self.safes - self.moves_made
    if safe_moves:
        return random.choice(list(safe_moves))
    else:
        return None
```

**6. `make_random_move(self)`**

- **Purpose:** Returns a random move among cells that are not known mines and have not been made.
    
- **Logic:** Iterate through all possible cells on the board and filter them.
    
- **Implementation:** Use list comprehensions to create a list of valid moves, then pick randomly.
    
- **Code:**

```python
def make_random_move(self):
    safe_moves = [
        (i, j)
        for i in range(self.height)
        for j in range(self.width)
        if (i, j) not in self.moves_made and (i, j) not in self.mines
    ]
    if safe_moves:
        return random.choice(safe_moves)
    else:
        return None
```

### IV. Key Concepts and Takeaways

- **Knowledge Representation (Sentences):** How complex game state information is encapsulated into simple logical sentences (set of cells + count).
    
- **Constraint Propagation:** How knowing a new fact (a cell is a mine/safe) ripples through and updates _all_ related knowledge (all sentences containing that cell). This is handled by `mark_mine`/`mark_safe` methods in both classes.
    
- **Deduction/Inference:**
    
    - **Direct Deduction:** `known_mines` and `known_safes` deduce facts from single sentences.
        
    - **Subset Rule Inference:** The crucial `(s2 - s1) = (s2.count - s1.count)` rule allows inferring _new sentences_ from existing ones. This is a powerful form of logical reasoning.
        
- **Iterative Reasoning:** The `while something_changed:` loop in `add_knowledge` is fundamental. New information can trigger further deductions, which in turn trigger more. This loop ensures all possible deductions are made based on the current knowledge base.
    
- **Data Structure Management:**
    
    - Using `set` for cells in `Sentence` and AI's `mines`/`safes`/`moves_made` is efficient for `in` checks and set operations (`-`, `issubset`).
        
    - Iterating over `list(self.knowledge)` (a copy) when modifying `self.knowledge` or when `mark_mine`/`mark_safe` are called internally prevents `RuntimeError`.
        
    - Removing redundant/empty sentences from `self.knowledge` keeps the knowledge base clean and efficient.