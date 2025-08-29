import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print("PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
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


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_pages = len(corpus)
    distribution = {}

    # Get the links from the current page
    links_on_page = corpus[page]
    num_links = len(links_on_page)

    if num_links > 0:
        # Probability from the (1 - damping_factor) part, for every page
        base_prob = (1 - damping_factor) / num_pages
        # Probability from the damping_factor part, only for linked pages
        linked_prob = damping_factor / num_links

        for p in corpus:
            distribution[p] = base_prob
            if p in links_on_page:
                distribution[p] += linked_prob
    else:
        # If there are no outgoing links, choose any page with equal probability
        prob_per_page = 1 / num_pages
        for p in corpus:
            distribution[p] = prob_per_page

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Dictionary to store the counts
    counts = {page: 0 for page in corpus}

    # A variable to keep track of the current page the surfer is on
    current_page = None

    # Starting Point
    current_page = random.choice(list(corpus.keys()))

    # Simulate the surfer's journey for n steps
    for i in range(n):
        counts[current_page] += 1

        # Get the outgoing links from the current page
        links = corpus[current_page]

        # Decide whether to follow a link or jump to a random page
        if random.random() < damping_factor and links:
            # With probability 'damping_factor', if the current page has outgoing links,
            # choose one of them at random to be the next page.
            current_page = random.choice(list(links))
        else:
            # With probability '1 - damping_factor', or if the current page has no links,
            # choose a random page from the entire corpus to be the next page.
            # This handles the "dead end" case.
            current_page = random.choice(list(corpus.keys()))
    # Normalize these counts.
    # The PageRank for a page is its count divided by the total number of samples (n).
    pagerank = {page: count / n for page, count in counts.items()}

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)

    # Initialize pagerank with equal probability for each page
    pagerank = {page: 1 / num_pages for page in corpus}

    # Convergence threshold
    threshold = 0.001

    while True:
        # A dictionary to store the new pagerank values for the current iteration
        new_pagerank = {}

        # Calculate new PageRank for each page
        for page in corpus:
            # First part of the formula: the probability of a random jump
            new_rank = (1 - damping_factor) / num_pages

            # Second part of the formula: the probability from linked pages
            sigma = 0
            for i in corpus:
                # If page 'i' has links and one of them is to the current 'page'
                if page in corpus[i]:
                    sigma += pagerank[i] / len(corpus[i])

                # A page with no links is treated as linking to all pages
                if not corpus[i]:
                    sigma += pagerank[i] / num_pages

            new_rank += damping_factor * sigma
            new_pagerank[page] = new_rank

        # Check for convergence by finding the maximum change in PageRank values
        max_change = max(abs(new_pagerank[p] - pagerank[p]) for p in corpus)

        # Update pagerank for the next iteration
        pagerank = new_pagerank

        # If the change is less than the threshold, we have converged
        if max_change < threshold:
            break

    return pagerank


if __name__ == "__main__":
    main()
