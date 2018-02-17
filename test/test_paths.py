"""Test building word paths, given strings of letters."""


import unittest
from boggle.grid import Grid
from boggle.paths import Paths


class Test(unittest.TestCase):
    """Define generic testcase for boggle."""

    grid = Grid([['c', 'a', 't'],
                 ['d', 'o', 'g'],
                 ['h', 'o', 'g']], 3, 3)

    def test_instantiate_paths_fixed(self):
        """Test build paths object for fixed wlen."""
        p = Paths(Test.grid, 3)

        self.assertTrue(p.fixed)

    def test_instantiate_paths_flexible(self):
        """Test build paths object for flexible wlen."""
        p = Paths(Test.grid, 0)

        self.assertFalse(p.fixed)

    def test_search_space_fixed(self):
        """Test coordinates in a fixed search space."""
        p = Paths(Test.grid, 3)
        x = [i for i in p.search_space]
        self.assertEquals(len(x), 9)

    def test_search_space_flexible(self):
        """Test coordinates in a flexible search space."""
        p = Paths(Test.grid, 0)
        x = [i for i in p.search_space]
        self.assertEquals(len(x), 63)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
