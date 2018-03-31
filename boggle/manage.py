"""Manage loading and saving boggle boards."""
import pickle
import csv
from os import path as op
from codecs import open as copen

DICT_PATH = "/usr/share/dict/words"


def load_dictionary(fpath=DICT_PATH):
    """Load the system word list."""
    with copen(fpath, encoding='utf-8') as f:
        words = f.read().splitlines()
    return(set([x.upper().strip() for x in words]))


def export_words(all_words, fname):
    """Write to file boggle board words."""
    output = []
    for wlen, words in all_words.items():
        for word, chain in words:
            output.append({'length': wlen, 'word': word, 'path': chain})

    output.sort(key=lambda x: (x['length'], x['word']))
    fhandle = csv.DictWriter(open(fname, mode='w'),
                             fieldnames=["length", "word", "path"])
    fhandle.writeheader()
    fhandle.writerows(output)

    return output


def display_words(words):
    """Print boggle words to screen."""
    print("{}\t{}\t{}".format("WLEN", "WORD", "PATH"))
    print("="*80)
    for line in words:
        print("{}\t{}\t{}".format(line['length'], line['word'], line['path']))


def _get_board_data_dir():
    """Return the directory for storing board data."""
    x = op.dirname(op.abspath(__file__))
    x = op.abspath(op.join(x, 'data'))
    return x


def export_board_paths(grid, board_data, maxwlen, ow=False):
    """Save all board moves."""
    fname = "{}x{}-{}-board.pkl".format(grid.nrow, grid.ncol, maxwlen)
    fname = op.join(_get_board_data_dir(), fname)
    print("Export path: {}".format(fname))

    if op.exists(fname) and ow is False:
        return
    with open(fname, 'wb') as output:
        pickle.dump(board_data, output, pickle.HIGHEST_PROTOCOL)


def import_board_paths(grid, maxwlen):
    """Load all board moves."""
    fname = "{}x{}-{}-board.pkl".format(grid.nrow, grid.ncol, maxwlen)
    fname = op.join(_get_board_data_dir(), fname)

    if op.exists(fname):
        with open(fname, 'rb') as input:
            board_data = pickle.load(input)
        return (board_data)

    return None
