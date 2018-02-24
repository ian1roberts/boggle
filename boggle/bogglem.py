"""Boggle module."""
import multiprocessing
from codecs import open
from boggle.grid import Grid
from boggle.moves import Moves
from boggle.paths import make_digraph, compute_all_paths


MAX_WLEN = 10


def _do_compute(params):
    ori, grid, moves, wlen, dictionary = params
    xy_tree = make_digraph(ori, grid, moves, wlen)
    xy_paths = compute_all_paths(xy_tree)

    ori_words = dict()
    for k in xy_paths:
        kw = [xy_tree.nodes[l]['letter'] for l in k]
        while len(kw) > 2:
            i = len(kw)
            if i not in ori_words:
                ori_words[i] = set()
            fw = "".join(kw)
            rw = fw[::-1]
            if fw.upper() in dictionary:
                ori_words[i].add(fw)
            if rw.upper() in dictionary:
                ori_words[i].add(rw)
            kw.pop()

    return(ori_words)


def main(args, wlen, fpath='/usr/share/dict/words'):
    """Launch boggle app with passed arguments.

    Boggle searches a word grid for all words of length `wlen`.
    If `wlen` is 0, then all word sizes from 3 letters to grid length
    are computed.

    If `wlen` is specified, only words up to that size are returned.

    Args:
        args (['word1', 'word2', '...']): list of board_words.
        wlen (int): max length of result words.

    Example:
        a = main(['cat', 'dog', 'hog'], 3)
        b = main(['cat', 'dog', 'hog'], 0)

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
    if wlen == 0 or wlen > MAX_WLEN:
        wlen = MAX_WLEN

    p = multiprocessing.Pool(4)
    all_words = dict()
    xargs = []
    for coord in grid.upper_tri:
        xargs.append((coord, grid, moves, wlen, dictionary))

    results = p.map(_do_compute, xargs)
    for result in results:
        for k, v in result.items():
            if k not in all_words:
                all_words[k] = set()
            all_words[k] = all_words[k].union(v)

    # Return all objects
    return(all_words)


if __name__ == "__main__":
    a = main(['cat', 'dog', 'hog'], 0)
    # print('\n' * 2)
    # b = main(['cat', 'dog', 'hog'], 4)
    # print('\n' * 2)
    c = main(['sho', 'acw', 'sed'], 0)
    # d = main(['shop', 'acwe', 'sted', 'fobe'], 0)
