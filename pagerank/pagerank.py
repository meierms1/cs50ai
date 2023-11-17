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
    print(f"PageRank Results from Iteration")
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
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    random_factor = 1 - damping_factor
    current_links = corpus[page]
    new_dict = {}
    


    for i in corpus:
        if i in current_links:
            new_dict[i] = damping_factor / len(current_links) + random_factor / len(corpus)
        else:
            new_dict[i] = damping_factor / len(corpus)

    return new_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pick = random.choice(list(corpus))
    rank = {}

    for i in corpus:
        rank[i] = 0
 
    for i in range(n):
        if len(corpus[pick]) > 1:
            new_page = random.choice(list(corpus[pick]))
        elif len(corpus[pick]) == 1:
            new_page = list(corpus[pick])[0]
        else:
            new_page = random.choice(list(corpus.keys()))

        
        rank[new_page] += 1 / n 
        tm = transition_model(corpus, new_page, damping_factor)
        vals = list(tm.keys())
        w = [round(rank[j], 4) for j in vals]
        pick = random.choices(list(corpus), w)[0]
    
    rank_sum = 0
    for i in corpus:
        rank_sum += rank[i]
    print(f'Sum Sampling: {round(rank_sum, 2)}')

    return rank
    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = {}
    N = len(corpus)
    error = {}

    for i in corpus:
        rank[i] = 1 / N
        error[i] = 1

    loop = True
    while loop:
        for i in corpus:
            pri = 0
            for j in corpus:
                if i in corpus[j]:
                    pri += rank[j] / len(corpus[j])
                elif len(corpus[j]) == 0: 
                    pri += rank[j] / len(corpus)
            pr = (1 - damping_factor) / N + damping_factor * pri
            error[i] = abs(rank[i] - pr)
            rank[i] = pr

        loop = False
        for i in corpus:
            if error[i] > 0.0001: 
                loop = True

    rank_sum = 0
    for i in corpus:
        rank_sum += rank[i]
    print(f'Sum Iteration: {round(rank_sum,2)}')

    return rank



if __name__ == "__main__":
    main()
