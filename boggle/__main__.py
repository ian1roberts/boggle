"""Application wrapper for boggle."""
import argparse
from boggle.bogglem import main

parser = argparse.ArgumentParser(description="Boggle word puzzle solver")
parser.add_argument('-m', '--maxwordlength',
                    help='Maximum wordlength to search for in grid.',
                    default=9)
parser.add_argument('-n', '--minwordlength',
                    help='Minimum wordlength to search for in grid.',
                    default=3)
parser.add_argument('words', help='Add space separated words', nargs='*')

# Should be possible to save the Moves object - no need to recompute
# Come up with solution to save / load grids


def run_boggle():
    """Launch application via this main routine."""
    args = parser.parse_args()
    main(args.words, int(args.minwordlength), int(args.maxwordlength))
