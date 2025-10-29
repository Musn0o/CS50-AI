## Heredity Project Solution Notes

### 1. Project Goal & Core Concepts

The main goal of this project is to build a system that can estimate the likelihood of a person inheriting a particular genetic trait based on their family history. This involves using probabilistic models to handle the uncertainty inherent in genetics.

**Core Concepts Utilized:**

-   **Probability Theory:** The foundation of the project. We use probabilities to represent the chances of having a certain number of genes and exhibiting a trait.
-   **Conditional Probability:** The probability of an event occurring given that another event has already occurred. For example, the probability of a child having a gene, given the genetic makeup of their parents.
-   **Joint Probability:** The probability of multiple events happening at the same time. In this project, we calculate the joint probability of a specific combination of genes and traits for all individuals in a family.
-   **Bayesian Inference:** We update our beliefs (probabilities) about the genetic makeup of individuals as we get more evidence (data from the family). The whole process of calculating joint probabilities for all possible worlds and then normalizing is a form of Bayesian inference.
-   **Normalization:** After calculating the joint probabilities for all possible scenarios, we need to normalize them so that the probabilities for any given person's gene count or trait expression sum to 1.

### 2. General Strategy for Solving the Problem

The overall approach is to consider every possible "world" or scenario. A world is defined by a specific combination of gene counts and trait expressions for every person in the dataset.

1.  **Load Data:** Read the family data from a CSV file, which includes information about each person's name, mother, father, and whether they exhibit the trait.

2.  **Generate All Possible Scenarios:** Using the `powerset` function, we generate all possible subsets of people for having one gene, two genes, and the trait. This allows us to iterate through every single possible world.

3.  **Calculate Joint Probability for Each Scenario:** For each possible world, we calculate its joint probability using the `joint_probability` function. This function calculates the probability of that specific combination of genes and traits occurring, based on the laws of genetic inheritance and the given probabilities of mutation and trait expression.

4.  **Update Probabilities:** The joint probability of each world is added to the running total for the corresponding gene and trait distributions for each person. This is done by the `update` function.

5.  **Normalize Probabilities:** After iterating through all possible worlds, the accumulated probabilities for each person are normalized to ensure they form a valid probability distribution (i.e., they sum to 1).

### 3. Key Function Implementations

#### `joint_probability`

This is the core function of the project. It calculates the probability of a single, specific world.

-   It iterates through each person in the family.
-   For each person, it calculates two probabilities and multiplies them into the overall joint probability:
    1.  **Gene Probability:** The probability of the person having their assigned number of genes (0, 1, or 2).
        -   If the person has no parents in the dataset (a "founder"), this probability is taken directly from the `PROBS["gene"]` distribution.
        -   If the person has parents, this probability is calculated based on the parents' gene counts and the probability of passing on a gene (which includes the possibility of mutation).
    2.  **Trait Probability:** The probability of the person exhibiting (or not exhibiting) the trait, given their number of genes. This is a simple lookup from the `PROBS["trait"]` dictionary.

#### `update`

This function takes the joint probability of a single world (`p`) and adds it to the appropriate buckets in the `probabilities` dictionary. For each person, it updates the probability for their specific gene count and trait status in that particular world.

#### `normalize`

After all worlds have been processed, this function is called to clean up the `probabilities`. For each person, it takes the accumulated values for their gene distribution and trait distribution, and divides each value by the sum of the values in that distribution. This ensures that, for example, the sum of the probabilities of a person having 0, 1, or 2 genes is equal to 1.

### 4. Common Pitfalls and Lessons Learned

1.  **Combinatorial Explosion:** The number of possible worlds grows exponentially with the number of people. The `powerset` approach is feasible for small family trees but would be computationally intractable for very large ones. More advanced inference algorithms (like variable elimination or sampling methods) would be needed for larger problems.
2.  **Floating Point Precision:** When multiplying many small probabilities together, you can run into floating-point underflow issues. While not a major problem in this project due to the small scale, it's a key consideration in real-world probabilistic models.
3.  **Understanding Conditional Independence:** The model makes certain conditional independence assumptions. For example, a person's trait is independent of their parents' traits, given the person's own genotype. Understanding these assumptions is key to understanding how the model works.
4.  **The Power of Full Joint Distribution:** This project is a great illustration of how the full joint probability distribution can be used to answer any probabilistic query about the variables in the model. By calculating `P(Gene, Trait | Data)`, we can then derive `P(Gene | Data)` and `P(Trait | Data)` through marginalization (which is what the `normalize` function effectively helps us do).
