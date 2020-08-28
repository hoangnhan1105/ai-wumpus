# 1..100: Breeze
# 101..200: Pit
# 201..300: Stench
# 301..400: Wumpus
# 401..500: Safe

from pysat.solvers import Glucose3

class percept:
    def __init__(self, pos, breeze, stench):
        self.pos = pos
        self.breeze = breeze
        self.stench = stench

class agent:
    def __init__(self, knowledge_base=[]):
        self.knowledge_base = knowledge_base

    def init_kb(self):

        # Breeze(x, y) <=> Pit(x, y - 1) v Pit(x - 1, y) v Pit(x + 1, y) v Pit(x, y + 1)
        for i in range(1, 101):
            clause_list = [[-i]]
            for j in [-10, -1, 1, 10]:
                if 1 <= i + j <= 100:
                    clause_list[0].append(100 + i + j)
                    clause_list.append([i, -(100 + i + j)])
            self.knowledge_base += clause_list

        # Stench(x, y) <=> Wumpus(x, y - 1) v Wumpus(x - 1, y) v Wumpus(x + 1, y) v Wumpus(x, y + 1)
        for i in range(201, 301):
            clause_list = [[-i]]
            for j in [-10, -1, 1, 10]:
                if 201 <= i + j <= 300:
                    clause_list[0].append(100 + i + j)
                    clause_list.append([i, -(100 + i + j)])
            self.knowledge_base += clause_list

        # ~Pit(x, y) ^ ~Wumpus(x, y) => Safe(x, y)
        for i in range(1, 101):
            self.knowledge_base.append([100 + i, 300 + i, 400 + i])

    def convert_pos_to_index(self):
        pass

    def get_adjacent_cells(self, pos):
        pass

    def infer_new_knowledge(self, new_percept):
        idx = new_percept.pos

        self.knowledge_base.append([500 + idx])  # Visited
        if new_percept.breeze:
            self.knowledge_base.append([idx])
        if new_percept.stench:
            self.knowledge_base.append([200 + idx])

        adj_cells = self.get_adjacent_cells(new_percept.pos)
        adj_idx_list = [self.convert_pos_to_index(cell) for cell in adj_cells]
        for adj_idx in adj_idx_list:
            g = Glucose3()
            for clause in self.knowledge_base:
                g.add_clause(clause)
                # ...
