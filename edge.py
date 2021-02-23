
import point

class Edge: 
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
        self.status = "unknown"
        self.changed = False

    def __repr__(self):
        return f"Edge: {self.source.__repr__()} -> {self.dest.__repr__()} ({self.status})" 
 
    def reset(self):
        self.status = "unknown"
        self.changed = False

    def make(self):
        self.status = "alive"
        self.changed = True

    def kill(self):
        self.status = "dead"
        self.changed = True
 
    def is_unknown(self):
        return (self.status == "unknown")

    def is_alive(self):
        return (self.status == "alive")

    def is_dead(self):
        return (self.status == "dead")

    def is_attached_to_point(self, point):
        return (point is self.source or point is self.dest)
        

    def draw_h(self):
        if self.is_alive():
            return "-"
        elif self.is_dead():
            return "x"
        else: 
            return " "

    def draw_v(self):
        if self.is_alive(): 
            return "|"
        elif self.is_dead():
            return "x"
        else: 
            return " "

if __name__ == "__main__":

    x = Edge(point.Point(0,0), point.Point(1,0))
    y = Edge(point.Point(0,0), point.Point(1,0))
    z = Edge(point.Point(0,0), point.Point(100,10))
    y.make()
    z.kill()
    print(x)
    print(y)
    print(z)
