
class EdgeSet:
    def __init__(self, edges: set):
        """
        :param edges: list or set of edge objects
        """
        self.edges = edges

    def kill_remaining(self):
        for edge in self.edges:
            if edge.is_unknown():
                edge.kill()
    
    def make_remaining(self):
        for edge in self.edges:
            if edge.is_unknown():
                edge.make()

    def n_dead(self):
        is_dead = [edge.is_dead() for edge in self.edges]
        return sum(is_dead)
        
    def n_alive(self):
        is_alive = [edge.is_alive() for edge in self.edges]
        return sum(is_alive)

    def n_unknown(self):
        is_unknown = [edge.is_unknown() for edge in self.edges]
        return(sum(is_unknown))
