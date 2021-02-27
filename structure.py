 
from abc import ABC, abstractclassmethod

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


class EdgeSet(Structure):
    def __init__(self, edges):
        """
        :param edges: list or set of edge objects
        """
        self.edges = edges

    def _edges(self):
        return self.edges

    def _update(self):
        pass


class StructureCross(Structure):
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

    def _update(self):
        if self._n_alive() == 2:
            self._kill_remaining()
        elif self._n_unknown() == 1:
            if self._n_alive() == 1:
                self._make_remaining()
            else:
                self._kill_remaining()

    def _edges(self):
        return list(self.edges.values())

    def __repr__(self):
        res = ""
        for key, value in self.edges.items():
            res = res + key + " : " + value.draw_h() + ", "
        return res


class StructureSquareWithTarget(Structure):
    """
    A square contains one cell and its surrounding edges.

    Rules: the cell target is the number edges that must surround
    the cell.
    """

    def __init__(self, target, edges):

        super().__init__()

        self._n_max = 4
        self.target = target
        self.edges = edges

    def __repr__(self):
        out = ""
        for key, value in self.edges.items():
            out = out + key + " : " + value.draw_h() + "\n"

        return out

    def _edges(self):
        return self.edges.values()

    def _update(self):
        if (self._n_alive_equals_target()):
            self._kill_remaining()

        if (self._n_dead_equals_max_minus_target()):
            self._make_remaining()

    def _n_alive_equals_target(self):
        return (self._n_alive() == self.target)

    def _n_dead_equals_max_minus_target(self):
        return (self._n_dead() == (self._n_max - self.target))


class CrossPlusSquare(Structure):
    def __init__(self, cross: StructureCross, square: StructureSquareWithTarget):
        self.cross = cross
        self.square = square
        cross_edges = set(cross.edges.values())
        square_edges = set(square.edges.values())
        self.opposing_edges = EdgeSet(square_edges-cross_edges)
        self.common_edges = EdgeSet(cross_edges.intersection(square_edges))
        self.outgoing_edges = EdgeSet(cross_edges-square_edges)

    def _edges(self):
        return []

    def _update(self):
        pass

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