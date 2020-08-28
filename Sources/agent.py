# 1..100: Breeze
# 101..200: Pit
# 201..300: Stench
# 301..400: Wumpus
# 401..500: Safe

from pysat.solvers import Glucose3


class percept:
    def __init__(self, pos=(), breeze=False, stench=False):
        self.pos = pos
        self.breeze = breeze
        self.stench = stench


class agent:
    def __init__(self, knowledge_base=[], pos=(), visited=[]):
        self.knowledge_base = knowledge_base
        self.pos = pos
        self.visited = visited

    def init_kb(self):
        self.knowledge_base = []

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

    def perceive(self, raw_map, pos):
        new_percept = percept(pos=pos)
        if 'b' in raw_map[pos[1]][pos[0]]:
            new_percept.breeze = True
        if 's' in raw_map[pos[1]][pos[0]]:
            new_percept.stench = True
        return new_percept

    def convert_pos_to_index(self, pos):
        return pos[1] * 10 + pos[0] + 1

    def convert_index_to_pos(self, index):
        return (index - 1) % 10, (index - 1) // 10

    def get_adjacent_cells_pos(self, pos):
        adj_cells_pos = []
        for i in [-1, 1]:
            if 0 <= pos[0] + i <= 9:
                adj_cells_pos.append((pos[0] + i, pos[1]))
            if 0 <= pos[1] + i <= 9:
                adj_cells_pos.append((pos[0], pos[1] + i))
        return adj_cells_pos

    def infer_new_knowledge(self, new_percept):
        self.pos = new_percept.pos
        self.visited.append(new_percept.pos)

        cell_idx = self.convert_pos_to_index(new_percept.pos)
        if new_percept.breeze:
            self.knowledge_base.append([cell_idx])
        else:
            self.knowledge_base.append([-cell_idx])
        if new_percept.stench:
            self.knowledge_base.append([200 + cell_idx])
        else:
            self.knowledge_base.append([-(200 + cell_idx)])

        # WORK IN PROGRESS...
        # (Only ask if the adjacent cells are SAFE.)
        adj_cells_pos = self.get_adjacent_cells_pos(new_percept.pos)
        adj_cells_idx = [self.convert_pos_to_index(pos) for pos in adj_cells_pos]
        for adj_idx in adj_cells_idx:
            g = Glucose3()
            for clause in self.knowledge_base:
                g.add_clause(clause)
            g.add_clause([-(400 + adj_idx)])
            sol = g.solve()
            if not sol:
                self.knowledge_base.append([400 + adj_idx])

    def manhattan_distance(self, pos_1, pos_2):
        return abs(pos_1[0] - pos_2[0]) + abs(pos_1[1] - pos_2[1])

    def make_action(self):
        # WORK IN PROGRESS...
        # (Only make MOVE action, and only find safe and ADJACENT cell to move to.)
        safe_cells_idx = [clause[0] % 400 for clause in self.knowledge_base
                          if len(clause) == 1 and 401 <= clause[0] <= 500]
        safe_cells_pos = [self.convert_index_to_pos(idx) for idx in safe_cells_idx]


        next_cell_pos = ()
        for pos in safe_cells_pos:
            if self.manhattan_distance(self.pos, pos) == 1 and pos not in self.visited:
                next_cell_pos = pos
                break

        return next_cell_pos
