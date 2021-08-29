"""Boggle main module. Responsible for executing a game session."""
import multiprocessing
from boggle.grid import Grid
from boggle.moves import Moves
from boggle.manage import (
    load_dictionary,
    export_words,
    display_words,
    export_board_paths,
    import_board_paths,
)
from boggle.paths import (
    do_compute_chains,
    do_chains_to_words
)

MAX_WLEN = 10
MIN_WLEN = 2



def main(args):
    """Execute boggle app with passed arguments.

    Boggle searches a word grid for all words of length longer than.
    `minwlen` and shorter than `maxwlen`.

    Maximum allowable wordlength is 10 characters.
    Minimum allowable wordlength is 2 characters.

    Args:
        args (['word1', 'word2', '...']): list of board_words.
        maxwlen (int): max length of result words.
        nodisplay (bool): Suppress printing words to screen (False).
        filename (str): boggle output filename (boggle_words.tsv).
        graph (bool): plot boogle chart
        overwrite (bool): Force recomputing and overwriting boggle boards.
        debug (bool): If true, return objects in interactive shell session.

    Example:
        a = main(['cat', 'dog', 'hog'], 10)
        b = main(['cat', 'dog', 'hog'], 10)

    """
    # Parse command line args
    maxwlen = int(args.maxwordlength)

    # sanity check word lengths
    assert maxwlen > MIN_WLEN, "Max word length less than minimum wordlength."
    assert maxwlen <= MAX_WLEN, "Maximum word length exceeds limit."

    # Parse command line arguments
    x = " ".join(args.words)
    grid = Grid(x)
    moves = Moves(grid)
    # Check if grid moves are known, load them or compute
    board = import_board_paths(grid, maxwlen)
    if board is None or args.overwrite:
        # Unknown board, so compute moves, paths and save new board.
        # Or force recompute
        p = multiprocessing.Pool(4)
        xargs = []
        for coord in grid.coords:
            xargs.append((coord, moves, maxwlen))

        board = p.map(do_compute_chains, xargs)

        # Export the newly computed board_data
        export_board_paths(grid, board, maxwlen, args.overwrite)

    # Parse the results object to form set of all legal words for all origins.
    # Parse dictionary
    dictionary = load_dictionary(args.dictionary)
    all_words = do_chains_to_words(grid, board, dictionary)

    # Export words to a file
    output = export_words(all_words, args.filename)

    # Display words on screen
    if not args.nodisplay:
        display_words(output)

    # Draw boogle board if requested
    if args.graph:
        fn = args.filename.replace(".tsv", "_board.png")
        moves.grid = grid
        moves.draw_board(fn)

    # Return all objects
    if args.debug:
        return (grid, board, all_words)
