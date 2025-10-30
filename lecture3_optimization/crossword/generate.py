import sys
from crossword import *


class CrosswordCreator:
    """TODO: Add docstring for CrosswordCreator class"""

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        # Store the Crossword object which holds structure, words, and variables
        self.crossword = crossword
        # Initialize domains for all variables, initially allowing all words as possibilities
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        # Initialize an empty 2D list (grid) to hold letters
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        # Iterate over each variable and its assigned word in the assignment
        for variable, word in assignment.items():
            direction = variable.direction
            # Iterate through each letter of the assigned word
            for k in range(len(word)):
                # Calculate the row (i) index based on direction (k only applies if DOWN)
                i = variable.i + (k if direction == Variable.DOWN else 0)
                # Calculate the column (j) index based on direction (k only applies if ACROSS)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                # Place the letter in the calculated grid position
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        # Get the 2D grid of letters based on the current assignment
        letters = self.letter_grid(assignment)
        # Loop through each row
        for i in range(self.crossword.height):
            # Loop through each column
            for j in range(self.crossword.width):
                # Check if the cell is part of the crossword structure
                if self.crossword.structure[i][j]:
                    # Print the letter (or a space if None) without a newline
                    print(letters[i][j] or " ", end="")
                else:
                    # Print a block character for non-word cells
                    print("█", end="")
            # Print a newline after each row is complete
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        # Import necessary modules for image generation
        from PIL import Image, ImageDraw, ImageFont

        # Define dimensions and spacing for the image
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        # Get the letter grid
        letters = self.letter_grid(assignment)
        # Create a new blank image with black background
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        # Load a font for displaying letters
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        # Prepare the drawing context
        draw = ImageDraw.Draw(img)
        # Loop through rows and columns to draw cells
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                # Define the coordinates for the cell rectangle
                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                # Check if the cell is part of the crossword structure (word path)
                if self.crossword.structure[i][j]:
                    # Draw a white rectangle for the cell interior
                    draw.rectangle(rect, fill="white")
                    # If a letter is assigned to this cell
                    if letters[i][j]:
                        # Calculate text bounding box for centering
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        # Draw the letter, centered within the cell
                        draw.text(
                            (
                                rect[0][0] + (interior_size - w) / 2,
                                rect[0][1] + (interior_size - h) / 2 - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )
        # Save the final image to the specified filename
        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        # Apply node consistency (unary constraints: word length)
        self.enforce_node_consistency()
        # Apply arc consistency (binary constraints: letter overlaps)
        self.ac3()
        # Start the recursive backtracking search with an empty initial assignment
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Iterate over every variable (position in the crossword)
        for var in self.crossword.variables:
            # Iterate over a copy of the words set to check against the variable's length
            for word in self.crossword.words:
                # If the word's length doesn't match the required length for the variable
                if len(word) != var.length:
                    # Remove the inconsistent word from the variable's domain
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        # Get the overlap indices (i for x, j for y)
        overlap = self.crossword.overlaps[x, y]
        # If there is no overlap, no revision is possible
        if overlap is None:
            return revised
        i, j = overlap
        # Iterate over a copy of the domain of x (safe for removal)
        for word1 in self.domains[x].copy():
            # Check if ANY word2 in domain[y] has the same letter at the overlap index j
            if not any((word1[i] == word2[j] for word2 in self.domains[y])):
                # If no consistent word exists in domain[y], remove word1 from domain[x]
                self.domains[x].remove(word1)
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If no initial arcs are provided, generate all binary arcs
        if arcs is None:
            arcs = []
            for var1 in self.crossword.variables:
                for var2 in self.crossword.neighbors(var1):
                    # Add arc (var1, var2) to the queue
                    arcs.append((var1, var2))
        # Process the queue of arcs
        while arcs:
            x, y = arcs.pop(0)
            # Try to revise the domain of x based on y
            if self.revise(x, y):
                # If revision caused the domain of x to become empty, consistency failed
                if not self.domains[x]:
                    return False
                # Re-queue all arcs (z, x) where z is a neighbor of x (excluding y)
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.append((z, x))
        # Consistency enforced successfully
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check if the set of assigned variables matches the set of all crossword variables
        return set(self.crossword.variables) == set(assignment.keys())

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check unary constraints (length) and binary constraints (overlaps)
        for var, word in assignment.items():
            # 1. Unary constraint check: assigned word length must match variable length
            if var.length != len(word):
                return False
            # 2. Binary constraint check: iterate through neighbors
            for neighbor in self.crossword.neighbors(var):
                # Only check neighbors that are also assigned
                if neighbor in assignment:
                    # Get the overlap indices
                    i, j = self.crossword.overlaps[var, neighbor]
                    # Check if the letters at the overlap point conflict
                    if word[i] != assignment[neighbor][j]:
                        return False
        # If all checks pass, the assignment is consistent
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Dictionary to store the count of ruled-out values for each domain word
        n_values = {}
        # Iterate over each possible word (value) in the variable's domain
        for value in self.domains[var]:
            n_values[value] = 0
            # Iterate over the unassigned neighbors of the current variable
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    continue
                # Get the overlap index for the current variable (i) and the neighbor (j)
                i, j = self.crossword.overlaps[var, neighbor]
                # Check how many domain values of the neighbor are ruled out by the current value
                for neighbor_value in self.domains[neighbor]:
                    # If the letters at the overlap point do not match, the neighbor's value is ruled out
                    if value[i] != neighbor_value[j]:
                        n_values[value] += 1
        # Sort the domain values (words) by the count of ruled-out neighbor values (Minimum Remaining Values heuristic)
        return sorted(n_values, key=n_values.get)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = None
        # Iterate over all variables to find the best unassigned one
        for var in self.crossword.variables:
            if var not in assignment:
                # If this is the first unassigned variable found, set it as the current best
                if unassigned is None:
                    unassigned = var
                # Primary heuristic: Choose the variable with the Minimum Remaining Values (MRV)
                elif len(self.domains[var]) < len(self.domains[unassigned]):
                    unassigned = var
                # Tie-breaker: If MRV is tied, choose the variable with the highest degree (most neighbors)
                elif len(self.domains[var]) == len(self.domains[unassigned]):
                    if len(self.crossword.neighbors(var)) > len(
                        self.crossword.neighbors(unassigned)
                    ):
                        unassigned = var
        return unassigned

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Base case: If the assignment is complete, a solution is found
        if self.assignment_complete(assignment):
            return assignment
        # Select the next unassigned variable using heuristics (MRV, Degree)
        var = self.select_unassigned_variable(assignment)
        # Iterate over the variable's domain values, ordered by LCV heuristic
        for value in self.order_domain_values(var, assignment):
            # Try assigning the value
            assignment[var] = value
            # Check for consistency (no conflicts with existing assignments)
            if self.consistent(assignment):
                # Recurse: continue backtracking search with the new partial assignment
                result = self.backtrack(assignment)
                # If recursion returns a non-None result, a solution was found down this path
                if result is not None:
                    return result
            # Backtrack step: if no solution found, remove the assignment
            del assignment[var]
        # If the loop finishes, no value for 'var' leads to a solution
        return None


def main():
    """TODO: Add docstring for main function"""
    # Check for correct number of command-line arguments (structure file, words file, optional output file)
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Load the crossword structure and available words
    crossword = Crossword(structure, words)

    # Initialize the CrosswordCreator
    creator = CrosswordCreator(crossword)

    # Solve the crossword using CSP techniques
    assignment = creator.solve()

    # Handle the result
    if assignment is None:
        print("No solution.")
    else:
        # Print the solved crossword to the terminal
        creator.print(assignment)
        # If an output filename was provided, save the result as an image
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
