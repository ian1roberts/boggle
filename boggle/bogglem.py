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
from boggle.paths import make_digraph, compute_all_paths


MAX_WLEN = 10
MIN_WLEN = 2


def do_chains_to_words(grid, all_paths, dictionary):
    """Convert chains of letter coordinates to words.

    Words are computed for each letter orgin, using the digraph `tree` of all
    moves from origin. The tree nodes have `coordinate` attributes, and the
    tree paths are node chains.  To compute a word, it is necessary to convert
    the node chains to coordinate chains, then via the `Grid` object, Convert
    coordinate chains to letters.  Only words in dictionary are permissible.

    Words are computed from `MAX_WLEN` to `MIN_WLEN` in a loop, dropping
    a node (coordinate) at each cycle.  Note that `*` is used to signify a
    blocked tile.

    Arguments:
        grid (Grid) Representation of a boggle board.
        all_paths (list) Word chains in boggle board coordinate space.
        dictionary (set) Set of known words from unix dictionary.

    Returns:
        ori_words (dict) set of all found words indexed by word length.

    """
    ori_words = dict()
    for ori, tree, paths in all_paths:
        for path in paths:
            # grid path for word
            chain = [tree.nodes[i]["coord"] for i in path]
            # add words, chains to growing dictionary
            while len(chain) > MIN_WLEN:
                # word from chain
                word = [grid[i] for i in chain]
                word = "".join(word)
                if "*" not in word and word.upper() in dictionary:
                    wordlen = len(word)
                    if wordlen not in ori_words:
                        ori_words[wordlen] = set()
                    ori_words[wordlen].add((word, tuple(chain)))
                chain.pop()

    return ori_words


def do_compute_chains(params):
    """For a given boggle letter `ori` make the digraph of all_paths.

    From the digraph, compute all_paths through the grid, up to `MAX_WLEN`.
    through the grid, which equates to all possible words. Note that all_paths
    are chains of nodes through the digraph, not letter coordinates.

    This function is run asynchronously, in parallel. Passing `ori` back makes
    it easier to work out which cell of the boggle grid is being processed.

    Arguments:
        params (tuple) Origin coordinate letter, valid moves, maxwordlength.

    Returns:
        ori (tuple) Origin coordinate letter.
        tree (DiGraph) Graph of all paths through boggle grid from `ori`.
        all_paths (list) List of node chains up to `MAX_WLEN`.

    """
    ori, moves, maxwlen = params
    tree = make_digraph(ori, moves, maxwlen)
    all_paths = []
    for path in compute_all_paths(tree):
        all_paths.append(path)

    return (ori, tree, all_paths)


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
