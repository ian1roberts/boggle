"""Boards main module."""
import multiprocessing
from boggle.grid import Grid
from boggle.moves import Moves
from boggle.paths import make_digraph, compute_all_paths
from boggle.manage import (load_dictionary, export_words, display_words,
                           export_board_paths, import_board_paths)

MAX_WLEN = 10
MIN_WLEN = 2


def _do_chains_to_words(grid, all_paths, dictionary):
    """Convert chain of coordinates to words."""
    ori_words = dict()
    for ori, tree, paths in all_paths:
        for path in paths:
            # grid path for word
            chain = [tree.nodes[i]['coord'] for i in path]
            # add words, chains to growing dictionary
            while len(chain) > MIN_WLEN:
                # word from chain
                word = [grid[i] for i in chain]
                word = ''.join(word)
                if "*" not in word and word.upper() in dictionary:
                    wordlen = len(word)
                    if wordlen not in ori_words:
                        ori_words[wordlen] = set()
                    ori_words[wordlen].add((word, tuple(chain)))
                chain.pop()

    return ori_words


def _do_compute_chains(params):
    ori, moves, maxwlen = params
    tree = make_digraph(ori, moves, maxwlen)
    all_paths = []
    for path in compute_all_paths(tree):
        all_paths.append(path)

    return((ori, tree, all_paths))


def main(args):
    """Launch boggle app with passed arguments.

    Boggle searches a word grid for all words of length longer than.
    `minwlen` and shorter than `maxwlen`.

    Maximum allowable wordlength is 10 characters.
    Minimum allowable wordlength is 2 characters.

    Args:
        args (['word1', 'word2', '...']): list of board_words.
        minwlen (int): min length of result words.
        maxwlen (int): max length of result words.
        xdisplay (bool): Suppress printing words to screen (False).
        xfilename (str): boggle output filename (boggle_words.tsv).

    Example:
        a = main(['cat', 'dog', 'hog'], 2, 10)
        b = main(['cat', 'dog', 'hog'], 2, 10)

    """
    # Parse command line args
    minwlen = int(args.minwordlength)
    maxwlen = int(args.maxwordlength)

    # sanity check word lengths
    assert maxwlen >= minwlen, "Max word length less than minimum wordlength."
    assert maxwlen <= MAX_WLEN, "Maximum word length exceeds limit."
    assert minwlen >= MIN_WLEN, "Minimum word length too low."

    # Parse command line arguments
    x = ' '.join(args.words)
    grid = Grid(x)
    # Check if grid moves are known, load them or compute
    board = import_board_paths(grid, maxwlen)
    if board is None:
        # Unknown board, so compute moves, paths and save new board.
        moves = Moves(grid)
        p = multiprocessing.Pool(4)

        xargs = []
        for coord in grid.coords:
            xargs.append((coord, moves, maxwlen))

        board = p.map(_do_compute_chains, xargs)

        # Export the newly computed board_data
        export_board_paths(grid, board, maxwlen, args.overwrite)

    # Parse the results object to form set of all legal words for all origins.
    # Parse dictionary
    dictionary = load_dictionary()
    all_words = _do_chains_to_words(grid, board, dictionary)

    # Export words to a file
    output = export_words(all_words, args.filename)

    # Display words on screen
    if not args.nodisplay:
        display_words(output)

    # Return all objects
    if args.debug:
        return (grid, board, all_words)
