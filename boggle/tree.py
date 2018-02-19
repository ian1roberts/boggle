"""Tree module is the main program."""
import networkx as nx


class Tree(object):
    """Instantiate tree class with origin, wordlength number of rows, cols."""

    COMPASS = {'n': (-1, 0), 'ne': (-1, 1), 'e': (0, 1),  'se': (1, 1),
               's': (1, 0),  'sw': (1, -1), 'w': (0, -1), 'nw': (-1, -1)
               }

    def __init__(self, wlen, grid):
        """Instantiate class."""
        self.wlen = wlen
        self.grid = grid
        # {tier3:{p1:[x1y1,x2y2], p2
        self.tree = dict(zip([x for x in range(0, wlen)],
                             [{} for x in range(0, wlen)]))
        # Route through grid
        self.compute_tree()
        self.build_paths_graph()
        self.compute_all_paths()

    @property
    def number_paths(self):
        """Return number of unique terminal nodes, equals number of paths."""
        return (len(set(self.tree[self.wlen-1].keys())))

    def __getitem__(self, key):
        """Return item from object."""
        return self.tree[key]

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

    def compute_tree(self):
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

    def compute_all_paths(self):
        """Compute paths for all origins in grid."""
        all_paths = set()

        for node in self.tree['nodes']:
            _paths = find_paths_in_graph(self.graph, node, self.wlen-1)

            for i in _paths:
                all_paths.add(tuple(i))

        self.paths = all_paths


def find_paths_in_graph(g, u, n):
    """Find all n length paths from u in a graph."""
    if n == 0:
        return [[u]]
    paths = []
    for neighbor in g.neighbors(u):
        for path in find_paths_in_graph(g, neighbor, n-1):
            if u not in path:
                paths.append([u] + path)
    return paths


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "/home/ian/workspace/boggle")

    from boggle.grid import Grid
    import matplotlib.pyplot as plt

    grid = Grid([['c', 'a', 't'],
                 ['d', 'o', 'g'],
                 ['h', 'o', 'g']], 3, 3)

    t = Tree(3, grid)

# Examine Tree graphs
    gcoords = [x for y in grid.coords for x in y]
    ggrid = [x for y in grid.grid for x in y]
    pos = dict((n, n) for n in t.graph.nodes())
    labels = dict(zip(gcoords, ggrid))
    nx.draw_networkx(t.graph, pos=pos, labels=labels, node_size=900)
    plt.savefig('hierarchy.png')
    plt.close()
