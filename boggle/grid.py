"""Set up grid."""

class Grid(object):
    """Setup the word grid coordinates."""

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

    def __getitem__(self, key):
        """Return items."""
        r, c = key
        return self.grid[r][c]

    def parse_letters(self, letters):
        """Split on space, listify."""
        self.grid = []
        if not isinstance(letters, list):
            items = letters.split(' ')
        else:
            items = letters

        for item in items:
            self.grid.append(list(item))

    def layout(self):
        """Set out grid."""
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
        """Drawer the grid."""
        grid = ''
        for i in self.grid:
            row = ''.join(i) + '\n'
            grid += row

        self.board = grid
