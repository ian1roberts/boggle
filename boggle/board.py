"""Boggle word puzzle solver."""
from boggle.tree import Tree


class Board(object):
    """Perform word search - Class provides letters for the Board."""

    def __init__(self, wlen, grid, dictionary):
        """Create board."""
        self.wlen = wlen
        self.grid = grid
        self.dictionary = dictionary

        self._build_tree()
        self.make_words()
        self.filter_valid()

    def _build_tree(self):
        """Construct data structure parent --> child moves."""
        self.tree = Tree(self.wlen, self.grid)

    def make_words(self):
        """Make words."""
        words = {}
        for path_coords in self.tree.paths:
            letters = [self.grid[x] for x in path_coords]
            words[path_coords] = ''.join(letters)
        self.words = words

    def filter_valid(self):
        """Filter out invalid words."""
        bad_words = []
        for k, v in self.words.items():
            if v.upper() not in self.dictionary:
                bad_words.append(k)

        for bw in bad_words:
            del self.words[bw]

# To do - parse results in Board before rturning
