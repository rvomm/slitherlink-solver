 
from abc import ABC, abstractclassmethod
import edge 
import point

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


