from boggle.grid import Grid
from boggle.moves import Moves
from boggle.paths import make_digraph, compute_all_paths

from boggle.bogglem import main, _do_compute


a, b = main(['cat', 'dog', 'hog'], 2, 9)
