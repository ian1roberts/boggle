"""Application wrapper for boggle."""
import argparse
from boggle.bogglem import main

parser = argparse.ArgumentParser(description="Boggle word puzzle solver")
parser.add_argument('-m', '--maxwordlength',
                    help='Maximum wordlength to search for in grid.',
                    default=9)
parser.add_argument('-g', '--graph',
                    help='Plot a graph of the word grid.',
                    action="store_true", default=False)
parser.add_argument('-x', '--nodisplay',
                    help='Suppress displaying found words',
                    action="store_true", default=False)
parser.add_argument('-f', '--filename', help='Output filename',
                    default='boggle_words.tsv', type=str)
parser.add_argument('-w', '--overwrite',
                    help='Overwrite existing grid data.',
                    action="store_true", default=False)
parser.add_argument('-d', '--debug', default=False,
                    help='Run interactive and return main objects.',
                    action="store_true")

parser.add_argument('words', help='Add space separated words', nargs='*')
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s 0.1')

# Should be possible to save the Moves object - no need to recompute
# Come up with solution to save / load grids


def run_boggle():
    """Launch application via this main routine."""
    args = parser.parse_args()
    main(args)
