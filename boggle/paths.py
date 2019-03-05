"""Compute all paths in a digraph."""
import networkx as nx
from boggle import MIN_WLEN


def make_digraph(orig, tree, wlen):
    """Make a tree graph from an origin."""
    # initialize tree with root node
    idx = 0

    g = nx.DiGraph()
    g.add_node(idx, tier=0, coord=orig)
    print("ori: {}\ttier: {}\tnode: {}".format(orig, 0, len(g)))
    for tier in range(1, wlen):

        parent_nodes = [(n, d) for n, d in g.nodes(data=True)
                        if d['tier'] == tier-1]

        for pu, pd in parent_nodes:

            children = [cc for (pc, cc) in tree.tree['edges']
                        if pc == pd['coord']]

            while children:
                idx += 1
                child_xy = children.pop()

                g.add_node(idx, tier=tier, coord=child_xy)
                g.add_edge(pu, idx)

                ancest = nx.algorithms.dag.ancestors(g, idx)
                ancest = list(ancest) + [idx]
                if len(ancest) != len(set([g.nodes[x]['coord']
                                           for x in ancest])):
                    g.remove_node(idx)

        print("ori: {}\ttier: {}\tnode: {}".format(orig, tier, len(g)))

    return(g)


def compute_all_paths(gx):
    """Brute force compute all paths by bactracking method."""
    wlen = max([d for _, d in list(gx.nodes.data('tier'))])
    tns = [n for n, d in gx.nodes.data('tier') if d == wlen]

    for n in tns:
        path = list(nx.algorithms.dag.ancestors(gx, n)) + [n]
        yield(sorted(path))


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


def do_compute_chains(params):
    """For a given boggle letter `ori` make the digraph of all_paths.

    From the digraph, compute all_paths through the grid,  up to `MAX_WLEN`
    which equates to all possible words. Note that all_paths
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

    return((ori, tree, all_paths))
