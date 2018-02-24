"""Random thoughts on DiGraphs."""
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
from uuid import uuid4


def make_digraph(orig, grid, tree, wlen=3, dedup=True):
    """Make a tree graph from an origin."""
    # initialize tree with root node
    idx = 0

    g = nx.DiGraph()
    g.add_node(idx, tier=0, coord=orig, letter=grid[orig])
    print("tier: {}\tnode: {}".format(0, len(g)))
    for tier in range(1, wlen):

        parent_nodes = [(n, d) for n, d in g.nodes(data=True)
                        if d['tier'] == tier-1]

        for pu, pd in parent_nodes:

            children = [cc for (pc, cc) in tree.tree['edges']
                        if pc == pd['coord']]

            while children:
                idx += 1
                child_xy = children.pop()
                g.add_node(idx, tier=tier, coord=child_xy,
                           letter=grid[child_xy])
                g.add_edge(pu, idx)

            # Check uniqueness of child nodes in paths.
            if dedup:
                for i in compute_all_paths(g):
                    if len(i) != len(set([g.nodes[x]['coord'] for x in i])):
                        g.remove_node(i[-1])

        print("tier: {}\tnode: {}".format(tier, len(g)))

    return(g)


def compute_all_paths(gx):
    """Brute force compute all paths by bactracking method."""
    wlen = list(set([d['tier'] for (_, d) in gx.nodes(data=True)]))[-1]
    tns = [n for n, d in gx.nodes(data=True) if d['tier'] == wlen]

    for n in tns:
        path = []
        q = n
        for i in range(wlen):
            for j in gx.predecessors(q):
                path.insert(0, j)
            q = j
        path.append(n)
        yield(path)

# def opt_path_calculation(g, wlen):
#     """Optimized all paths calculation."""
#     all_paths = []
#     source = [n for (n, d) in g.nodes(data=True) if d['tier'] == 0]
#     term_nodes = [n for (n, d) in g.nodes(data=True) if d['tier'] == wlen]
#     for sink in term_nodes:
#         for path in nx.shortest_simple_paths(g, source=source, target=sink):
#             all_paths.append(path)
#     return all_paths




if __name__ == "__main__":
    import sys
    sys.path.insert(0, "/home/ian/workspace/boggle")
    from boggle.grid import Grid
    from boggle.tree import Tree

    # (row, col)
    grid = Grid([['m', 'x', 't', 'e', 't'],
                 ['y', 'z', 'y', 'm', 'l'],
                 ['d', 'n', 'r', 'h', 'a'],
                 ['i', 'e', 'u', 'u', 't'],
                 ['c', 'i', 'k', 'l', 'p']], 5, 5)

    # standard tree
    t = Tree(3, grid)

    # build dag
    g = make_digraph((0, 0), grid, t, wlen=4)
    # h = make_digraph((0, 0), grid, t, wlen=10, dedup=False)
    zz = compute_all_paths(g)
    # yy = compute_all_paths(h)
    #
    labels = {}
    for n in g.nodes():
        labels[n] = "{}\n{}".format(g.nodes[n]['coord'], g.nodes[n]['letter'])

    plt.title('draw_g_networkx')
    pos = graphviz_layout(g, prog='dot')
    #nx.draw_networkx_labels(g, pos=pos, labels=labels, font_size=6)
    nx.draw(g, pos=pos, with_labels=True, arrows=True, node_size=350, font_size=6)
    plt.savefig('nx_g_test.png')
    plt.close()
    #
    # labels = {}
    # for n in h.nodes():
    #     labels[n] = "{}\n{}".format(h.nodes[n]['coord'], h.nodes[n]['letter'])
    #
    # plt.title('draw_h_networkx')
    # pos = graphviz_layout(h, prog='dot')
    # nx.draw_networkx_labels(h, pos=pos, labels=labels, font_size=6)
    # nx.draw(h, pos=pos, with_labels=False, arrows=True, node_size=500)
    # plt.savefig('nx_h_test.png')
    # plt.close()
