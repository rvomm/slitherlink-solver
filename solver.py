from Board import Board

if __name__ == "__main__":
    table = [[None, None, 3, 2],
             [None, 0, None, None],
             [3, 3, None, 2],
             [None, None, 2, 2]]
    _board = Board(table)
    _board.print()

    print("___________________________________")

    new_unknown_count = _board.unknonw_edge_count()
    old_unknown_count = new_unknown_count + 1
    while new_unknown_count < old_unknown_count:
        old_unknown_count = new_unknown_count
        for cross in _board.structures:
            cross.update()
        for square in _board.squares:
            square.update()
        new_unknown_count = _board.unknonw_edge_count()
    _board.print()


    