boggle
******

Playing the Game
================

Quick start play, simply invoke from command line::

    $ boggle --minwordlength 3 --maxwordlength 9 cat dog hog

This command will find all 3, 4, 5, 6, 7, 8 and 9 letter words that exist within the boggle grid.

Logic
=====

The objective of boggle is to find all words in the grid of 3 or more characters in length. Words can be made from adjacent characters only, and letters may not be reused in a word.  For example:

.. table:: Boggle Grid. Coordinates are XY, such that C: (0, 2)

   +---+---+---+---+---+
   |   | 2 | C | A | T |
   +---+---+---+---+---+
   | Y | 1 | D | O | G |
   +---+---+---+---+---+
   |   | 0 | H | O | G |
   +---+---+---+---+---+
   |   |   | 0 | 1 | 2 |
   +---+---+---+---+---+
   |   |   |   | X |   |
   +---+---+---+---+---+

Table
