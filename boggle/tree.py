"""Tree module is the main program."""
import uuid
import networkx as nx
from boggle.leaves import Leaves


class Tree(object):
    """Instantiate tree class with origin, wordlength number of rows, cols."""

    COMPASS = {'n': (-1, 0), 'ne': (-1, 1), 'e': (0, 1),  'se': (1, 1),
               's': (1, 0),  'sw': (1, -1), 'w': (0, -1), 'nw': (-1, -1)
               }

    def __init__(self, ori, wlen, grid):
        """Instantiate class."""
        self.ori = ori
        self.wlen = wlen
        self.grid = grid
        # {tier3:{p1:[x1y1,x2y2], p2
        self.tree = dict(zip([x for x in range(0, wlen)],
                             [{} for x in range(0, wlen)]))
        # Route through grid
        self.compute_tree()
        self.build_paths()

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
        """Build a tree of word stems.

        Trees are constructed using tier and leaf indexes. Tiers match the
        letter position within the growing word, and leaves are the valid
        characters at each tier position.

        Tree.tree[tier][leaf]

        Tiers are letter indexes
        Leaf nodes are `Leaves` objects of parent and child node relationships.
        Leaves are indexed: Parent.Location, Move made, UUID

        To compute the complete word graph, start from root node, and descend
        to terminal nodes, computing valid character positions at each tier.

        Leaves are lists of nodes at each tier position. To enable path
        construction Leaves record parent and child relationships.

        Note that no filtering is applied in constructing the graph. Hence,
        backtracking of characters is allowed.

        """
        # assign root node, seeds tree from letter in grid that all words will
        # be computed.
        root_moves = self._next_step(self.ori)  # compute moves from root node.
        root_node = Leaves(0, 0, self.ori, root_moves)  # No parent leaf node.

        # Tree.tree atrribute stores the word graph of moves through the grid.
        # Initiate graph with root node. Index is [tier][Leaf]
        self.tree[0][0] = root_node

        # Iterate over remaining tiers, computing Leaves at each level.
        for tier in range(0, self.wlen-1):
            for node in self.tree[tier]:
                parent = self.tree[tier][node]

                # One Leaf per available move from Parent.
                for move in parent.moves:
                    loc = parent.moves[move]
                    next_moves = self._next_step(loc)  # These are child moves

                    # Leaves need a UUID to avoid stomping.
                    node_uuid = str(uuid.uuid4())[:6]
                    self.tree[tier+1][(parent.loc, move, node_uuid)] = Leaves(
                                      tier+1, parent, loc, next_moves)

    def build_paths(self):
        """Optimized path building for improved speed."""
        key_list = [list(self.tree[x].keys()) for x in range(1, self.wlen)]

        path_dict = {self.ori: set()}
        for keys in key_list:
            for key in keys:
                src = key[0]
                move = key[1]
                _r, _c = self.COMPASS[move]
                dest = (src[0] + _r, src[1] + _c)
                if src in path_dict:
                    path_dict[src].add(dest)
                else:
                    path_dict[src] = set()
                    path_dict[src].add(dest)

        # Compute a set of Nodes
        node_set = set()
        for k, v in path_dict.items():
            node_set.add(k)
            [node_set.add(_v) for _v in v]

        # Compute set of paths bewteen nodes
        path_set = set()
        for k, v in path_dict.items():
            for _v in v:
                path_set.add((k, _v))

        G = nx.Graph()
        G.add_nodes_from(node_set)
        G.add_edges_from(path_set)

        _paths = find_paths_in_graph(G, self.ori, self.wlen-1)
        paths = set()
        for i in _paths:
            paths.add(tuple(i))

        self.paths = paths
        self.graph = G


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

    t = Tree((0, 0), 3, grid)

# Examine Tree graphs
    pos = nx.spring_layout(t.graph)
    nx.draw_networkx_nodes(t.graph, pos, node_size=900)
    nx.draw_networkx_labels(t.graph, pos, font_size=8)
    nx.draw_networkx_edges(t.graph, pos, arrows=True)
    plt.savefig('hierarchy.png')
    plt.close()
