"""Test building word paths, given strings of letters."""


import unittest
import multiprocessing
from boggle.grid import Grid
from boggle.moves import Moves
from boggle.paths import do_chains_to_words, do_compute_chains
from boggle.manage import load_dictionary


class Test(unittest.TestCase):
    """Define generic testcase for boggle."""

    grid = Grid("cat dog hog")
    moves = Moves(grid)
    p = multiprocessing.Pool(4)
    xargs = []
    for coord in grid.coords:
        xargs.append((coord, moves, 3))  # maxwlen=3

    board = p.map(do_compute_chains, xargs)
    dictionary = load_dictionary()
    all_words = do_chains_to_words(grid, board, dictionary)

    def test_instantiate_board(self):
        """Test build board for single fixed wlen path."""
        self.assertEquals(len(self.board), 9)

    def test_tlw_00(self):
        """Test all three letter words from 0,0."""
        expect = set(
            [
                "hod",
                "gog",
                "cod",
                "tad",
                "tog",
                "oho",
                "ago",
                "dog",
                "cat",
                "hot",
                "dot",
                "cot",
                "goa",
                "oat",
                "ado",
                "tod",
                "god",
                "got",
                "tag",
                "goo",
                "coo",
                "doc",
                "cog",
                "tao",
                "cad",
                "gad",
                "hog",
                "too",
            ]
        )
        observed = {y[0] for y in self.all_words[3]}

        self.assertSetEqual(expect, observed)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
