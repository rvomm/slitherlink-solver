
from point import Point
from edge import Edge

class Board:

    def __init__(self, table=None):
        """

        :param table: rectangular list of digits. None means no digit in the corresponding square
        """
        if table is None:
            table = [[1, None, 3], [None, 2, None]]
        self.nrow = len(table)
        self.ncol = len(table[0])
        self._initialize()

    def _initialize(self):
        self._initialize_points()
        self._initialize_edges()
        self._initialize_constraints()
    
    def _initialize_points(self):
        """
        The full set of points is the union of all corners of each 
        of the cells.

        Also need points outside of the grid (void points) they are 
        not stored.  
        """
        points = []
        for row in range(0, self.nrow + 1):
            for col in range(0, self.ncol + 1):
                points.append(
                    Point(row = row, col = col)
                )
        self.points = points

    def _point(self, row, col):
        """
        Return a Point object from self.points given row and column.

        If a coordinate outside the grid is given, no Point will be 
        found and a void point is created and returned.
        """
        point = [point for point in self.points if point.row == row and point.col == col]

        if (len(point) == 1):
            return point.pop()
        else:
            return self._void_point(row, col)


    def _edge(self, source, dest):
        """
        Return an Edge object from self.edges given source and 
        destination. 

        If no edge is found (which happens when either source or 
        dest is a void point), a void edge is created, killed, and 
        returned. 
        """
        edge = [edge for edge in self.edges if (edge.source is source and edge.dest is dest) or edge.source is dest and edge.dest is source]
        
        if (len(edge) == 1):
            return edge.pop()

        else: 
            return self._void_edge(source, dest)

    @staticmethod
    def _void_point(row, col):
        """
        Create a void point outside of the grid. 
        """
        return Point(row, col)

    @staticmethod
    def _void_edge(source, dest):
        """
        Create an edge outside of the grid. These edges are always 
        dead, so we don't need to store them in an awkward data 
        structure but just generate dead edges every time.
        """
        edge = Edge(source, dest)
        edge.kill()
        return edge

    def _initialize_edges(self):
        """
        For each point, simply create an edge from the point to the 
        point on the right and an edge to the point downwards. Skipping
        rightward edge creation for points on the most right column and
        skipping downward edge creation for bottom row.
        """

        self.edges = []
        for row in range(self.nrow+1):
            for col in range(self.ncol+1):
                self._initialize_edge(row, col)
    
    def _initialize_edge(self, row, col):

        here = self._point(row, col)
        # edge creation to right
        if col <= self.ncol:
            down = self._point(row, col + 1)
            self.edges.append(
                Edge(source=here, dest=down)
            )
        # edge creation to bottom
        if col <= self.ncol:
            right = self._point(row + 1, col)
            self.edges.append(
                Edge(source=here, dest=right)
            )
    
    def _initialize_constraints(self): 
        """
        TODO: Initialize cells
        """ 
        self.constraints = [['1', ' ', '2'], ['1', ' ', '3']]

    def _get_edges_from_point(self, row, col):

        edges = {}
        here = self._point(row, col)

        if (row != 0):
            up = self._point(row, col + 1)
            edges["up"] = self._edge(here, up)
        
        if (row != self.nrow): 
            down = self._point(row, col + 1)
            edges["down"] = self._edge(here, down)

        left = self._point(row -1, col)
        right = self._point(row + 1, col)

        return [edge for edge in self.edges if edge.is_attached_to_point(here)]

    def print(self):
        """
        placeholder for a method that prints the current state of the board
        This method does nothing yet
        :param board: a Board object
        :return: a nice print (by default something has to be returned, so a None-value will be returned)
        """
        pass

if __name__ == "__main__":
    
    b = Board()
    for i in Board().points:
        print(i)
    print(Board()._point(1,1))
    
    for i in Board().edges:
        print(i)

    print("Edges from (1,2)")
    for i in Board()._get_edges_from_point(1, 2):
        print(i)

