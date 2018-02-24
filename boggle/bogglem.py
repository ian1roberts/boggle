"""Boggle module."""
import multiprocessing
from codecs import open
from boggle.grid import Grid
from boggle.moves import Moves
from boggle.paths import make_digraph, compute_all_paths


MAX_WLEN = 10


def _do_compute(params):
    ori, grid, tree, wlen, dictionary = params
    xy_tree = make_digraph(ori, grid, tree, wlen)
    xy_paths = compute_all_paths(xy_tree)

    ori_words = dict()
    for k in xy_paths:
        kw = [xy_tree.nodes[l]['letter'] for l in k]
        while len(kw) > 2:
            i = len(kw)
            if i not in ori_words:
                ori_words[i] = set()
            fw = "".join(kw)
            # rw = fw[::-1]
            if fw.upper() in dictionary:
                ori_words[i].add(fw)
            # if rw.upper() in dictionary:
            #     ori_words[i].add(rw)
            kw.pop()

    ori_data = {'loc': ori, 'tree': xy_tree, 'words': ori_words}
    return(ori_data)


def main(args, wlen, fpath='/usr/share/dict/words'):
    """Launch boggle app with passed arguments.

    Boggle searches a word grid for all words of length `wlen`.
    If `wlen` is 0, then all word sizes from 3 letters to grid length
    are computed.

    If `wlen` is specified, only words of that size are returned.

    It returns a `Paths` object, defining all the solved word paths
    in the grid.

    Args:
        args (['word1', 'word2', '...']): list of board_words.
        wlen (int): length of result words.

    Example:
        a = main(['cat', 'dog', 'hog'], 3)
        b = main(['cat', 'dog', 'hog'], 0)

    """
    # Parse dictionary
    with open(fpath, encoding='utf-8') as f:
        words = f.read().splitlines()
    dictionary = set([x.upper().strip() for x in words])

    # Parse command line arguments
    nrow = len(args)
    ncol = len(args[0])
    x = ' '.join(args)
    grid = Grid(x, nrow, ncol)
    moves = Moves(grid)

    # Word checking
    if wlen == 0 or wlen > MAX_WLEN:
        wlen = MAX_WLEN

    p = multiprocessing.Pool(4)
    all_words = dict()

    xargs = []
    for coord in grid:
        xargs.append((coord, grid, moves, wlen, dictionary))

    board_data = {'grid': grid, 'moves': moves}
    results = p.map(_do_compute, xargs)
    for result in results:
        board_data[result['loc']] = result
        for k, v in result['words'].items():
            if k not in all_words:
                all_words[k] = set()
            all_words[k] = all_words[k].union(v)

    # Return all objects

    return (all_words, board_data)


if __name__ == "__main__":
    # import sys
    # sys.path.insert(0, "/home/ian/workspace/boggle")
    # a = main(['cat', 'dog', 'hog'], 0)
    # print('\n' * 2)
    # b = main(['cat', 'dog', 'hog'], 4)
    # print('\n' * 2)
    c, c_data = main(['sho', 'acw', 'sed'], 0)
    # d = main(['shop', 'acwe', 'sted', 'fobe'], 0)
