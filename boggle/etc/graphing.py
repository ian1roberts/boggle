##
## From tree.py
##
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt

# Examine moves graphs
pos = dict((n, n) for n in moves.graph.nodes())
nx.draw_networkx(moves.graph, pos=pos, labels=grid.board, node_size=900)
plt.savefig("hierarch1.png")
plt.close()

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from networkx.drawing.nx_agraph import graphviz_layout
    from boggle.grid import Grid
    from boggle.moves import Moves

    grid = Grid("sho acw sed")
    moves = Moves(grid)

    xy_tree = make_digraph((0, 2), grid, moves, 9)
    z = compute_all_paths(xy_tree)
    # labels = {}
    # for n in xy_tree.nodes():
    #     labels[n] = "{}".format(xy_tree.nodes[n]['letter'])
    #
    # plt.title('draw_g_networkx')
    # pos = graphviz_layout(xy_tree, prog='dot')
    # nx.draw_networkx_labels(xy_tree, pos=pos, labels=labels, font_size=6)
    # nx.draw(xy_tree, pos=pos, with_labels=False, arrows=True,
    #         node_size=350, font_size=6)
    # plt.savefig('nx_g_test.png')
    # plt.close()


##
## From script.py
##

# if __name__ == "__main__":
#     import sys
#     sys.path.insert(0, "/home/ian/workspace/boggle")
#     from boggle.grid import Grid
#     from boggle.tree import Tree
#
#     # (row, col)
#     grid = Grid([['m', 'x', 't', 'e', 't'],
#                  ['y', 'z', 'y', 'm', 'l'],
#                  ['d', 'n', 'r', 'h', 'a'],
#                  ['i', 'e', 'u', 'u', 't'],
#                  ['c', 'i', 'k', 'l', 'p']], 5, 5)
#
#     # standard tree
#     t = Tree(3, grid)
#     words = main(grid, t)
#
#     # build dag
#     # g = make_digraph((0, 0), grid, t, wlen=5)
#     # zz = compute_all_paths(g)
#     #
#     # labels = {}
#     # for n in g.nodes():
#     #     labels[n] = "{}\n{}".format(g.nodes[n]['coord'],
#     #                                 g.nodes[n]['letter'])
#     #
#     # plt.title('draw_g_networkx')
#     # pos = graphviz_layout(g, prog='dot')
#     # # nx.draw_networkx_labels(g, pos=pos, labels=labels, font_size=6)
#     # nx.draw(g, pos=pos, with_labels=True, arrows=True,
#     #         node_size=350, font_size=6)
#     # plt.savefig('nx_g_test.png')
#     # plt.close()

# Draw paths from filtered origins
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt

tree = c_data[(0, 2)]
plt.title("(0, 2) sho acw sed --> showcased")
pos = graphviz_layout(tree, prog="dot")
nx.draw(tree, pos=pos, with_labels=True, arrows=True, node_size=350, font_size=6)
plt.savefig("nx_filt_origin.png")
plt.close()
