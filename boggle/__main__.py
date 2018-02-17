"""Application wrapper for boggle."""


import argparse
from boggle.bogglem import main

parser = argparse.ArgumentParser(description="Boggle word puzzle solver")
parser.add_argument('-l', '--wordlength',
                    help='Number of letters in word to search', default=3)
parser.add_argument('words', help='Add space separated words', nargs='*')


def run_boggle():
    """Launch application via this main routine."""
    args = parser.parse_args()
    main(args.words, int(args.wordlength))
