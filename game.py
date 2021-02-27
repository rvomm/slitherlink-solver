

import board
import re

class Game: 
    
    def __init__(self, path):
        self.path = path
        self.board = board.Board(self._constraints())

    def _constraints(self):

        # TODO: add validations
        return self._read_constraints()
    
    def _read_constraints(self):
        
        with open(self.path, "r") as file:
            level = file.read().split("\n")

        level = [re.sub("[^01234]", " ", line) for line in level]
        constraints = [[None if x == " " else int(x) for x in list(line)] for line in level]
    
        return constraints