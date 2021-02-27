 
from abc import ABC, abstractclassmethod
import edge 
import point
from crosspoint import StructureCross
from square import StructureSquareWithTarget

class Structure(ABC):
    """
    A structure is a superclass,
    which is inherited from by square.StructureSquareWithTarget and crosspoint.StructureCross
    mainly containing the boolean is_complete
    """
    _cell_max = 4

    def __init__(self):
        self.is_complete = False

    def update(self):
        if not self.is_complete:
            self._update() 
            self._set_complete()

    def is_changed(self):
        changed = [obj.changed for obj in self._edges()]
        return any(changed)

    @abstractclassmethod
    def _update(self):
        pass

    @abstractclassmethod
    def _edges(self):
        pass

    def _set_complete(self):
        is_known = [not obj.is_unknown() for obj in self._edges()]
        self.is_complete = all(is_known)
    
    def _kill_remaining(self):
        for obj in self._edges():
            if obj.is_unknown():
                obj.kill()
    
    def _make_remaining(self):
        for obj in self._edges():
            if obj.is_unknown():
                obj.make()

    def _n_dead(self):
        is_dead = [obj.is_dead() for obj in self._edges()]
        return sum(is_dead)
        
    def _n_alive(self):
        is_alive = [obj.is_alive() for obj in self._edges()]
        return sum(is_alive)

    def _n_unknown(self):
        is_unknown = [obj.is_unknown() for obj in self._edges()]
        return(sum(is_unknown))


class CrossPlusSquare(Structure):
    def __init__(self, cross: StructureCross, square: StructureSquareWithTarget):
        self.cross = cross
        self.cross = square
        cross_edges = set(cross.edges)
        square_edges = set(square.edges)
        self.opposing_edges = EdgeSet(square_edges-cross_edges)
        self.common_edges = EdgeSet(cross_edges.intersection(square_edges))
        self.outgoing_edges = EdgeSet(cross_edges-square_edges)

    def get_opposing_edges(self):
        return self.opposing_edges

    def get_common_edges(self):
        return self.common_edges

    def get_outgoing_edges(self):
        return self.outgoing_edges

    def update(self):
        if self.outgoing_edges._n_alive() == 1 and self.square.target == 3:
            self.opposing_edges._make_remaining()
        if self.outgoing_edges._n_alive() == 1 and self.square.target == 1:
            self.opposing_edges._kill_remaining()

class EdgeSet(Structure):
    def __init__(self, edges):
        """
        :param edges: list or set of edge objects
        """
        self.edges = edges
        # for testing purposes
        assert len(set.edges) <= 2
