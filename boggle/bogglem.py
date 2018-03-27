"""Boggle module."""
import multiprocessing
from codecs import open
from boggle.grid import Grid
from boggle.moves import Moves
from boggle.paths import make_digraph, compute_all_paths


MAX_WLEN = 10
MIN_WLEN = 2


def _do_compute(params):
    ori, jd = params
    xy_tree = make_digraph(ori, jd["grid"], jd["moves"], jd["maxwlen"])
    xy_paths = compute_all_paths(xy_tree)

    ori_words = dict()
    for k in xy_paths:
        path_key = tuple(k)       # path_keys are ordered lists of node indexes
        ori_words[path_key] = {}  # words by length under Longest Path Key

        kw = [xy_tree.nodes[l]['letter'] for l in k]
        while len(kw) > jd["minwlen"]:
            i = len(kw)
            if i not in ori_words:
                ori_words[path_key][i] = set()
            fw = "".join(kw)

            if "*" not in fw and fw.upper() in jd["dictionary"]:
                ori_words[path_key][i].add(fw)

            kw.pop()

        if len(ori_words[path_key]) < 1:
            del ori_words[path_key]

    return((ori, ori_words, xy_tree))


def main(args, minwlen, maxwlen, fpath='/usr/share/dict/words'):
    """Launch boggle app with passed arguments.

    Boggle searches a word grid for all words of length longer than.
    `minwlen` and shorter than `maxwlen`.

    Maximum allowable wordlength is 10 characters.
    Minimum allowable wordlength is 2 characters.

    Args:
        args (['word1', 'word2', '...']): list of board_words.
        minwlen (int): min length of result words.
        maxwlen (int): max length of result words.

    Example:
        a = main(['cat', 'dog', 'hog'], 2, 10)
        b = main(['cat', 'dog', 'hog'], 2, 10)

    """
    # Parse dictionary
    with open(fpath, encoding='utf-8') as f:
        words = f.read().splitlines()
    dictionary = set([x.upper().strip() for x in words])

    # Parse command line arguments
    x = ' '.join(args)
    grid = Grid(x)
    moves = Moves(grid)

    # Word length checking
    assert maxwlen > minwlen, "Max word length less than minimum wordlength."
    assert maxwlen < MAX_WLEN, "Maximum word length exceeds limit."
    assert minwlen > MIN_WLEN, "Minimum word length too low."

    p = multiprocessing.Pool(4)
    all_words = dict()
    xargs = []
    job_data = {"grid": grid, "moves": moves, "dictionary": dictionary,
                "maxwlen": maxwlen, "minwlen": minwlen}
    for coord in grid.coords:
        xargs.append((coord, job_data))

    results = p.map(_do_compute, xargs)

    # Parse the results object to form set of all legal words for all origins.
    boards = {}
    for locus, words, tree in results:
        boards[locus] = tree
        for path_key, wordlens in words.items():
            for k, word in wordlens.items():
                if k not in all_words:
                    all_words[k] = set()
                all_words[k] = all_words[k].union(word)

    # Return all objects
    return((all_words, boards))
