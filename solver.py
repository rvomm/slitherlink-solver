from Board import Board

if __name__ == "__main__":
    table = [[None, None, 3, 2],
             [None, 0, None, None],
             [3, 3, None, 2],
             [None, None, 2, 2]]
    _board = Board(table) #if I would not type the underscore python might maybe confuse the object with a class or definition.
    # You cant call an object list, but you can call it _list
    _board.print()
    print("breakpoint here in Pycharm")