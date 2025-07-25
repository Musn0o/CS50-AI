## Knave or Knight Project Solution Notes

### 1. Project Goal & Core Concepts

The primary goal of this project was to learn how to represent knowledge and perform logical inference using propositional logic. You essentially built a small "expert system" that can deduce facts (who is a Knight or a Knave) based on a set of given rules and statements.

**Core Concepts Utilized:**

- **Propositional Logic:** The foundation. Everything is represented as propositions (statements that are either true or false).
    
- **Logical Connectives:**
    
    - `And(P, Q)`: P and Q. True only if both P and Q are true.
        
    - `Or(P, Q)`: P or Q. True if P, Q, or both are true (Inclusive OR).
        
    - `Not(P)`: Not P. True if P is false.
        
    - `Implication(P, Q)` (P → Q): If P then Q. False _only_ if P is true and Q is false. Otherwise true.
        
    - `Equivalence(P, Q)` (P ↔ Q): P if and only if Q. True if P and Q have the same truth value.
        
- **Knowledge Base (KB):** This is the collection of all logical statements (axioms, facts, implications) that the AI knows about the world. For these puzzles, `knowledge0`, `knowledge1`, etc., were your KBs. All propositions within the KB are joined by `And()`.
    
- **Model Checking / Satisfiability:** The underlying mechanism (provided by the `logic.py` library's `model_check` function) that goes through all possible assignments of truth values to propositional symbols and finds those that make the entire Knowledge Base true. If only one such assignment exists, it's a unique solution.
    

### 2. General Strategy for Solving Each Puzzle

The approach for each puzzle followed a consistent pattern:

1. **Define Universal Rules for ALL Characters Present:**
    
    - For every character (e.g., A, B, C) in the current puzzle, you must include two foundational axioms in your `knowledgeX` variable:
        
        - **`Or(PersonKnight, PersonKnave)`**: Each person is _either_ a Knight _or_ a Knave.
            
        - **`Not(And(PersonKnight, PersonKnave))`**: No person can be _both_ a Knight AND a Knave.
            
    - These rules are fundamental and **must be included in every puzzle's knowledge base**, as they define the very nature of a Knight/Knave.
        
2. **Translate Each Character's Utterance into a Logical Proposition:**
    
    - This is the "What they say" part. For example, if A says "I am a knight," `WhatA_says = AKnight`. If B says "A is a knave and I am a knight," `WhatB_says = And(AKnave, BKnight)`.
        
    - Pay close attention to logical connectives (`and`, `or`, `not`) within the natural language.
        
3. **Apply the Knight/Knave Implication Rule:**
    
    - This is the crucial step that links a character's identity to the truthfulness of their statement. For every character (`P`) and their statement (`S`):
        
        - **If P is a Knight, then their statement S must be TRUE:** `Implication(PKnight, S)`
            
        - **If P is a Knave, then their statement S must be FALSE:** `Implication(PKnave, Not(S))`
            
4. **Combine All Knowledge:**
    
    - Use the `And()` connective to combine all the universal rules and all the implications derived from each character's statement into a single `knowledgeX` variable for that specific puzzle.
        

### 3. Specific Puzzle Insights

#### Puzzle 0: A says "I am both a knight and a knave."

- **A's statement (`A_claims_to_be`):** `And(AKnight, AKnave)`
    
- **Key Deduction:**
    
    - If A were a Knight, then `And(AKnight, AKnave)` would have to be true. This immediately leads to `AKnight` AND `AKnave`, which contradicts the universal rule that A cannot be both (`Not(And(AKnight, AKnave))`). So, A cannot be a Knight.
        
    - Therefore, A must be a Knave.
        
    - If A is a Knave, then `Not(And(AKnight, AKnave))` must be true. This is consistent with the universal rule.
        
- **Result:** A is a Knave.
    

#### Puzzle 1: A says "We are both knaves." B says nothing.

- **A's statement (`A_claims_both_knaves`):** `And(AKnave, BKnave)`
    
- **Key Deduction:**
    
    - Similar to Puzzle 0, if A were a Knight, A's statement `And(AKnave, BKnave)` would be true, meaning `AKnave` is true. This contradicts A being a Knight. So, **A must be a Knave.**
        
    - Since A is a Knave, A's statement `And(AKnave, BKnave)` must be FALSE.
        
    - `Not(And(AKnave, BKnave))` is equivalent to `Or(Not(AKnave), Not(BKnave))` by De Morgan's Law.
        
    - Since we know `AKnave` is true, then `Not(AKnave)` is false.
        
    - For `Or(False, Not(BKnave))` to be true, `Not(BKnave)` must be true.
        
    - If `Not(BKnave)` is true, then `BKnave` is false.
        
    - Since B must be either a Knight or a Knave, and is not a Knave, then **B must be a Knight.**
        
- **Result:** A is a Knave, B is a Knight.
    

#### Puzzle 2: A says "We are the same kind." B says "We are of different kinds."

- **A's statement (`a_claims_both_same`):** `Or(And(AKnight, BKnight), And(AKnave, BKnave))`
    
- **B's statement (`b_claims_both_different`):** `Or(And(AKnight, BKnave), And(AKnave, BKnight))` (Or `Xor(AKnight, BKnight)`)
    
- **Key Deduction Path (Simplified):**
    
    - If A is a Knight, A's statement (`a_claims_both_same`) is true. This means A and B are the same kind. So, B must be a Knight.
        
        - If B is a Knight, B's statement (`b_claims_both_different`) is true. This means A and B are different kinds.
            
        - Contradiction! (A and B are same kind AND A and B are different kinds).
            
        - Therefore, the initial assumption (A is a Knight) must be false. **A must be a Knave.**
            
    - Since A is a Knave, A's statement (`a_claims_both_same`) is false. This means A and B are NOT the same kind. So, B must be a Knight.
        
    - If B is a Knight, B's statement (`b_claims_both_different`) is true. This means A and B are different kinds. This is consistent with A being a Knave and B being a Knight.
        
- **Result:** A is a Knave, B is a Knight.
    

#### Puzzle 3: Nested Statements and Complex Deductions

- **A says:** "I am a knight or I am a knave."
    
    - `A_claims_to_be = Or(AKnight, AKnave)`
        
    - **Insight:** From our universal rules, `Or(AKnight, AKnave)` is _always true_.
        
    - If A were a Knave, A's statement (`Or(AKnight, AKnave)`) would have to be false (`Not(Or(AKnight, AKnave))`). But `Not(True)` is `False`. So `Implication(AKnave, False)` means `AKnave` must be False.
        
    - Therefore, **A must be a Knight.**
        
- **B says:** "A said 'I am a knave'."
    
    - **This is the trickiest part.** B is making a claim about what A _said_.
        
    - If A says "I am a knave" (`AKnave`), that means `(AKnight <==> AKnave)`. (If A is Knight, AKnave is true, contradiction. If A is Knave, AKnave is false, contradiction). This statement `(AKnight <==> AKnave)` is inherently `False` in any consistent world.
        
    - So, B is making a claim that is logically `False`.
        
    - If B says something `False`, then **B must be a Knave.**
        
    - `b_claims_1 = Equivalence(AKnight, AKnave)`
        
- **B also says:** "C is a knave."
    
    - `b_claims_2 = CKnave`
        
    - Since B is a Knave, _both_ of B's claims (the combined `And(b_claims_1, b_claims_2)`) must be false.
        
    - We know `b_claims_1` (`Equivalence(AKnight, AKnave)`) is false, so `Not(b_claims_1)` is true. This already satisfies `Not(And(b_claims_1, b_claims_2))`. This doesn't directly force C's type yet.
        
- **C says:** "A is a knight."
    
    - `c_claims = AKnight`
        
    - Since we deduced **A is a Knight**, C's statement "A is a knight" is TRUE.
        
    - If C's statement is TRUE, then **C must be a Knight.**
        
- **Result:** A is a Knight, B is a Knave, C is a Knight.
    

### 4. Common Pitfalls and Lessons Learned

1. **"Too Direct" Statements:** The biggest lesson is to avoid encoding your own deductions directly into the knowledge base. Your `knowledgeX` variables should only contain the raw facts from the puzzle description and the universal rules of the game. Let the logical solver do the heavy lifting of deduction.
    
2. **Missing Universal Rules:** Remember to include the `Or(PersonKnight, PersonKnave)` and `Not(And(PersonKnight, PersonKnave))` for _every_ character in _every_ puzzle's `knowledgeX`. They are fundamental definitions.
    
3. **Precise Translation of Natural Language:** This is where most errors occur.
    
    - "A and B" means `And(A, B)`.
        
    - "A or B" (inclusive) means `Or(A, B)`.
        
    - "A but not B" means `And(A, Not(B))`.
        
    - "If X then Y" means `Implication(X, Y)`.
        
    - "X if and only if Y" means `Equivalence(X, Y)`.
        
    - **Nested Statements/Reported Speech:** This was the most challenging. "Person X says 'Person Y said "Statement S"'" translates to `X` claiming the truth of `(YKnight <==> S)`. Be very careful when someone is reporting on _another person's speech_.
        
4. **Understanding `Implication`:** The rule `Implication(P, Q)` being true when `P` is false is often counter-intuitive. Remember the "broken promise" analogy. This property is crucial for how logical solvers find consistent models.
    
5. **Importance of `And()` for the KB:** The entire knowledge base for a puzzle is one giant `And` statement of all the individual logical sentences. If any part of that `And` leads to a contradiction, the solver knows it's an inconsistent model.