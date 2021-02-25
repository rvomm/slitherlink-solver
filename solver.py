from Board import Board

if __name__ == "__main__":
    table = [[None, None, 3, 2],
             [None, 0, None, None],
             [3, 3, None, 2],
             [None, None, 2, 2]]
    _board = Board(table)
    for edge in _board.edges:
        source = edge.source.pos()
        dest = edge.dest.pos()
        if source[0] % 3 == 0 and dest[1] % 3 == 2:
            edge.make()
    _board.print()

    print("___________________________________")

    new_unknonw_count = _board.unknonw_edge_count()
    old_unknown_count = new_unknonw_count + 1
    while new_unknonw_count < old_unknown_count:
        old_unknown_count = new_unknonw_count
        for cross in _board.structures:
            cross.update()
        new_unknown_count = _board.unknonw_edge_count()
    # _board.structures[2].update()
    _board.print()


    