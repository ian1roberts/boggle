"""Application wrapper for boggle."""


import sys
import argparse
import boggle

parser = argparse.ArgumentParser(description="Boggle word puzzle solver")
parser.add_argument('-l', '--wordlength',
                    help='Number of letters in word to search',
                    required=False, default=3)


def run_boggle(args=None):
    """Launch application via this main routine."""
    if args is None:
        args = sys.argv[1:]

    print("args: {}".format(args))

    boggle.main(args)
