

class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def __repr__(self):
        return "(" + str(self.row) + "," + str(self.col) + ")"

    def pos(self):
        return [self.row, self.col]

if __name__ == "__main__":
    print(Point(1, 2))
    print(Point(0,0).pos())