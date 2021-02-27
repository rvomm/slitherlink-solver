
from point import Point
from edge import Edge
from structure import CrossPlusSquare, Cross, TargetSquare

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
        self._initialize_squares()
        self._initialize_crossplussquares()

    def _initialize_squares(self):
        squares = []
        for row_index, constraint_row in enumerate(self.constraints):
            for column_index, constraint in enumerate(constraint_row):
                if constraint is not None:
                    ul = self._point(row_index, column_index)
                    ur = self._point(row_index, column_index + 1)
                    dl = self._point(row_index + 1, column_index)
                    dr = self._point(row_index + 1, column_index + 1)

                    edges = {
                        "u": self._edge(ul, ur),
                        "d": self._edge(dl, dr),
                        "r": self._edge(ur, dr),
                        "l": self._edge(ul, dl)
                    }
                    squares.append(TargetSquare(constraint, edges))
        self.squares = squares

    def solve_iteration(self):
        for cross in self.crosses:
            cross.update()
            self.print(True)
        for square in self.squares:
            square.update()
            self.print(True)
        for cross_plus_square in self.cross_plus_square_list:
            cross_plus_square.update()
            self.print(True)

    def _initialize_structure_crosspoints(self):
        crosspoints = []
        for point in self.points:
            edges = self._get_edges_from_point(point)
            obj = Cross(edges)
            crosspoints.append(obj)

        self.crosses = crosspoints

    def _initialize_crossplussquares(self):
        cross_plus_square_list = []
        for cross in self.crosses:
            for square in self.squares:
                set_of_overlapping_edges = set(cross.edges.values()).intersection(set(square.edges.values()))
                if len(set_of_overlapping_edges) > 1:
                    cross_plus_square_list.append(CrossPlusSquare(cross, square))
        self.cross_plus_square_list = cross_plus_square_list

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

    def unknonw_edge_count(self):
        count = 0
        for edge in self.edges:
            if edge.is_unknown():
                count += 1
        return count

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

    def _get_edges_from_point(self, point):

        up = self._point(point.row + 1, point.col)
        down = self._point(point.row - 1, point.col)
        right = self._point(point.row, point.col + 1)
        left = self._point(point.row, point.col - 1)
        
        edges = {
            "u" : self._edge(point, up),
            "d" : self._edge(point, down),
            "r" : self._edge(point, right),
            "l" : self._edge(point, left)
        }
        
        return edges

    @staticmethod
    def delta_point(source, dest):
        source = source.pos()
        dest = dest.pos()
        return source[0]-dest[0], source[1]-dest[1]

    def print(self, with_line):
        """
        placeholder for a method that prints the current state of the board
        This method does nothing yet
        :return: a nice print (by default something has to be returned, so a None-value will be returned)
        """
        if with_line == True:
            print("------------------------------")

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
                row_index = int(i/2)
                line = "+"
                for column_index in range(self.ncol):
                    line = line + (horizontal_edges[row_index][column_index].draw_h()) + "+"
                print(line)
            else:
                row_index = int((i-1)/2)
                line = vertical_edges[row_index][0].draw_v()
                for column_index in range(self.ncol):
                    digit = self.constraints[row_index][column_index]
                    line = line + " " + (str(digit) if digit is not None else " ") + " "
                    line = line + (vertical_edges[row_index][column_index+1].draw_v())
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

