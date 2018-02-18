"""Boggle module."""


from boggle.grid import Grid
from boggle.paths import Paths


def main(args, wlen=0):
    """Launch boggle app with passed arguments.

    Boggle searches a word grid for all words of length `wlen`.
    If `wlen` is 0, then all word sizes from 3 letters to grid length
    are computed.

    If `wlen` is specified, only words of that size are returned.

    It returns a `Paths` object, defining all the solved word paths
    in the grid.

    Args:
        args (['word1', 'word2', '...']): list of bad_words.
        wlen (int): length of result words.

    Example:
        a = main(['cat', 'dog', 'hog'], 3)
        b = main(['cat', 'dog', 'hog'], 0)

    """
    print("Starting ...")
    nrow = len(args)
    ncol = len(args[0])
    x = ' '.join(args)
    g = Grid(x, nrow, ncol)
    p = Paths(g, wlen)

    all_words = set()
    for i in p.paths:
        for k, v in i.words.items():
            all_words.add(v)
    p.all_words = all_words
    print("Finishing ...")
    return(p)


if __name__ == "__main__":
    # import sys
    # sys.path.insert(0, "/home/ian/workspace/boggle")
    a = main(['cat', 'dog', 'hog'], 3)
    print('\n' * 2)
    b = main(['cat', 'dog', 'hog'], 4)
    print('\n' * 2)
    c = main(['sho', 'acw', 'sed'], 0)
