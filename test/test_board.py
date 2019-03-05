"""Test building word paths, given strings of letters."""


import unittest
from boggle.grid import Grid
from boggle.moves import Moves
from boggle.paths import make_digraph, compute_all_paths


class Test(unittest.TestCase):
    """Define generic testcase for boggle."""

    grid = Grid("cat dog hog")
    moves = Moves(grid)
    p3 = Paths(grid, 3)

    def test_instantiate_board(self):
        """Test build board for single fixed wlen path."""
        b = Board(3, Test.p3.grid, Test.p3.dictionary)
        self.assertEquals(len(b.words), 7)

    def test_tlw_00(self):
        """Test all three letter words from 0,0."""
        expect = set(['cat', 'cad', 'cot', 'cod', 'cog', 'coo'])
        b = Board(3, Test.p3.grid, Test.p3.dictionary)

        observed = set(b.words.values())
        self.assertSetEqual(expect, observed)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
