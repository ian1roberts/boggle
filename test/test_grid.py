'''
Created on 12 Oct 2017

@author: ian
'''
import unittest
import boggle


class Test(unittest.TestCase):

    def test_parse_letters(self):
        ' test string list is parsed'        
        # input
        nrow = 3
        ncol = 3
        letters = 'cat dog hog'
        
        # expected
        expected = [['c', 'a', 't'], ['d', 'o', 'g'], ['h', 'o', 'g']]
        grid = boggle.Grid(letters, nrow, ncol)
        
        self.assertListEqual(grid.grid, expected)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()