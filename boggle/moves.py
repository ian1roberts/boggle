"""Moves module computes the permissable moves from each node."""
import networkx as nx


class Moves(object):
    """Make `Moves` class with origin, wordlength number of rows, cols."""

    COMPASS = {'n': (-1, 0), 'ne': (-1, 1), 'e': (0, 1),  'se': (1, 1),
               's': (1, 0),  'sw': (1, -1), 'w': (0, -1), 'nw': (-1, -1)
               }

    def __init__(self, grid):
        """Instantiate class."""
        self.grid = grid

        # Route through grid
        self.compute_moves()
        self.build_paths_graph()

    def _get_valid_moves(self, loc):
        """Compute valid compass points from an x, y location."""
        R, C = loc
        vmoves = []  # valid moves store

        # Iterate over all (8) compass moves and store the
        # the ones that are in range
        for m, (i, j) in self.COMPASS.items():
            next_r = R+i
            next_c = C+j

            # Check that next row / col position is in range (> 0)
            if next_r < 0 or next_c < 0:
                continue
            # Check that next row / col position is in range (< max)
            if next_r >= self.grid.nrow or next_c >= self.grid.ncol:
                continue

            vmoves.append(m)

        return vmoves

    def _next_step(self, xy):
        """Next steps are a dictionary of destination coordinates.

        Given an origin coordinate, e.g. (0, 0), valid moves will be:
        `{'e': (0, 1), 's': (1, 0), 'se': (1, 1)}`

        Meaning that starting from (0, 0) player can move east, south and
        southeast, with the destination coordinates given.

        """
        # set originating [source] coordinate
        r, c = xy

        steps = {}  # store of valid next steps
        # Get available moves
        moves = self._get_valid_moves((r, c))

        for m in moves:
            _r, _c = self.COMPASS[m]
            steps[m] = (r + _r, c + _c)

        return steps

    def compute_moves(self):
        """Build a tree of word stems."""
        # Initiate graph with root node. Index is [tier][next moves]

        self.tree = {'nodes': set([x for y in self.grid.coords for x in y]),
                     'edges': set()}
        for node in self.tree['nodes']:
            moves = self._next_step(node)
            for move in moves.values():
                self.tree['edges'].add((node, move))

    def build_paths_graph(self):
        """Optimized path building for improved speed."""
        self.graph = nx.grid_2d_graph(self.grid.nrow, self.grid.ncol)
        self.graph.add_nodes_from(self.tree['nodes'])
        self.graph.add_edges_from(self.tree['edges'])
