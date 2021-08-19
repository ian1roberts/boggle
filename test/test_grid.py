"""Test building word grid, given strings of letters."""


import unittest
from boggle.grid import Grid


class Test(unittest.TestCase):
    """Define generic testcase for boggle."""

    def test_parse_letters(self):
        """Test string list is parsed."""
        # input
        nrow = 3
        ncol = 3
        letters = "cat dog hog"

        # expected
        expected = [["c", "a", "t"], ["d", "o", "g"], ["h", "o", "g"]]
        observed = Grid(letters, nrow, ncol)

        self.assertListEqual(observed.grid, expected)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
