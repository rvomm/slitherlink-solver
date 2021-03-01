 
from abc import ABC, abstractclassmethod
from edgeset import EdgeSet
from edge import Edge

class Structure(ABC):
    """
    A structure is a superclass,
    which is inherited from by square.StructureSquareWithTarget and crosspoint.StructureCross
    mainly containing the boolean is_complete
    """
    _cell_max = 4

    def __init__(self):
        self.is_complete = False

    def solve(self):
        if not self.is_complete:
            self._try_solve() 
            self._set_complete()

    def is_changed(self):
        changed = [obj.changed for obj in self.edge_set().edges]
        return any(changed)

    @abstractclassmethod
    def _try_solve(self):
        pass

    @abstractclassmethod
    def edge_set(self):
        pass

    def _set_complete(self):
        is_known = [not edge.is_unknown() for edge in self.edge_set().edges]
        self.is_complete = all(is_known)

class Cross(Structure):
    """
    A StructureCross is a set of four edges stemming from a single
    point.

    Rules: there can only be 0 or 2 active edges. If two edges
    are alive, kill the remaining two. If only one edge is left
    unknown, deduce status from the other 3 edges.
    """

    def __init__(self, edges):
        super().__init__()

        self.edges = edges

    def _try_solve(self):
        if self.edge_set().n_alive() == 2:
            self.edge_set().kill_remaining()
        elif self.edge_set().n_unknown() == 1: 
            if self.edge_set().n_alive() == 1:
                self.edge_set().make_remaining()
            else:
                self.edge_set().kill_remaining()

    def edge_set(self):
        return EdgeSet(self.edges)

class TargetSquare(Structure):
    """
    A square contains one cell and its surrounding edges.

    Rules: the cell target is the number edges that must surround
    the cell.
    """

    def __init__(self, target: int, edges: set):

        super().__init__()
        self._n_max = 4
        self.target = target
        self.edges = edges

    def edge_set(self):
        return EdgeSet(self.edges)

    def _try_solve(self):
        if (self._n_alive_equals_target()):
            self.edge_set().kill_remaining()

        if (self._n_dead_equals_max_minus_target()):
            self.edge_set().make_remaining()

    def _n_alive_equals_target(self):
        return (self.edge_set().n_alive() == self.target)

    def _n_dead_equals_max_minus_target(self):
        return (self.edge_set().n_dead() == (self._n_max - self.target))


class CrossPlusSquare(Structure):
    def __init__(self, cross: Cross, square: TargetSquare):

        super().__init__()
        self.cross = cross
        self.square = square

        self.edges_opposing = EdgeSet(square.edges - cross.edges)
        self.edges_common = EdgeSet(cross.edges.intersection(square.edges))
        self.edges_outgoing = EdgeSet(cross.edges - square.edges)

    def edge_set(self):
        return EdgeSet(self.cross.edges.union(self.square.edges))

    def _try_solve(self):
        if self.square.target == 1:
            if self._cross_is_incoming():
                self.edges_opposing.kill_remaining()
            
            if self.edges_outgoing.n_dead() == 2:
                self.edges_common.kill_remaining()

        if self.square.target == 2:
            if self._cross_is_incoming():
                if self.edges_opposing.n_alive() == 1:
                    self.edges_opposing.kill_remaining()
                if self.edges_opposing.n_dead() == 1:
                    self.edges_opposing.make_remaining()
        
        if self.square.target == 3: 
            if self.edges_outgoing.n_alive() == 1:
                self.edges_opposing.make_remaining()
                self.edges_outgoing.kill_remaining()
            if self.edges_outgoing.n_dead() == 2:
                self.edges_common.make_remaining()

    def _cross_is_incoming(self):
        """
        Check if outgoing cross edges are linked to common edges.
        """
        return self.edges_outgoing.n_alive() == 1 and self.edges_outgoing.n_dead() == 1
        
class AdjacentSquaresOneOne(Structure):

    def __init__(self, square1, square2, cross):
        
        super().__init__()
        self.square1 = square1 
        self.square2 = square2
        self.cross = cross
    
    def _try_solve(self):
        if self._outlier_edge().is_dead():
            self._mid_edge().kill()

    def _square_edges(self) -> set:
        return self.square1.edges.union(self.square2.edges)

    def _outlier_edge(self) -> Edge:
        [edge] = self.cross.edges.difference(self._square_edges())
        return edge

    def _mid_edge(self) -> Edge:
        [edge] = self.square1.edges.intersection(self.square2.edges)
        return edge
        
    def edge_set(self) -> EdgeSet:
        return EdgeSet(set([self._outlier_edge()]))
    
class AdjacentSquaresThreeThree(Structure):
    """
    Two adjacent threes have a deterministic strategy which can be applied
    immediately. The opposite edges and the mid-edge should always be alive. 
    As a bonus, the outliers of the two crosses shared by the squares 
    should always be dead.
    """
    def __init__(self, square1, square2, cross1, cross2):
        
        super().__init__()
        self.square1 = square1
        self.square2 = square2
        self.cross1 = cross1
        self.cross2 = cross2
        
    def edge_set(self):
        return self._mid_edgeset()

    def _try_solve(self):

        self._outlier_edgeset().kill_remaining()
        self._opposite_edgeset().make_remaining()
        self._mid_edgeset().make_remaining()

    def _outlier_edgeset(self):
        edges = self._cross_edges().difference(self._square_edges())
        return EdgeSet(edges)

    def _opposite_edgeset(self):
        edges = self._square_edges().difference(self._cross_edges())
        return EdgeSet(edges)

    def _mid_edgeset(self):
        edges = self.square1.edges.intersection(self.square2.edges)
        return EdgeSet(edges)

    def _cross_edges(self):
        return self.cross1.edges.union(self.cross2.edges)

    def _square_edges(self):
        return self.square1.edges.union(self.square2.edges)

    
class AdjacentSquaresOneThree(Structure):
    """
    A 1-square and an adjacent 3-square, accompanied by their two overlapping
    cross. 

    If a cross has a dead 'outlier' edge (the edge not part of either square),
    the edge of the cross adjacent to only the 3-square must be alive.
    """
    def __init__(self, square1, square2, cross):
        
        super().__init__()
        self.square1 = square1
        self.square2 = square2
        self.cross = cross
    
    def _square_edges(self) -> set:
        return self.square1.edges.union(self.square2.edges)

    def _outlier_edge(self) -> Edge:
        [edge] = self.cross.edges.difference(self._square_edges())
        return edge

    def _square_three_edge(self) -> Edge:
        edges = self.square2.edges
        edges = edges.intersection(self.cross.edges)
        [edge] = edges.difference(self.square1.edges)
        return edge
        
    def edge_set(self) -> EdgeSet:
        return EdgeSet(set([self._outlier_edge()]))
    
    def _try_solve(self):
        if self._outlier_edge().is_dead():
            self._square_three_edge().make()
        

class CrossSquareCross(Structure):
    """
    A 2-square with two opposing edges. 
    """
    def __init__(self, square: TargetSquare, cross1: Cross, cross2: Cross):
        super().__init__()
        self.square = square
        self.cross1 = cross1
        self.cross2 = cross2
    
    def edge_set(self):
        return EdgeSet(self.square.edges)
        
    def _try_solve(self): 
        pass

class CrossSquareCrossNotAdjacent(Structure):
    """
    A CrossSquareCross structure that is not adjacent (horizontally or 
    vertically) to any other TargetSquares. 

    For such structures, we can leverage on the uniqueness of the solution. 
    If one edge has zero incoming edges (both are dead edges), there are only
    two solutions for the 2-square. The opposite cross (cross2) then either 
    has zero or two edges alive. To solve we reason by contradiction:
    
    Suppose the opposite cross has zero edges alive. Then the square is not 
    restricted by these opposing crosses. But there are also no constraints
    implied by any adjacent squares (there are none!). This means that the
    square must have two solutions! This contradicts the uniqueness of the 
    solution.

    Hence, the opposite cross must have two edges alive. The solution of the 
    rest of the square is dealt with by the relevant CrossSquare object. A 
    simple example would be a 2-square in a corner without adjacent squares.
    """
    def __init__(self, square: TargetSquare, cross1: Cross, cross2: Cross):
        
        super().__init__()
        self.square = square
        self.cross1 = cross1
        self.cross2 = cross2
    
    def edge_set(self):
        return EdgeSet(self.square.edges)
        
    def _try_solve(self): 
        if self._cross_edges_outgoing(self.cross1).n_dead() == 2:
            if self._cross_edges_outgoing(self.cross2).n_unknown() == 2:
                self._cross_edges_outgoing(self.cross2).make_remaining()

    def _cross_edges_outgoing(self, cross: Cross): 
        edges = cross.edges.difference(self.square.edges)
        return EdgeSet(edges)
