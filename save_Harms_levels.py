levels = [[[None, None, 3, 2], [None, 0, None, None], [3, 3, None, 2], [None, None, 2, 2]], [[2, None, 1, 1, None, 2, None], [None, 3, None, None, 1, None, 1], [3, 2, None, None, None, None, None], [None, 1, 2, 2, 1, 2, None], [3, 2, None, 2, 1, None, 2], [None, None, 2, None, 1, 2, 3], [3, 2, None, None, 2, 2, None]], [[None, 3, 1, None, None, None, 3], [None, 3, None, None, 2, 2, None], [3, None, 1, 2, 1, 0, 3], [None, None, None, None, None, None, None], [None, None, None, 2, None, None, 3], [None, None, 2, 3, None, 3, None], [3, None, 3, None, 2, 2, None]]]

def _print(table):
    for row in table:
        line = ""
        for el in row:
            if el is None:
                line+="."
            else:
                line+=str(el)
        print(line)

_print(levels[2])