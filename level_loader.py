import json

FILE_PATH = "data/levels.json"

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

if __name__ == "__main__":
    table = [[None, None, 3, 2],
             [None, 0, None, None],
             [3, 3, None, 2],
             [None, None, 2, 2]]
    save_level([table])
    level_list = load_level_list()
    print(level_list[0])
    table2 = [[2, None, 1, 1, None, 2, None],
             [None, 3, None, None, 1, None, 1],
             [3, 2, None, None, None, None, None],
             [None, 1, 2, 2, 1, 2, None],
             [3, 2, None, 2, 1, None, 2],
             [None, None, 2, None, 1, 2, 3],
             [3, 2, None, None, 2, 2, None]]
    append_level(table2)
    level_list = load_level_list()
    print(level_list[1])