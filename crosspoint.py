
import structure
import edge
import point

class StructureCross(structure.Structure):
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
    

