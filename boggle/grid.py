"""Set up grid."""


class Grid(object):
    """Represent the boggle board as a letter grid.

    The boggle board is represented as an XY coordinate space. Where bottom
    left hand corner is (0, 0).  The `Grid` maps letters to coordinates.

    Args:
        letters ("word1 word2 ..."): a space separated string of words..

    Attributes:
        nrow (int): number of rows
        ncol (int): number of columns
        coords ([[(x0, y0), (x0, y1), (x0, y2)],[ ... ]]): grid coordinates
        board (str): string representation of grid
        grid ([['a', 'b', 'c'], [ ... ]]): grid letters

    Example:
        grid = Grid('cat dog hog')

    """

    def __init__(self, letters):
        """Instantiate with letters, number of rows and columns."""
        self.parse_letters(letters)
        self.layout()

    def __str__(self):
        """Print letter board in coordinate space."""
        txt = ""
        for y in range(self.nrow - 1, -1, -1):
            row = self.grid[y]
            a = ""
            for x, l in enumerate(row):
                a += "{}({}) ".format((x, y), self[(x, y)])
            txt += a + "\n"
        return txt

    def __len__(self):
        """Return number of characters in grid."""
        return len(self._chars)

    def __getitem__(self, key):
        """Return letter item given (x, y) coordinate."""
        x, y = key
        return self.grid[y][x]

    def __iter__(self):
        """Step over letters row(y) by column(x)."""
        for x in range(0, self.ncol):
            for y in range(0, self.nrow):
                yield (x, y)

    def parse_letters(self, letters):
        """Split on space, listify words. Set up (x, y) coords.

        Grid is held as a list of lists. Number of rows (y) is the number of
        space separated words input. Number of columns (x) is the number of
        letters in first word. Note there is no check that all columns have
        same number of letters.

        """
        self._chars = letters.replace(" ", "")
        self.grid = []
        items = letters.split(" ")
        self.nrow = len(items)  # maps to y
        self.ncol = len(items[0])  # maps to x

        for item in reversed(items):
            self.grid.append(list(item))

    def layout(self):
        """Layout the board coordinate system. lower left is (0, 0)."""
        self.coords = [xy for xy in self]
        self.board = dict()
        for x, y in self.coords:
            self.board[(x, y)] = self[(x, y)]
