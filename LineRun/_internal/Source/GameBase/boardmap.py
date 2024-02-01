import random
from Source.GameBase.relation import Relation

'''
This class is responsible to generate random board maps according to the chosen dificulty level.
The self.map attribute is a matriz representation of the board. The points(.) are the empty spaces
and the numbers are the sequence components.
'''

class BoardMap:
    def __init__(self, level):
        self.sequence = []
        self.map = []
        self.level = level
        self.size = Relation.map_relation[level][0]
        self.max_sequence = Relation.map_relation[level][1]
        for i in range(0, self.size[0]*self.size[1]): self.map.append(" ")
        for i in range(1, self.max_sequence + 1): 
            c = random.randint(0, len(self.map) - 1)
            while self.map[c] != " ":
                c = random.randint(0, len(self.map) - 1)
            self.map[c] = str(i)
            self.sequence.append(str(i))
    





