B O G G L E
***********

Welcome to Boggle

Playing the Game
================

Quick start play, simply invoke from command line::

  $ boggle --minwordlength 3 --maxwordlength 9 cat dog hog

This command will find all 3, 4, 5, 6, 7, 8 and 9 letter words that exist within the boggle grid.

Switches
========

Modify behaviour with the following command line options::

  --minwordlength ... set the minimum length of found words (default 3)
  --maxwordlength ... set the maximum length of found words (default 9)
  --nodisplay     ... do not display found words on screen (False)
  --filename      ... filename of output (boggle_words.tsv)

Note that the longer the word, the longer the run time!

Output
======

Output file displays the found words, alphabetically ordered by length, in two columns.  First column contains the word, second column provides the coordinates of the word path.  Coordinates are in RC format.
