"""Moves module computes the permissable moves from each node."""
import networkx as nx
import matplotlib.pyplot as plt
from uuid import uuid4


class Moves(object):
    """Make `Moves` class with origin, wordlength number of rows, cols."""

    COMPASS = {'n': (0, 1), 'ne': (1, 1), 'e': (1, 0),  'se': (1, -1),
               's': (0, -1),  'sw': (-1, -1), 'w': (-1, 0), 'nw': (-1, 1)
               }

    def __init__(self, grid):
        """Instantiate class."""
        self.grid = grid

        # Route through grid
        self.compute_moves()
        self.build_paths_graph()

    def _get_valid_moves(self, loc):
        """Compute valid compass points from an x, y location."""
        x, y = loc
        vmoves = []  # valid moves store

        # Iterate over all (8) compass moves and store the
        # the ones that are in range
        for m, (dx, dy) in self.COMPASS.items():
            next_x = x + dx
            next_y = y + dy

            # Check that next row / col position is in range (> 0)
            if next_x < 0 or next_y < 0:
                continue
            # Check that next row / col position is in range (< max)
            if next_x >= self.grid.nrow or next_y >= self.grid.ncol:
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
        x, y = xy

        steps = {}  # store of valid next steps
        # Get available moves
        moves = self._get_valid_moves((x, y))

        for m in moves:
            _x, _y = self.COMPASS[m]
            steps[m] = (x + _x, y + _y)

        return steps

    def compute_moves(self):
        """Build a tree of word stems."""
        # Initiate graph with root node. Index is [tier][next moves]

        self.tree = {'nodes': [x for x in self.grid],
                     'edges': []}
        for node in self.tree['nodes']:
            moves = self._next_step(node)
            for move in moves.values():
                self.tree['edges'].append((node, move))

    def build_paths_graph(self, fn='boggle_board.png'):
        """Optimized path building for improved speed."""
        self.graph = nx.grid_2d_graph(self.grid.nrow, self.grid.ncol)
        self.graph.add_nodes_from(self.tree['nodes'])
        self.graph.add_edges_from(self.tree['edges'])

        pos = dict((n, n) for n in self.graph.nodes())
        nx.draw_networkx(self.graph, pos=pos, labels=self.grid.board,
                         node_size=900)
        plt.savefig("{}_{}".format(str(uuid4())[:6], fn))
        plt.close()
