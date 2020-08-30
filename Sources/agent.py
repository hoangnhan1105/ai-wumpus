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

    def print_clause(self, clause):
        for i, literal in enumerate(clause):
            if self.BREEZE_OFFSET + 1 <= abs(literal) <= self.BREEZE_OFFSET + 100:
                if literal > 0:
                    print('Breeze(', literal, ')', sep='', end='')
                else:
                    print('NOT Breeze(', -literal, ')', sep='', end='')
            elif self.PIT_OFFSET + 1 <= abs(literal) <= self.PIT_OFFSET + 100:
                if literal > 0:
                    print('Pit(', literal % self.PIT_OFFSET, ')', sep='', end='')
                else:
                    print('NOT Pit(', -literal % self.PIT_OFFSET, ')', sep='', end='')
            elif self.STENCH_OFFSET + 1 <= abs(literal) <= self.STENCH_OFFSET + 100:
                if literal > 0:
                    print('Stench(', literal % self.STENCH_OFFSET, ')', sep='', end='')
                else:
                    print('NOT Stench(', -literal % self.STENCH_OFFSET, ')', sep='', end='')
            elif self.WUMPUS_OFFSET + 1 <= abs(literal) <= self.WUMPUS_OFFSET + 100:
                if literal > 0:
                    print('Wumpus(', literal % self.WUMPUS_OFFSET, ')', sep='', end='')
                else:
                    print('NOT Wumpus(', -literal % self.WUMPUS_OFFSET, ')', sep='', end='')
            elif self.SAFE_OFFSET + 1 <= abs(literal) <= self.SAFE_OFFSET + 100:
                if literal > 0:
                    print('Safe(', literal % self.SAFE_OFFSET, ')', sep='', end='')
                else:
                    print('NOT Safe(', -literal % self.SAFE_OFFSET, ')', sep='', end='')

            if i < len(clause) - 1:
                print(' OR ', end='')
            else:
                print('')

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
            cell_pos = self.convert_index_to_pos(i)
            adj_cells_pos = self.get_adjacent_cells_pos(cell_pos)
            adj_cells_idx = [self.convert_pos_to_index(pos) for pos in adj_cells_pos]

            clause_list = [[-(self.BREEZE_OFFSET + i)]]
            for adj_idx in adj_cells_idx:
                clause_list[0].append(self.PIT_OFFSET + adj_idx)
                clause_list.append([self.BREEZE_OFFSET + i, -(self.PIT_OFFSET + adj_idx)])
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
            cell_pos = self.convert_index_to_pos(i)
            adj_cells_pos = self.get_adjacent_cells_pos(cell_pos)
            adj_cells_idx = [self.convert_pos_to_index(pos) for pos in adj_cells_pos]

            clause_list = [[-(self.STENCH_OFFSET + i)]]
            for adj_idx in adj_cells_idx:
                clause_list[0].append(self.WUMPUS_OFFSET + adj_idx)
                clause_list.append([self.STENCH_OFFSET + i, -(self.WUMPUS_OFFSET + adj_idx)])
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

        print('Initial KB:')
        for clause in self.knowledge_base:
            self.print_clause(clause)
        print('')

    def perceive(self, raw_map, pos):
        new_percept = percept(pos=pos)
        if 'b' in raw_map[pos[1]][pos[0]]:
            new_percept.breeze = True
        if 's' in raw_map[pos[1]][pos[0]]:
            new_percept.stench = True
        return new_percept

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
        """
        # Frontier cell: an UNVISITED cell which is adjacent to at least one VISITED cell.
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

        # For each frontier cell, ask if it is SAFE.
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
