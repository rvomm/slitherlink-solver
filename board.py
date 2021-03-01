
from point import Point
from edge import Edge
from structure import Cross, TargetSquare, CrossPlusSquare, AdjacentThreeThree, AdjacentOneOne, AdjacentOneThree, SquareTwoUniquenessContraint

class Board:

    def __init__(self, constraints):
        """

        :param constraints: rectangular list of digits. None means no digit in the corresponding square
        """
        self.constraints = constraints
        self.nrow = len(constraints)
        self.ncol = len(constraints[0])
        self._initialize()
        self.pointgroups = []

    def _initialize(self):
        self._initialize_points()
        self._initialize_edges()
        self._initialize_crosses()
        self._initialize_squares()
        self._initialize_cross_plus_squares()
        self._initialize_adjacent_one_ones()
        self._initialize_adjacent_one_threes()
        self._initialize_adjacent_three_threes()
        self._initialize_cross_square_crosses()
        
    
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

    def _initialize_adjacent_three_threes(self):
        
        adjacent_three_threes = []
        threes = [square for square in self.squares if square.target == 3]
        for square1 in threes:
            for square2 in threes:

                edges_common = square1.edges.intersection(square2.edges)

                if len(edges_common) == 1:
                    crosses = [cross for cross in self.crosses if len(cross.edges.intersection(edges_common)) > 0]
                    struc = AdjacentThreeThree(square1, square2, crosses[0], crosses[1])
                    adjacent_three_threes.append(struc)

        self.adjacent_three_threes = adjacent_three_threes

    def _initialize_adjacent_one_ones(self):
        
        adjacent_one_ones = []
        ones = [square for square in self.squares if square.target == 1]
        for square1 in ones:
            for square2 in ones:

                edges_common = square1.edges.intersection(square2.edges)

                if len(edges_common) == 1:
                    crosses = [cross for cross in self.crosses if len(cross.edges.intersection(edges_common)) > 0]
                    struc = AdjacentOneOne(square1, square2, crosses[0], crosses[1])
                    adjacent_one_ones.append(struc)

        self.adjacent_one_ones = adjacent_one_ones

    def _initialize_adjacent_one_threes(self):
        
        adjacent_one_threes = []
        ones = [square for square in self.squares if square.target == 1]
        threes = [square for square in self.squares if square.target == 3]
        for square1 in ones:
            for square3 in threes:

                edges_common = square1.edges.intersection(square3.edges)

                if len(edges_common) == 1:
                    crosses = [cross for cross in self.crosses if len(cross.edges.intersection(edges_common)) > 0]
                    struc = AdjacentOneThree(square1, square3, crosses[0], crosses[1])
                    adjacent_one_threes.append(struc)

        self.adjacent_one_threes = adjacent_one_threes

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
                        self._edge(ul, ur), self._edge(dl, dr),
                        self._edge(ur, dr), self._edge(ul, dl)
                    }
                    squares.append(TargetSquare(constraint, edges))
        self.squares = squares

    def _initialize_cross_square_crosses(self):
        """
        Only for squares with target 2, we need to create a structure with the square
        and diagonal crosses. By considering ordered pairs, there are four different 
        combinations per square.  
        """
        cross_square_crosses = []
        square2s = [square for square in self.squares if square.target == 2]

        for square2 in square2s:

            adjacent = [square for square in self.squares if len(square.edges.intersection(square2.edges)) == 1]
            if (len(adjacent) == 0):

                crosses = [cross for cross in self.crosses if len(cross.edges.intersection(square2.edges)) > 0]
                for cross1 in crosses:
                    cross2 = next(iter(
                        [cross for cross in crosses if len(cross1.edges.intersection(cross.edges)) == 0]
                    ))
                    
                cross_square_crosses.append(
                    SquareTwoUniquenessContraint(square2, [cross1, cross2])
                )

        self.cross_square_crosses = cross_square_crosses        

    def solve_iteration(self):
        for cross in self.crosses:
            cross.solve()
        for square in self.squares:
            square.solve()
        for cross_plus_square in self.cross_plus_squares:
            cross_plus_square.solve()

        for adjacent_three_three in self.adjacent_three_threes:
            adjacent_three_three.solve()
        for adjacent_one_one in self.adjacent_one_threes:
            adjacent_one_one.solve()
        for adjacent_one_one in self.adjacent_one_ones:
            adjacent_one_one.solve()

        for cross_square_cross in self.cross_square_crosses:
            cross_square_cross.solve()
        self.point_group_update()
        self.print(True)

    def point_group_update(self):
        # update self.pointgroups based on edge.recently_changed (with edge in self.edges)
        for edge in self.edges:
            if edge.recently_changed:
                if edge.is_alive():
                    point_list = [edge.dest, edge.source]
                    index_list = [self.index_of_pointgroup(point) for point in point_list]
                    nr_of_nones = index_list.count(None)
                    if nr_of_nones == 1:
                        group_index = [el for el in index_list if el is not None][0]
                        new_point = point_list[index_list.index(None)]
                        self.pointgroups[group_index].append(new_point)
                    if nr_of_nones == 2:
                        self.pointgroups.append(point_list)
                    if nr_of_nones == 0:
                        if index_list[0] == index_list[1]:
                            print("level solved")
                        else:
                            index_list.sort()
                            pointgroup_b = self.pointgroups.pop(index_list[1])
                            pointgroup_a = self.pointgroups.pop(index_list[0])
                            self.pointgroups.append(pointgroup_a+pointgroup_b)
                edge.change_is_processed()
        # check whether edges can be killed
        for edge in self.edges:
            if edge.is_unknown():
                point_list = [edge.dest, edge.source]
                index_list = [self.index_of_pointgroup(point) for point in point_list]
                if index_list[0] is not None and index_list[0] == index_list[1]:
                    # the very last edge of the puzzle should not be forbidden here
                    if len(self.pointgroups) > 1:
                        edge.kill()
                    found_unmet_constraint = False
                    for square in self.squares:
                        if edge not in square.edges and not square._n_alive_equals_target():
                            found_unmet_constraint = True
                    if found_unmet_constraint:
                        edge.kill()

    def index_of_pointgroup(self, point: Point):
        for index, group in enumerate(self.pointgroups):
            if point in group:
                return index
        return None


    def _initialize_crosses(self):
        crosses = []
        for point in self.points:
            edges = self._get_edges_from_point(point)
            crosses.append(Cross(edges))

        self.crosses = crosses

    def _initialize_cross_plus_squares(self):

        cross_plus_squares = []
        for cross in self.crosses:
            for square in self.squares:
                set_of_overlapping_edges = cross.edges.intersection(square.edges)
                if len(set_of_overlapping_edges) > 1:
                    cross_plus_squares.append(CrossPlusSquare(cross, square))

        self.cross_plus_squares = cross_plus_squares

    
    def _point(self, row: int, col: int) -> Point:
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


    def _edge(self, source: Point, dest: Point) -> Edge:
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

    def _get_edges_from_point(self, point):

        up = self._point(point.row + 1, point.col)
        down = self._point(point.row - 1, point.col)
        right = self._point(point.row, point.col + 1)
        left = self._point(point.row, point.col - 1)
        
        edges = {
            self._edge(point, up), self._edge(point, down),
            self._edge(point, right), self._edge(point, left)
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

