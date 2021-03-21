import game 
import os.path
from level_loader import all_levels


def report_all_levels():
    path_list = all_levels()
    print(path_list)
    level_dict = {path: None for path in path_list}
    for key in level_dict.keys():
        _board = game.Game(key).board
        _board.no_prints()
        new_unknown_count = _board.unknonw_edge_count()
        old_unknown_count = new_unknown_count + 1
        while new_unknown_count < old_unknown_count:
            old_unknown_count = new_unknown_count
            _board.solve_iteration()
            _board.solve_iteration()
            new_unknown_count = _board.unknonw_edge_count()
        _board.print(True, ignore_mute=True)
        level_dict[key] = _board.solved()
        print(key)
        print("solved:", level_dict[key])
    for key, item in level_dict.items():
        print(item, key)



if __name__ == "__main__":
    # level = os.path.join("levels", "medium", "normal_0001.txt")
    # _board = game.Game(level).board
    # new_unknown_count = _board.unknonw_edge_count()
    # old_unknown_count = new_unknown_count + 1
    # while new_unknown_count < old_unknown_count:
    #     old_unknown_count = new_unknown_count
    #     _board.solve_iteration()
    #     _board.solve_iteration()
    #     new_unknown_count = _board.unknonw_edge_count()
    # _board.print(True)
    # print(_board.solved())
    report_all_levels()


    