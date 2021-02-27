from Board import Board
import level_loader
if __name__ == "__main__":
    table = level_loader.load_level_list()[2]
    _board = Board(table)
    new_unknown_count = _board.unknonw_edge_count()
    old_unknown_count = new_unknown_count + 1
    while new_unknown_count < old_unknown_count:
        old_unknown_count = new_unknown_count
        _board.solve_iteration()
        new_unknown_count = _board.unknonw_edge_count()
    _board.print(True)


    