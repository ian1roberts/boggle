"""Build boggle paths."""

import itertools
from multiprocessing import Pool
from boggle.board import Board


class Paths(object):
    """This is the Path class."""

    def __init__(self, grid, wlen, mlen=3):
        """Pass in grid and max length of query word."""
        self.grid = grid

        self.fixed = False
        if wlen > 0:
            self.fixed = True

        self.maxlen = len(grid) + 1  # upper bound for wordlength, not fixed
        self.minlen = mlen
        self.wlen = wlen  # fixed wordlengths only

        self.get_dictionary()
        self.get_search_space()
        self.walk_grid()

    def get_dictionary(self, fpath='/usr/share/dict/words'):
        """Build local dictionary of words."""
        with open(fpath) as f:
            words = f.read().splitlines()

        self.dictionary = set([x.upper().strip() for x in words])

    def get_search_space(self):
        """Build search coordinates and wordlength list.

        If working on a fixed board, then wordlength is fixed.

        Returns:
            search_space (w, (x, y)): x, y start coord, w is wordlength.

        """
        coords = [(i, j) for x in self.grid.coords for (i, j) in x]

        if self.fixed:
            self.search_space = ((self.wlen, xy) for xy in coords)
        else:
            wlenrange = range(self.minlen, self.maxlen)
            self.search_space = itertools.product(wlenrange, coords)

    def walk_grid(self):
        """Compute the boggle paths for a fixed or flexible wordlength."""
        p = Pool(4)

        searches = []
        for w, (x, y) in self.search_space:
            searches.append([(x, y), self.grid, w, self.dictionary])

        results = [p.apply(_do_search, args=(x, )) for x in searches]
        self.paths = []
        for result in results:
            self.paths.append(result)


def _do_search(x):
    xy, grid, wlen, dictionary = x
    return Board(xy, grid, wlen, dictionary)
