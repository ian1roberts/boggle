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

Modify behaviour with the following command line options:

    --minwordlength ... set the minimum length of found words (default 3)
    --maxwordlength ... set the maximum length of found words (default 9)
    --overwrite     ... recompute board objects and replace existing data file
    --nodisplay     ... do not display found words on screen (False)
    --filename      ... filename of output (boggle_words.tsv)
    --charts        ... export boggle board picture (False)
    --debug         ... return objects when running in python interpreter (False)


Note that the longer the word, the longer the run time, and the bigger the data file

Output
======

Output file displays the found words, alphabetically ordered by length, in three columns.  First column contains the length, second column is the word, and the last column provides the coordinates of the word path.  Coordinates are in XY format::

    Length    Word    path
    3         cat     ((0, 2), (1, 2), (2, 2))

Output file will be written to the directory in which boggle was executed.

Installation
============

Install with pip, github or directly from distributed gzipped tarball.
A requirements file is provided in the archive::

    python setup.py develop
    pip install -e git+https://github.com/ian1roberts/boggle.git
