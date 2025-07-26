import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __hash__(self):
        # Use frozenset for hashability, since set is unhashable
        return hash((frozenset(self.cells), self.count))

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        else:
            pass

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        else:
            pass


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 2) mark the cell as safe
        self.mark_safe(cell)

        # Collect neighbors for the new sentence and adjust count
        new_sentence_cells = set()
        mines_around_clicked_cell = 0

        # Iterate over all 8 potential neighbors
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Skip the clicked cell itself
                if (i, j) == cell:
                    continue

                # Check if neighbor is within board boundaries
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbor = (i, j)
                    # If this neighbor is a known mine, decrement the count for the sentence
                    if neighbor in self.mines:
                        mines_around_clicked_cell += 1
                    # If this neighbor is NOT a known safe or mine, it's an unknown cell for the new sentence
                    elif neighbor not in self.safes:  # Already marked safe in step 2
                        new_sentence_cells.add(neighbor)

        # 3) Create and add the new sentence to the AI's knowledge base
        # The count for the new sentence is the original count minus the known mines among neighbors
        new_sentence = Sentence(new_sentence_cells, count - mines_around_clicked_cell)

        # Only add non-empty sentences (e.g., if new_sentence_cells is empty and count is 0, it's trivial)
        # Also avoid adding duplicates to prevent infinite loops or redundant work
        if new_sentence not in self.knowledge and (
            new_sentence.cells or new_sentence.count > 0
        ):
            self.knowledge.append(new_sentence)

        # Loop to repeatedly apply deductions and inferences until no new knowledge is gained
        something_changed = True
        while something_changed:
            something_changed = False

            # Part 4: Mark any additional cells as safe or as mines
            # based on the AI's knowledge base
            newly_identified_safes = set()
            newly_identified_mines = set()

            # First, gather all known safes/mines from current sentences
            # Iterate over a copy to avoid issues if knowledge base is modified
            for sentence in list(self.knowledge):
                newly_identified_safes.update(sentence.known_safes())
                newly_identified_mines.update(sentence.known_mines())

            # Now, apply these new findings to the AI's overall knowledge
            # and update all sentences. This might change `self.knowledge`.
            for safe_cell in newly_identified_safes:
                if safe_cell not in self.safes:  # Only mark if truly new
                    self.mark_safe(
                        safe_cell
                    )  # This will loop through self.knowledge and update sentences
                    something_changed = True

            for mine_cell in newly_identified_mines:
                if mine_cell not in self.mines:  # Only mark if truly new
                    self.mark_mine(
                        mine_cell
                    )  # This will loop through self.knowledge and update sentences
                    something_changed = True

            # Important: Remove redundant sentences (e.g., empty sentences with count 0)
            # This helps keep the knowledge base clean and prevent infinite loops.
            sentences_to_remove = set()
            for sentence in list(self.knowledge):  # Iterate over a copy
                if not sentence.cells and sentence.count == 0:
                    sentences_to_remove.add(sentence)

            for sentence in sentences_to_remove:
                if (
                    sentence in self.knowledge
                ):  # Check if still present after modifications
                    self.knowledge.remove(sentence)
                    something_changed = True

            # Part 5: Infer new sentences from existing knowledge (subset rule)
            newly_inferred_sentences = []
            # Iterate over a copy of the knowledge base to avoid modification issues
            for s1 in list(self.knowledge):
                for s2 in list(self.knowledge):
                    # Don't compare a sentence to itself
                    if s1 == s2:
                        continue

                    # If s1 is a subset of s2
                    if s1.cells.issubset(s2.cells):
                        # Calculate the new inferred sentence: s2 - s1 = s2.count - s1.count
                        inferred_cells = s2.cells - s1.cells
                        inferred_count = s2.count - s1.count

                        # Ensure validity of the new sentence (e.g., count not negative)
                        if (
                            inferred_count < 0
                        ):  # This implies a logical contradiction or error in prior steps
                            # This case implies something is wrong, might want to raise an error
                            # or skip, but should ideally not occur with correct logic.
                            continue

                        new_s = Sentence(inferred_cells, inferred_count)

                        # Add the new sentence only if it's not already known
                        # and if it's not a trivial empty sentence (e.g., set() = 0)
                        if new_s not in self.knowledge and (
                            new_s.cells or new_s.count > 0
                        ):
                            newly_inferred_sentences.append(new_s)
                            something_changed = True  # We found a new sentence

            # Add all newly inferred sentences to the knowledge base
            for new_s in newly_inferred_sentences:
                if (
                    new_s not in self.knowledge
                ):  # Double check to avoid duplicates if added by another part of loop
                    self.knowledge.append(new_s)

            # If no changes were made in this entire loop iteration, we are done
            if not something_changed:
                break

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made
        if safe_moves:
            return random.choice(list(safe_moves))
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
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
