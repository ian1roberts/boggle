"""Boggle word puzzle solver."""
import tree


class Board(object):
    """Perform word search - Class provides letters for the Board."""

    def __init__(self, xy, grid, wlen, dictionary):
        """Create board."""
        self.ori = xy   # set the initial coordinate for word building
        self.grid = grid
        self.wlen = wlen

        self.dictionary = dictionary

        self._build_tri()
        self.make_words()
        self.filter_valid()

    def _build_tri(self):
        """Construct data structure parent --> child moves."""
        self.tree = tree.Tree(self.ori, self.wlen, self.grid.nrow,
                              self.grid.ncol)

    def make_words(self):
        """Make words."""
        words = {}
        for k, v in self.tree.paths.items():
            letters = [self.grid[x.loc] for x in v]
            words[k] = ''.join(letters)
        self.words = words

    def filter_valid(self):
        """Filter out invalid words."""
        bad_words = []
        for k, v in self.words.items():
            if v.upper() not in self.dictionary:
                bad_words.append(k)

        for bw in bad_words:
            del self.words[bw]
            del self.tree.paths[bw]
