import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

test_corpus = {"A": {"B"}, "B": {"C"}, "C": {"A"}}


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
    raise NotImplementedError


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

        if random.random() < damping_factor:
            # The surfer wants to follow a link.
            links_from_current_page = corpus[current_page]
            if links_from_current_page:
                # If there are links on the current page, choose one at random.
                next_page = random.choice(list(links_from_current_page))
                current_page = next_page
        else:
            # This is a key edge case!
            # If the page has no outgoing links, the surfer jumps to a random page from the entire corpus.
            next_page = random.choice(list(corpus.keys()))
            current_page = next_page

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
    raise NotImplementedError


# if __name__ == "__main__":
#     main()
pageranks = sample_pagerank(test_corpus, damping_factor=0.85, n=10000)
print(pageranks)
