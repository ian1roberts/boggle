"""Build boggle paths."""


from boggle import Board


class Paths(object):
    """This is the Path class."""

    def __init__(self, grid, wlen, mlen=3):
        """Pass in grid and max length of query word."""
        self.grid = grid

        self.maxlen = wlen
        self.minlen = mlen

        self.get_dictionary()
        self.walk_grid()

    def get_dictionary(self, fpath='/usr/share/dict/words'):
        """Build local dictionary of words."""
        with open(fpath) as f:
            words = f.read().splitlines()

        self.dictionary = set([x.upper().strip() for x in words])

    def walk_grid(self):
        """For a fixed word length, walk grid."""
        # grid = original letters
        # wlen = length of word to find
        # x,y are starting coordinates for search

        grids = []
        # for (x,y) in itertools.product(range(self.grid.nrow),
        #                               range(self.grid.ncol)):
        #    grids.append(Board((x,y), self.grid, self.maxlen))

        grids.append(Board((0, 0), self.grid, self.maxlen, self.dictionary))

        self.paths = grids
