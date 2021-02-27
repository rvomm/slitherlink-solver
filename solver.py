import game 

if __name__ == "__main__":
    level = "test1.txt"
    _board = game.Game(level).board
    
    new_unknown_count = _board.unknonw_edge_count()
    old_unknown_count = new_unknown_count + 1
    while new_unknown_count < old_unknown_count:
        old_unknown_count = new_unknown_count
        _board.solve_iteration()
        new_unknown_count = _board.unknonw_edge_count()
    _board.print(True)


    