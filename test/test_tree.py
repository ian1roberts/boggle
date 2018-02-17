"""Test building word trees, given strings of letters."""


import unittest
from boggle.grid import Grid
from boggle.tree import Tree


class Test(unittest.TestCase):
    """Define generic testcase for boggle."""

    grid = Grid([['c', 'a', 't'],
                 ['d', 'o', 'g'],
                 ['h', 'o', 'g']], 3, 3)

    def test_instantiate_tree(self):
        """Test build tree for single fixed board."""
        t = Tree((0, 0), 3, Test.grid)

        print(t)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()