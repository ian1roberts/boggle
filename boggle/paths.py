"""Compute all paths in a digraph."""
import networkx as nx


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
