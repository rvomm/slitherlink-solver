from Board import Board

if __name__ == "__main__":
    # table = [[None, None, 3, 2],
    #          [None, 0, None, None],
    #          [3, 3, None, 2],
    #          [None, None, 2, 2]]
    table = [[2, None, 1, 1, None, 2, None],
             [None, 3, None, None, 1, None, 1],
             [3, 2, None, None, None, None, None],
             [None, 1, 2, 2, 1, 2, None],
             [3, 2, None, 2, 1, None, 2],
             [None, None, 2, None, 1, 2, 3],
             [3, 2, None, None, 2, 2, None]]

    _board = Board(table)
    _board.print()

    print("___________________________________")

    new_unknown_count = _board.unknonw_edge_count()
    old_unknown_count = new_unknown_count + 1
    while new_unknown_count < old_unknown_count:
        old_unknown_count = new_unknown_count
        _board.solve_iteration()
        new_unknown_count = _board.unknonw_edge_count()
    _board.print()


    