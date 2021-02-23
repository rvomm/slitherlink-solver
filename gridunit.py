
import edge

class GridUnit:
    """
    An GridUnit is a collection of a Cell and its four surrounding 
    edges. Its main purpose is to complete any remaining edges of 
    cell.  
    """
    def __init__(self, cell, u, d, l, r):
        self.complete = False
        self.cell = cell
        self.u = u
        self.d = d
        self.l = l
        self.r = r

    def _count_alive(self):
        res = [obj.status == "alive" for obj in self._list()]
        return sum(res)

    def _count_dead(self):
        res = [obj.status == "dead" for obj in self._list()]
        return sum(res)

    def _kill_remaining(self):
        for obj in self._list():
            if obj.status == "unknown":
                obj.kill()
    
    def _make_remaining(self):
        for obj in self._list():
            if obj.status == "unknown":
                obj.make()
    
    def _list(self):
        return [self.u, self.d, self.l, self.r]

    def update(self):
        if not self.complete:
            if self._count_alive() == self.cell.target():
                self._kill_remaining()
            if self._count_dead() == (self.cell.n_max - self.cell.target()):
                self._make_remaining()
            self._set_complete()
    
    def _set_complete(self):
        res = [obj.status != "unknown" for obj in self._list()]
        if res == self.cell.n_max:
            self._complete = True

if __name__ == "__main__":

    u = edge.Edge()
    u.make()
    d = edge.Edge() 
    d.kill()
    l = edge.Edge()
    r = edge.Edge()
    obj = EdgeSquare(u, d, l, r)
    print(obj)
    print(obj.count_alive())
    print(obj.count_dead())
    obj.make_all()
    print(obj.count_alive())
