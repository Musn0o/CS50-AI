import os
import random
import re
import sys

"""
PageRank Algorithm Implementation

Implements both sampling-based and iterative approaches to compute PageRank for a web corpus.

Key Components:
- Web corpus preprocessing
- Transition model with damping factor
- Monte Carlo sampling method
- Power iteration method
- Convergence checking

The algorithm handles dangling nodes (pages with no outgoing links) by treating them
as having links to all pages in the corpus.
"""
DAMPING = 0.85  # Damping factor (probability of following links vs random jump)
SAMPLES = 10000  # Number of samples for Monte Carlo simulation


def main() -> None:
    """
    Execute PageRank analysis on a web corpus directory.

    Handles command-line arguments and coordinates the ranking process.

    Args:
        sys.argv[1]: Path to directory containing HTML corpus

    Raises:
        SystemExit: If incorrect number of arguments provided
    """
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")

    # Process corpus and calculate rankings using both algorithms
    corpus = crawl(sys.argv[1])  # Build link graph from HTML files
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print("PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory: str) -> dict[str, set[str]]:
    """
    Parse a directory of HTML pages and build a web corpus graph.

    Args:
        directory: Path to directory containing HTML files
        corpus: Dictionary mapping page names to sets of linked pages

    Returns:
        Dictionary where:
        - Keys:   Page filenames (e.g. 'page1.html')
        - Values: Set of pages linked from the key page

    Example:
        corpus = crawl('corpus1')
        print(corpus['bfs.html'])  # {'dfs.html', 'search.html'}
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(
    corpus: dict[str, set[str]], page: str, damping_factor: float
) -> dict[str, float]:
    """
    Calculate transition probabilities for PageRank algorithm (Equation 1 in paper).

    Args:
        corpus: Web corpus from crawl()
        page: Current page being evaluated
        damping_factor: Probability of following existing links (vs random jump)

    Returns:
        Probability distribution over all pages where:
        - Sum of probabilities = 1.0
        - Probability = damping_factor * (1/out_links) + (1-damping_factor) * (1/N)

    Handles dangling nodes (pages with no links) by distributing probability evenly.

    Example:
        corpus = {'A': {'B'}, 'B': set()}
        model = transition_model(corpus, 'A', 0.85)
        # {'A': 0.075, 'B': 0.9 + 0.075 = 0.975}
    """
    # Handle normal pages with outgoing links (Equation 2 in paper)
    if corpus[page]:
        # Base probability from random jump (1-d)/N
        base_prob = (1 - damping_factor) / len(corpus)
        prob_dist = {p: base_prob for p in corpus}

        # Probability from following links (d * 1/out_degree)
        link_prob = damping_factor / len(corpus[page])
        for linked_page in corpus[page]:
            prob_dist[linked_page] += link_prob

        return prob_dist
    else:
        # Handle dangling nodes: uniform distribution (Section 2.7 in paper)
        return {p: 1 / len(corpus) for p in corpus}


def sample_pagerank(
    corpus: dict[str, set[str]], damping_factor: float, n: int
) -> dict[str, float]:
    """
    Estimate PageRank using Monte Carlo sampling (Algorithm 1 in paper).

    Args:
        corpus: Web corpus from crawl()
        damping_factor: Probability of following links vs random jump
        n: Number of samples to generate

    Returns:
        PageRank estimates where:
        - Values represent probability distribution (sum to 1.0)
        - Higher values indicate more important pages

    Complexity:
        Time: O(n) - Linear in number of samples
        Space: O(N) - Stores count for each page in corpus

    Example:
        ranks = sample_pagerank(corpus, 0.85, 100000)
    """
    # Initialize sampling counters and starting page
    counts = {page: 0 for page in corpus}
    page = random.choice(list(corpus.keys()))  # Uniform random initial selection
    for _ in range(n):
        counts[page] += 1
        model = transition_model(corpus, page, damping_factor)
        # Select next page using weighted probability distribution
        page = random.choices(
            population=list(model.keys()),
            weights=list(model.values()),  # Use computed probabilities as weights
            k=1,
        )[0]  # Extract single result from list
    ranks = {page: count / n for page, count in counts.items()}
    return ranks


def iterate_pagerank(
    corpus: dict[str, set[str]], damping_factor: float
) -> dict[str, float]:
    """
    Calculate PageRank using power iteration method (Equation 3 in paper).

    Args:
        corpus: Web corpus from crawl()
        damping_factor: Probability of following links vs random jump

    Returns:
        Converged PageRank values (sum to 1.0)

    Algorithm:
        1. Initialize ranks evenly
        2. Iteratively update ranks until max change < 0.001
        3. Handle dangling nodes by redistributing their rank

    Complexity:
        Time: O(k*N^2) where k=iterations, N=number of pages
        Space: O(N) - Maintains current and new ranks

    Example:
        ranks = iterate_pagerank(corpus, 0.85)
    """
    N = len(corpus)  # Total number of pages in corpus
    ranks = {page: 1 / N for page in corpus}
    while True:
        new_ranks = {}
        for page in corpus:
            total = 0.0
            # Calculate contribution from all possible linking pages
            for possible_page in corpus:
                # Handle dangling nodes (links to all pages)
                if not corpus[possible_page]:
                    total += ranks[possible_page] / N
                elif page in corpus[possible_page]:
                    # Add rank contribution from linking page
                    total += ranks[possible_page] / len(corpus[possible_page])

            # PageRank formula with damping factor
            new_rank = (1 - damping_factor) / N + damping_factor * total
            new_ranks[page] = new_rank

        # Check convergence using L1 norm (sum of absolute differences)
        # Threshold of 0.001 ensures <0.1% change for all pages
        if all(abs(new_ranks[page] - ranks[page]) < 0.001 for page in ranks):
            break
        ranks = new_ranks
    return ranks


if __name__ == "__main__":
    """Execute PageRank analysis on provided corpus directory"""
    main()
