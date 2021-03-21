import json
import glob
import os

FILE_PATH = "data/levels.json"

def all_levels():
    return glob.glob(os.path.join("levels", "hard", "*.txt")) + glob.glob(os.path.join("levels", "medium", "*.txt"))

def load_level_list():
    with open(FILE_PATH, 'r') as file:
        return json.load(file)

def save_level(table_list):
    with open(FILE_PATH, 'w') as outfile:
        json.dump(table_list, outfile)

def append_level(table):
    level_list = load_level_list()
    already_in_there = False
    for t in level_list:
        if levels_equal(t,table):
            already_in_there = True
    if not already_in_there:
        level_list.append(table)
        with open(FILE_PATH, 'w') as outfile:
            json.dump(level_list, outfile)

def levels_equal(table_a, table_b):
    if len(table_a) != len(table_b) or len(table_a[0]) != len(table_b[0]):
        return False
    for row_index in range(len(table_a)):
        for col_index in range(len(table_a[0])):
            if table_a[row_index][col_index] != table_b[row_index][col_index]:
                return False
    return True

def test_shape(table):
    row_length = len(table[0])
    for index, row in enumerate(table):
        if len(row) != row_length:
            print("row with index ", index, " is not of same lenght as first row")
            return False
    return True

if __name__ == "__main__":
    table = [[None, 3, 1, None, None, None, 3],
              [None, 3, None, None, 2, 2, None],
              [3, None, 1, 2, 1, 0, 3],
              [None, None, None, None, None, None, None],
              [None, None, None, 2, None, None, 3],
              [None, None, 2, 3, None, 3, None],
              [3, None, 3, None, 2, 2, None]
              ]
    shape_bool = test_shape(table)
    print("right shape:"+str(shape_bool))
    if shape_bool:
        append_level(table)
        level_list = load_level_list()
        print(level_list[-1])
        print("length of level_list =", len(level_list))