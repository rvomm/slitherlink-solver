
from point import Point
from edge import Edge
from crosspoint import StructureCross

class Board:

    def __init__(self, constraints=None):
        """

        :param constraints: rectangular list of digits. None means no digit in the corresponding square
        """
        if constraints is None:
            constraints = [[1, None, 3], [None, 2, None]]
        self.constraints = constraints
        self.nrow = len(constraints)
        self.ncol = len(constraints[0])
        self._initialize()

    def _initialize(self):
        self._initialize_points()
        self._initialize_edges()
        self._initialize_structure_crosspoints()
    
    def _initialize_structure_crosspoints(self):
        
        crosspoints = []
        for point in self.points:
            edges = self._get_edges_from_point(point.row, point.col)
            obj = StructureCross(edges)
            crosspoints.append(obj)

        self.structures = crosspoints

    def _initialize_points(self):
        """
        The full set of points is the union of all corners of each 
        of the cells.

        Also fictional void point outside the grid are generated (not stored) to handle boundary conditions of the board
        """
        points = []
        for row in range(0, self.nrow + 1):
            for col in range(0, self.ncol + 1):
                points.append(
                    Point(row=row, col=col)
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
        For each point, create an edge from the point to the
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
        if col < self.ncol:
            down = self._point(row, col + 1)
            self.edges.append(
                Edge(source=here, dest=down)
            )
        # edge creation to bottom
        if row < self.nrow:
            right = self._point(row + 1, col)
            self.edges.append(
                Edge(source=here, dest=right)
            )

    def _get_edges_from_point(self, row, col):

        here = self._point(row, col)
        up = self._point(row + 1, col)
        down = self._point(row - 1, col)
        right = self._point(row, col + 1)
        left = self._point(row, col - 1)
        
        edges = {
            "u" : self._edge(here, up),
            "d" : self._edge(here, down),
            "r" : self._edge(here, right),
            "l" : self._edge(here, left)
        }
        
        return edges

    @staticmethod
    def delta_point(source, dest):
        source = source.pos()
        dest = dest.pos()
        return source[0]-dest[0], source[1]-dest[1]

    def print(self):
        """
        placeholder for a method that prints the current state of the board
        This method does nothing yet
        :return: a nice print (by default something has to be returned, so a None-value will be returned)
        """
        # organize edges
        horizontal_edges = [[None]*self.ncol for i in range(self.nrow+1)]
        vertical_edges = [[None]*(self.ncol+1) for i in range(self.nrow)]
        for edge in self.edges:
            delta_row, delta_col = Board.delta_point(edge.source, edge.dest)
            source = edge.source.pos()
            if delta_col == 0:
                vertical_edges[source[0]][source[1]] = edge
            else:  # if delta_row == 0:
                horizontal_edges[source[0]][source[1]] = edge
        # print edges
        for i in range(2*self.nrow + 1):
            if i % 2 == 0:
                line = "+"
                for column in range(self.ncol):
                    line = line + (horizontal_edges[int(i / 2)][column].draw_h()) + "+"
                print(line)
            else:
                line = vertical_edges[int((i - 1) / 2)][0].draw_v()
                for column in range(self.ncol):
                    digit = self.constraints[int((i - 1) / 2)][column]
                    line = line + " " + (str(digit) if digit is not None else " ") 
                    line = line + " "
                    line = line + (vertical_edges[int((i - 1) / 2)][column+1].draw_v())
                print(line)

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

