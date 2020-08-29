# 1..100: Breeze
# 101..200: Pit
# 201..300: Stench
# 301..400: Wumpus
# 401..500: Safe

import enum
import queue
from pysat.solvers import Glucose3


class AGENT_ACTION(enum.Enum):
    MOVE = 0
    SHOOT = 1
    CLIMB = 2


class percept:
    def __init__(self, pos=(), breeze=False, stench=False):
        self.pos = pos
        self.breeze = breeze
        self.stench = stench


class agent:
    BREEZE_OFFSET = 0
    PIT_OFFSET = 100
    STENCH_OFFSET = 200
    WUMPUS_OFFSET = 300
    SAFE_OFFSET = 400

    def __init__(self, start_pos):
        self.START_POS = start_pos
        self.knowledge_base = []
        self.pos = ()
        self.visited = []
        self.path = []

    def init_kb(self):
        self.knowledge_base = []

        # Breeze(x, y) <=> Pit(x, y - 1) v Pit(x - 1, y) v Pit(x + 1, y) v Pit(x, y + 1)
        # Equivalent to:
        # ~Breeze(x, y) v Pit(x, y - 1) v Pit(x - 1, y) v Pit(x + 1, y) v Pit(x, y + 1)
        # ^
        # Breeze(x, y) v ~Pit(x, y - 1)
        # ^
        # Breeze(x, y) v ~Pit(x - 1, y)
        # ^
        # Breeze(x, y) v ~Pit(x + 1, y)
        # ^
        # Breeze(x, y) v ~Pit(x, y + 1)
        for i in range(1, 101):
            clause_list = [[-(self.BREEZE_OFFSET + i)]]
            for j in [-10, -1, 1, 10]:
                if 1 <= i + j <= 100:
                    clause_list[0].append(self.PIT_OFFSET + i + j)
                    clause_list.append([i, -(self.PIT_OFFSET + i + j)])
            self.knowledge_base += clause_list

        # Stench(x, y) <=> Wumpus(x, y - 1) v Wumpus(x - 1, y) v Wumpus(x + 1, y) v Wumpus(x, y + 1)
        # Equivalent to:
        # ~Stench(x, y) v Wumpus(x, y - 1) v Wumpus(x - 1, y) v Wumpus(x + 1, y) v Wumpus(x, y + 1)
        # ^
        # Stench(x, y) v ~Wumpus(x, y - 1)
        # ^
        # Stench(x, y) v ~Wumpus(x - 1, y)
        # ^
        # Stench(x, y) v ~Wumpus(x + 1, y)
        # ^
        # Stench(x, y) v ~Wumpus(x, y + 1)
        for i in range(1, 101):
            clause_list = [[-(self.STENCH_OFFSET + i)]]
            for j in [-10, -1, 1, 10]:
                if 1 <= i + j <= 100:
                    clause_list[0].append(self.WUMPUS_OFFSET + i + j)
                    clause_list.append([self.STENCH_OFFSET + i, -(self.WUMPUS_OFFSET + i + j)])
            self.knowledge_base += clause_list

        # ~Pit(x, y) ^ ~Wumpus(x, y) <=> Safe(x, y)
        # Equivalent to:
        # Pit(x, y) v Wumpus(x, y) v Safe(x, y)
        # ^
        # ~Safe(x, y) v ~Pit(x, y)
        # ^
        # ~Safe(x, y) v ~Wumpus(x, y)
        for i in range(1, 101):
            self.knowledge_base.append(
                [self.PIT_OFFSET + i, self.WUMPUS_OFFSET + i, self.SAFE_OFFSET + i])
            self.knowledge_base.append([-(self.SAFE_OFFSET + i), -(self.PIT_OFFSET + i)])
            self.knowledge_base.append([-(self.SAFE_OFFSET + i), -(self.WUMPUS_OFFSET + i)])

        start_idx = self.convert_pos_to_index(self.START_POS)
        self.knowledge_base.append([self.SAFE_OFFSET + start_idx])

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
            self.knowledge_base.append([self.BREEZE_OFFSET + cell_idx])
        else:
            self.knowledge_base.append([-(self.BREEZE_OFFSET + cell_idx)])
        if new_percept.stench:
            self.knowledge_base.append([self.STENCH_OFFSET + cell_idx])
        else:
            self.knowledge_base.append([-(self.STENCH_OFFSET + cell_idx)])

        # <WORK IN PROGRESS>
        """
        adj_cells_pos = self.get_adjacent_cells_pos(new_percept.pos)
        adj_cells_idx = [self.convert_pos_to_index(pos) for pos in adj_cells_pos]
        
        # Ask if there is a WUMPUS in adjacent cells.
        for adj_idx in adj_cells_idx:
            g = Glucose3()
            for clause in self.knowledge_base:
                g.add_clause(clause)
            g.add_clause([-(self.WUMPUS_OFFSET + adj_idx)])
            sol = g.solve()
            if not sol:
                self.knowledge_base.append([self.WUMPUS_OFFSET + adj_idx])
        
        # Ask if there is a SAFE cell among adjacent cells.
        for adj_idx in adj_cells_idx:
            g = Glucose3()
            for clause in self.knowledge_base:
                g.add_clause(clause)
            g.add_clause([-(self.SAFE_OFFSET + adj_idx)])
            sol = g.solve()
            if not sol:
                self.knowledge_base.append([self.SAFE_OFFSET + adj_idx])
        """
        frontier_cells_pos = []
        for y in range(10):
            for x in range(10):
                if (x, y) in self.visited:
                    continue
                adj_list = self.get_adjacent_cells_pos((x, y))
                adj_visited_list = [adj for adj in adj_list if adj in self.visited]
                if len(adj_visited_list) > 0:
                    frontier_cells_pos.append((x, y))
        frontier_cells_idx = [self.convert_pos_to_index(pos) for pos in frontier_cells_pos]

        for frontier_idx in frontier_cells_idx:
            if [self.SAFE_OFFSET + frontier_idx] in self.knowledge_base:
                continue
            g = Glucose3()
            for clause in self.knowledge_base:
                g.add_clause(clause)
            g.add_clause([-(self.SAFE_OFFSET + frontier_idx)])
            sol = g.solve()
            if not sol:
                self.knowledge_base.append([self.SAFE_OFFSET + frontier_idx])

        # </WORK IN PROGRESS>

    def manhattan_distance(self, pos_1, pos_2):
        return abs(pos_1[0] - pos_2[0]) + abs(pos_1[1] - pos_2[1])

    def find_path(self, destination_list_pos):
        node = self.pos
        if node in destination_list_pos:
            return [node]

        frontier = queue.Queue()
        frontier.put(node)
        explored = []
        parent_list = [[() for j in range(10)] for i in range(10)]

        while True:
            if frontier.empty():
                return []
            node = frontier.get()
            explored.append(node)

            adj_pos = self.get_adjacent_cells_pos(node)
            for child in adj_pos:
                if (child not in explored) and (child not in frontier.queue):
                    if child in destination_list_pos:
                        explored.append(child)
                        path = [child]
                        parent = node
                        while parent:
                            path.insert(0, parent)
                            parent = parent_list[parent[1]][parent[0]]
                        return path
                    if child in self.visited:
                        frontier.put(child)
                        parent_list[child[1]][child[0]] = node

    def make_action(self):
        action = None
        next_cell_pos = ()

        safe_cells_idx = [clause[0] % self.SAFE_OFFSET for clause in self.knowledge_base
                          if len(clause) == 1
                          and self.SAFE_OFFSET + 1 <= clause[0] <= self.SAFE_OFFSET + 100]
        safe_cells_pos = [self.convert_index_to_pos(idx) for idx in safe_cells_idx]
        safe_unvisited_cells_pos = [cell for cell in safe_cells_pos if cell not in self.visited]

        path = self.find_path(safe_unvisited_cells_pos)
        if not path:  # No safe way to go
            path = self.find_path([self.START_POS])  # Get out of the cave
        path.pop(0)  # First element is the current cell

        if len(path) > 0:
            action = AGENT_ACTION.MOVE
            next_cell_pos = path[0]
            if len(path) > 1:
                self.path = path
        else:
            action = AGENT_ACTION.CLIMB
            next_cell_pos = ()

        return action, next_cell_pos

    def work(self, raw_map, pos):
        action = None
        next_cell_pos = ()

        if len(self.path) == 1:  # Agent has a predetermined path and has arrived at the destination
            self.path.pop(0)
        if not self.path:  # Agent doesn't have predetermined path
            new_percept = self.perceive(raw_map, pos)
            self.infer_new_knowledge(new_percept)
            action, next_cell_pos = self.make_action()
        else:  # Agent is following the predetermined path
            action = AGENT_ACTION.MOVE
            self.path.pop(0)
            next_cell_pos = self.path[0]
        return action, next_cell_pos
