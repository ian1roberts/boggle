"""Tree module is the main program."""


import datetime
import uuid


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
        self.prune_nodes()

    def __getitem__(self, key):
        """Return item from object."""
        return self.tree[key]

    def _get_valid_moves(self, loc):
        """Compute valid compass points from an x, y location."""
        R, C = loc
        vmoves = []

        for m, (i, j) in self.COMPASS.items():
            next_r = R+i
            next_c = C+j

            if next_r < 0 or next_c < 0:
                continue
            if next_r >= self.grid.nrow or next_c >= self.grid.ncol:
                continue

            vmoves.append(m)

        return vmoves

    def _next_step(self, xy):

        # set orig
        r, c = xy
        steps = {}
        # Get available moves
        moves = self._get_valid_moves((r, c))

        for m in moves:
            _r, _c = self.COMPASS[m]
            steps[m] = (r + _r, c + _c)

        return steps

    def compute_tree(self):
        """Build the tree of word stems."""
        # assign root node, seeds tree
        root_moves = self._next_step(self.ori)
        root_node = Leaves(0, 0, self.ori, root_moves)
        self.tree[0][0] = root_node

        for tier in range(0, self.wlen-1):
            for node in self.tree[tier]:
                parent = self.tree[tier][node]

                for move in parent.moves:
                    loc = parent.moves[move]
                    next_moves = self._next_step(loc)
                    self.tree[tier+1][(parent.loc, move,
                                      str(uuid.uuid4())[:6])] = Leaves(
                                      tier+1, parent, loc, next_moves)

    def build_paths(self):
        """Construct tree paths from nodes."""
        # paths
        pk = self.tree[self.wlen-1].keys()
        self.paths = dict(zip(pk, [[] for _ in pk]))
        # iterate over terminal paths, backtrack chain
        tn = datetime.datetime.now()
        print(tn)
        print("Terminal nodes: {}".format(len(pk)))
        for z, key in enumerate(pk):
            if z % 10000 == 0:
                print("Done {} of {} ({:.2f}%)".format(1+z, len(pk),
                                                       float(1+z)/len(pk)*100))
            cpath = self.paths[key]
            tnode = self.tree[self.wlen-1][key]
            cpath.append(tnode)

            for i in range((self.wlen-2), -1, -1):
                # print('Building path: tier {}'.format(i))
                candidates = self.tree[i]

                for _, v in candidates.items():
                    if v == tnode.parent:
                        cpath.append(v)
                        tnode = v
                        break

        tn = datetime.datetime.now()
        print(tn)
        print("Done {} of {} ({:.2f}%)".format(1+z, len(pk),
                                               float(1+z)/len(pk)*100))

    def build_paths2(self):
        """Optimized path construction."""
        pk = self.tree[self.wlen-1].keys()
        paths = dict(zip(pk, [set() for _ in pk]))

        # step back through parents
        for i in range((self.wlen-1), -1, -1):
            hubs = [(k, n.parents) for k, n in self.tree[i].items()]

    def prune_nodes(self):
        """Remove duplicate paths."""
        bad_path = []
        for k, v in self.paths.items():
            c = set()

            for i in v:
                c.add(i.loc)

            if len(c) < len(v):
                bad_path.append(k)

            self.paths[k] = [z for z in reversed(v)]

        for k in bad_path:
            del self.paths[k]
