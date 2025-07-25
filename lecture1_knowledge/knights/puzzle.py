from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
# A is either a Knight or a Knave (but not both)
# These are universal truths about person A
knowledge0_universal_rules = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))

# A's statement logic: "I am both a knight and a knave."
# This is what A claims to be.
a_claims_to_be = And(AKnight, AKnave)

# Rules for what a Knight/Knave says:
# If A is a Knight, then their statement (a_claims_to_be) must be true.
knowledge0_if_knight_says_true = Implication(AKnight, a_claims_to_be)

# If A is a Knave, then their statement (a_claims_to_be) must be false.
knowledge0_if_knave_says_false = Implication(AKnave, Not(a_claims_to_be))


# Combine all pieces of knowledge for Puzzle 0
knowledge0 = And(
    knowledge0_universal_rules,
    knowledge0_if_knight_says_true,
    knowledge0_if_knave_says_false,
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

# Universal rules for A
knowledge1_universal_A = And(
    Or(AKnight, AKnave),  # A is either Knight or Knave
    Not(And(AKnight, AKnave)),  # A is not both Knight and Knave
)

# Universal rules for B
knowledge1_universal_B = And(
    Or(BKnight, BKnave),  # B is either Knight or Knave
    Not(And(BKnight, BKnave)),  # B is not both Knight and Knave
)

# A's statement logic: "We are both knaves."
a_claims_both_knaves = And(AKnave, BKnave)

# Rule: If A is a Knight, then their statement (a_claims_both_knaves) must be true.
knowledge1_A_says_truth_if_knight = Implication(AKnight, a_claims_both_knaves)

# Rule: If A is a Knave, then their statement (a_claims_both_knaves) must be false.
knowledge1_A_says_false_if_knave = Implication(AKnave, Not(a_claims_both_knaves))

# B says nothing, so no direct logical statements come from B's words.

# Combine all fundamental pieces of knowledge for Puzzle 1
knowledge1 = And(
    knowledge1_universal_A,
    knowledge1_universal_B,
    knowledge1_A_says_truth_if_knight,
    knowledge1_A_says_false_if_knave,
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

# Universal rules for A
universal_A = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))

# Universal rules for B
universal_B = And(Or(BKnight, BKnave), Not(And(BKnight, BKnave)))

# A's statement logic: "We are the same kind."
a_claims_both_same = Or(And(AKnight, BKnight), And(AKnave, BKnave))

# B's statement logic: "We are of different kinds."
b_claims_both_different = Or(And(BKnight, AKnave), And(BKnave, AKnight))

# Rule: If A is a Knight, then A's statement must be true
knowledge2_A_says_truth_if_knight = Implication(AKnight, a_claims_both_same)

# Rule: If A is a Knave, then A's statement must be false
knowledge2_A_says_false_if_knave = Implication(AKnave, Not(a_claims_both_same))

# Rule: If B is a Knight, then B's statement must be true
knowledge2_B_says_truth_if_knight = Implication(BKnight, b_claims_both_different)

# Rule: If B is a Knave, then B's statement must be false
knowledge2_B_says_false_if_knave = Implication(BKnave, Not(b_claims_both_different))

# Combine all knowledge including the essential universal rules
knowledge2 = And(
    universal_A,
    universal_B,
    knowledge2_A_says_truth_if_knight,
    knowledge2_A_says_false_if_knave,
    knowledge2_B_says_truth_if_knight,
    knowledge2_B_says_false_if_knave,
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

# Universal rules for A
universal_A = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))

# Universal rules for B
universal_B = And(Or(BKnight, BKnave), Not(And(BKnight, BKnave)))

# Universal rules for C
universal_C = And(Or(CKnight, CKnave), Not(And(CKnight, CKnave)))

# A's statement logic: I am a knight." or "I am a knave.", but you don't know which.
A_claims_to_be = Or(AKnight, AKnave)

# B's statement 1 logic: "A said 'I am a knave'."
b_claims_1 = AKnave

# B's statement 2 logic: "C is a knave."
b_claims_2 = CKnave

# C's statement logic: "A is a knight."
c_claims = AKnight

# Rule: If A is a Knight, then A's statement must be true
knowledge3_A_says_truth_if_knight = Implication(AKnight, A_claims_to_be)

# Rule: If A is a Knave, then A's statement must be false
knowledge3_A_says_false_if_knave = Implication(AKnave, Not(A_claims_to_be))

# Rule: If B is a Knight, then B's statement must be true
knowledge2_B_says_truth_if_knight = Implication(BKnight, b_claims_both_different)

# Rule: If B is a Knave, then B's statement must be false
knowledge2_B_says_false_if_knave = Implication(BKnave, Not(b_claims_both_different))


knowledge3 = And()


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
