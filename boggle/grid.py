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

    def __init__(self, letters, nrow, ncol):
        """Instantiate with letters, number of rows and columns."""
        self.nrow = nrow
        self.ncol = ncol

        # populate the grid
        self.parse_letters(letters)
        # r,c coordinated grid
        self.layout()
        self.draw()

    def __str__(self):
        """Print representation."""
        x = ''
        for i in range(0, self.nrow):
            for j in range(0, self.ncol):
                x += '(%s, %s) ' % (str(i), str(j))
            x += '\n'

        return x

    def __len__(self):
        """Return number of characters in grid."""
        return (len(self.board)-self.nrow)

    def __getitem__(self, key):
        """Return items."""
        r, c = key
        return self.grid[r][c]

    def parse_letters(self, letters):
        """Split on space, listify words."""
        self.grid = []
        if not isinstance(letters, list):
            items = letters.split(' ')
        else:
            items = letters

        for item in items:
            self.grid.append(list(item))

    def layout(self):
        """Layout the board coordinate system. Upper left is (0, 0)."""
        coords = []
        for i in range(0, self.nrow):
            for j in range(0, self.ncol):
                coords.append((i, j))

        self.coords = []
        while coords:
            stack = []
            for i in range(self.nrow):
                stack.append(coords.pop(0))
            self.coords.append(stack)

    def draw(self):
        """Draw the board in words."""
        grid = ''
        for i in self.grid:
            row = ''.join(i) + '\n'
            grid += row

        self.board = grid
