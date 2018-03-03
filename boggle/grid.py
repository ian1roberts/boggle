"""Set up grid."""


class Grid(object):
    """Represent the boggle board as a letter grid.

    Args:
        letters ("word1 word2 ..."): a space separated string of words.
        nrow (int): number of rows in boggle grid.
        ncol (int): number of columns in boggle grid.

    Attributes:
        nrow (int): number of rows
        ncol (int): number of columns
        coords ([[(r0, c0), (r0, c1), (r0, c3)],[ ... ]]): grid coordinates
        board (str): string representation of grid
        grid ([['a', 'b', 'c'], [ ... ]]): grid letters

    Example:
        grid = Grid('cat dog hog', 3, 3)

    """

    def __init__(self, letters):
        """Instantiate with letters, number of rows and columns."""
        self.parse_letters(letters)
        self.layout()
        self.search_space()

    def __str__(self):
        """Print representation."""
        txt = ''
        for y in range(self.nrow-1, -1, -1):
            row = self.grid[y]
            a = ''
            for x, l in enumerate(row):
                a += '{}({}) '.format((x, y), self[(x, y)])
            txt += (a + '\n')
        return(txt)

    def __len__(self):
        """Return number of characters in grid."""
        return (len(self._chars))

    def __getitem__(self, key):
        """Return items."""
        x, y = key
        return self.grid[y][x]

    def __iter__(self):
        """Step over letters row by column."""
        for x in range(0, self.ncol):
            for y in range(0, self.nrow):
                yield (x, y)

    def parse_letters(self, letters):
        """Split on space, listify words. Set up (x, y) coords."""
        self._chars = letters.replace(" ", "")
        self.grid = []
        items = letters.split(" ")
        self.nrow = len(items)     # maps to y
        self.ncol = len(items[0])  # maps to x

        for item in reversed(items):
            self.grid.append(list(item))

    def layout(self):
        """Layout the board coordinate system. lower left is (0, 0)."""
        self.coords = [xy for xy in self]
        self.board = dict()
        for x, y in self.coords:
            self.board[(x, y)] = self[(x, y)]

    def search_space(self):
        """Compute search space. Diagnonal matrix."""
        upper_tri = []
        for n in self:
            if n[0] <= n[1]:
                upper_tri.append(n)

        self.upper_tri = upper_tri
