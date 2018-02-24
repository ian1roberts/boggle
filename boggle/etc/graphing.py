##
## From tree.py
##
# from networkx.drawing.nx_agraph import graphviz_layout
# import matplotlib.pyplot as plt
# if __name__ == "__main__":
#     import sys
#     sys.path.insert(0, "/home/ian/workspace/boggle")
#
#     from boggle.grid import Grid
#     import matplotlib.pyplot as plt
#     # d = main(['shop', 'acwe', 'sted', 'fobe'], 0)
#     grid = Grid([['m', 'e', 't', 'e', 't'],
#                  ['e', 'e', 'y', 'm', 'l'],
#                  ['d', 'n', 'r', 'h', 'a'],
#                  ['i', 'e', 'u', 'u', 't'],
#                  ['c', 'i', 'k', 'l', 'p']], 5, 5)
#
#     t = Tree(3, grid)
#
#     # Examine Tree graphs
#     gcoords = [x for y in grid.coords for x in y]
#     ggrid = [x for y in grid.grid for x in y]
#     pos = dict((n, n) for n in t.graph.nodes())
#     labels = dict(zip(gcoords, ggrid))
#     nx.draw_networkx(t.graph, pos=pos, labels=labels, node_size=900)
#     plt.savefig('hierarch1.png')
#     plt.close()

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
