


import structure
import point
import edge


class StructureSquareWithTarget(structure.Structure):
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
    

if __name__ == "__main__":

    edges = {
        "u" : edge.Edge(point.Point(0,0), point.Point(0,1)),
        "d" : edge.Edge(point.Point(1,0), point.Point(1,1)),
        "l" : edge.Edge(point.Point(0,0), point.Point(1,0)),
        "r" : edge.Edge(point.Point(0,1), point.Point(1,1))
    }

    print(edges["u"])
    swt = StructureSquareWithTarget(3, edges)
    print(swt)
    swt.update()
    print(swt)

    swt.edges["u"].kill()
    print(swt)
    swt.update()
    print(swt)
