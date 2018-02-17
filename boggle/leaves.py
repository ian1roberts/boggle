"""Build Leaves in a grid search."""


class Leaves(object):
    """The Leaves Class."""

    def __init__(self, tier, parent, loc, moves):
        """Instantiate with number of tiers, parents, origin and moves."""
        self.tier = tier
        self.parent = parent
        self.loc = loc
        self.moves = moves

        # record paths that leaf is in
        self.paths = set()

    def __hash__(self):
        """Return hash."""
        return hash((self.tier, self.loc))

    def __str__(self):
        """Return string."""
        return "T:{} P:{} L:{} M:{}".format(self.tier, repr(self.parent),
                                            self.loc, self.moves)

    def __contains__(self, pk):
        """Return membership."""
        return True if pk in self.paths else False

    def __eq__(self, leaf):
        """Return equality."""
        if isinstance(leaf, Leaves):
            return self.parent == leaf.parent and self.loc == leaf.loc

    def __lt__(self, leaf):
        """Return is less than."""
        if isinstance(self, leaf):
            return self.tier < leaf.tier

    @property
    def is_root(self):
        """Set is root node."""
        return True if self.tier == 0 and self.parent == 0 else False

    @property
    def is_valid(self, pk):
        """Set is valid path."""
        return False if pk in self else True
