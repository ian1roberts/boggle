from boggle.grid import Grid
from boggle.moves import Moves
from boggle.paths import make_digraph, compute_all_paths

from boggle.bogglem import main

"""
boggle cat dog hog
"""

class Args(object):
    words = ['cat', 'dog', 'hog']
    maxwordlength = 9
    nodisplay = False
    graph = True
    filename = "boggle_words.tsv"
    debug = True
    overwrite = True


args = Args()

g, b, a = main(args)
