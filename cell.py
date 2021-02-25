
class Cell:
    def __init__(self):
        self.completed = False
        self.n_max = 4

class CellFactory:
    def __init__(self, target):
        self.target = target

    def create(self):
        if self.target == 0:
            return CellZero()
        elif self.target == 1:
            return CellOne()
        elif self.target == 2: 
            return CellTwo()
        elif self.target == 3: 
            return CellThree()
        elif self.target == 4:
            return CellFour()
        else: 
            return CellUnknown()

class CellUnknown(Cell):
    """
    A dummy subclass that is only necessary to draw the 
    empty space. 
    """ 
    def target(self):
        pass

    def draw(self):
        return " "

class CellZero(Cell):
    """
    CellZero can't have any edges around it. All edges around it
    will be killed instantly. The cell is complete after the first 
    update().
    """
    
    def draw(self):
        return "0"

    def target(self):
        return 0

class CellOne(Cell):
    """
    Nothing special about CellOne. 
    """
    def draw(self):
        return "1"
    def target(self):
        return 1

class CellTwo(Cell):
    """
    CellTwo is the most complicated cell, as there are 6 
    different ways to fill in the surrounding edges. 
    Two cases have edges on opposite sides of the cell. 
    Two cases have a diagonal (/) from bottom left to 
    top right, either convex or concave.
    Two cases have a diagonal (\\) from top left to bottom
    right, either convex or concave.
    
    We need to be able to distinguish these three groups of
    cases for some solution techniques. 
    """
    def draw(self):
        return "2"
    def target(self):
        return 2

class CellThree(Cell):
    """
    Cell three is almost as simple as cell 1. 
    """
    def draw(self):
        return "3"
    def target(self):
        return 3

class CellFour(Cell):
    """
    I am not sure if there is need for this class, but since it is 
    so simple to implement it, might as well do it. 
    """
    def draw(self):
        return "4"
    def target(self):
        return 4

if __name__ == "__main__":
    x = CellFour()
    print(x.draw())
    print(x.target())
