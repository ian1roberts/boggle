"""Boggle module."""
import grid
import paths


def main(args, wlen):
    """Launch boggle app with passed arguments."""
    nrow = len(args)
    ncol = len(args[0])
    x = ' '.join(args)
    g = grid.Grid(x, nrow, ncol)
    p = paths.Paths(g, wlen)

    b = p.paths[0]
    print(b)
    return b


if __name__ == "__main__":
    a = main(['cat', 'dog', 'hog'], 3)
    print('\n' * 2)
    b = main(['cat', 'dog', 'hog'], 4)
    print('\n' * 2)
    # c = main(['sho', 'acw', 'sed'], 9)
