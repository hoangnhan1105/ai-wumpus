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
    def __init__(self, pos=(), breeze=False, stench=False, scream=False):
        self.pos = pos
        self.breeze = breeze
        self.stench = stench
        self.scream = scream


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
        self.guiding_path = []
        # If guiding_path is not empty,
        # this is the action which will be perform when the agent
        # arrives at the end of guiding_path.
        self.pending_action = None
        # If the agent's previous action is shooting,
        # this is the target of that shot.
        self.prev_shoot_pos = ()

        self.init_kb()

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
                    # 200 % 100 == 0
                    idx = -literal % self.PIT_OFFSET
                    if idx == 0:
                        idx = 100
                    print('NOT Pit(', idx, ')', sep='', end='')
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

    def perceive(self, env_input):
        return env_input

    def infer_new_knowledge(self, new_percept):
        new_knowledge = []
        remove_knowledge = []

        self.pos = new_percept.pos
        if new_percept.pos not in self.visited:
            self.visited.append(new_percept.pos)

        if new_percept.scream:
            wumpus_clause = [self.WUMPUS_OFFSET + self.convert_pos_to_index(self.prev_shoot_pos)]
            self.knowledge_base.remove(wumpus_clause)
            remove_knowledge.append(wumpus_clause)

            adj_cells_pos = self.get_adjacent_cells_pos(self.prev_shoot_pos)
            for adj_pos in adj_cells_pos:
                if adj_pos not in self.visited:
                    continue
                stench_clause = [self.STENCH_OFFSET + self.convert_pos_to_index(adj_pos)]
                self.knowledge_base.remove(stench_clause)
                remove_knowledge.append(stench_clause)

            self.prev_shoot_pos = ()

        cell_idx = self.convert_pos_to_index(new_percept.pos)
        if new_percept.breeze:
            if [self.BREEZE_OFFSET + cell_idx] not in self.knowledge_base:
                self.knowledge_base.append([self.BREEZE_OFFSET + cell_idx])
                new_knowledge.append([self.BREEZE_OFFSET + cell_idx])
        else:
            if [-(self.BREEZE_OFFSET + cell_idx)] not in self.knowledge_base:
                self.knowledge_base.append([-(self.BREEZE_OFFSET + cell_idx)])
                new_knowledge.append([-(self.BREEZE_OFFSET + cell_idx)])

        if new_percept.stench:
            if [self.STENCH_OFFSET + cell_idx] not in self.knowledge_base:
                self.knowledge_base.append([self.STENCH_OFFSET + cell_idx])
                new_knowledge.append([self.STENCH_OFFSET + cell_idx])
        else:
            if [-(self.STENCH_OFFSET + cell_idx)] not in self.knowledge_base:
                self.knowledge_base.append([-(self.STENCH_OFFSET + cell_idx)])
                new_knowledge.append([-(self.STENCH_OFFSET + cell_idx)])
                if [self.STENCH_OFFSET + cell_idx] in self.knowledge_base:
                    self.knowledge_base.remove([self.STENCH_OFFSET + cell_idx])
                    remove_knowledge.append([self.STENCH_OFFSET + cell_idx])

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

        # For each frontier cell, ask if there's a WUMPUS in that cell.
        found_wumpus = False
        for frontier_idx in frontier_cells_idx:
            if [self.WUMPUS_OFFSET + frontier_idx] in self.knowledge_base:
                continue
            g = Glucose3()
            for clause in self.knowledge_base:
                g.add_clause(clause)
            g.add_clause([-(self.WUMPUS_OFFSET + frontier_idx)])
            sol = g.solve()
            if not sol:
                self.knowledge_base.append([self.WUMPUS_OFFSET + frontier_idx])
                new_knowledge.append([self.WUMPUS_OFFSET + frontier_idx])
                found_wumpus = True
        if found_wumpus:
            print('* At ', self.pos, ' :', sep='')
            print('- New knowledge:')
            for clause in new_knowledge:
                self.print_clause(clause)
            print('- Removed knowledge:')
            for clause in remove_knowledge:
                self.print_clause(clause)
            print('')
            return

        # If there's no wumpus in any frontier cell, continue.
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
                new_knowledge.append([self.SAFE_OFFSET + frontier_idx])

        print('* At ', self.pos, ' :', sep='')
        print('- New knowledge:')
        for clause in new_knowledge:
            self.print_clause(clause)
        print('- Removed knowledge:')
        for clause in remove_knowledge:
            self.print_clause(clause)
        print('')

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

        wumpus_cells_idx = [clause[0] % self.WUMPUS_OFFSET for clause in self.knowledge_base
                            if len(clause) == 1
                            and self.WUMPUS_OFFSET + 1 <= clause[0] <= self.WUMPUS_OFFSET + 100]
        wumpus_cells_pos = [self.convert_index_to_pos(idx) for idx in wumpus_cells_idx]
        path = self.find_path(wumpus_cells_pos)
        if path:
            path.pop(0)  # First element is the current cell
            if len(path) > 1:  # If the wumpus cell is not adjacent to agent cell
                self.guiding_path = path
                self.pending_action = AGENT_ACTION.SHOOT
                action = AGENT_ACTION.MOVE
                next_cell_pos = path[0]
            else:
                action = AGENT_ACTION.SHOOT
                next_cell_pos = path[0]
            return action, next_cell_pos

        # If there's no wumpus in any frontier cell...
        safe_cells_idx = [clause[0] % self.SAFE_OFFSET for clause in self.knowledge_base
                          if len(clause) == 1
                          and self.SAFE_OFFSET + 1 <= clause[0] <= self.SAFE_OFFSET + 100]
        safe_cells_pos = [self.convert_index_to_pos(idx) for idx in safe_cells_idx]
        safe_unvisited_cells_pos = [cell for cell in safe_cells_pos if cell not in self.visited]

        path = self.find_path(safe_unvisited_cells_pos)
        if path:
            path.pop(0)
            if len(path) > 1:  # If the safe unvisited cell is not adjacent to agent cell
                self.guiding_path = path
                action = AGENT_ACTION.MOVE
                next_cell_pos = path[0]
            else:
                action = AGENT_ACTION.MOVE
                next_cell_pos = path[0]
            return action, next_cell_pos

        # If there's also no safe unvisited cell among the frontier cells...
        path = self.find_path([self.START_POS])  # Get out of the cave
        path.pop(0)
        if len(path) > 0:  # If the agent cell is not the exit
            self.guiding_path = path
            self.pending_action = AGENT_ACTION.CLIMB
            action = AGENT_ACTION.MOVE
            next_cell_pos = path[0]
        else:
            action = AGENT_ACTION.CLIMB
            next_cell_pos = ()

        return action, next_cell_pos

    def work(self, env_input):
        action = None
        next_cell_pos = ()

        if not self.guiding_path:  # Agent doesn't have a predetermined path
            new_percept = self.perceive(env_input)
            self.infer_new_knowledge(new_percept)
            action, next_cell_pos = self.make_action()
        else:  # Agent is following a predetermined path
            if self.pending_action is None:
                if len(self.guiding_path) > 2:
                    self.guiding_path.pop(0)
                    action = AGENT_ACTION.MOVE
                    next_cell_pos = self.guiding_path[0]
                else:
                    action = AGENT_ACTION.MOVE
                    next_cell_pos = self.guiding_path[1]
                    self.guiding_path = []
                    self.pending_action = None
            elif self.pending_action == AGENT_ACTION.SHOOT:
                # If agent isn't standing next to the wumpus.
                if len(self.guiding_path) > 2:
                    self.guiding_path.pop(0)
                    action = AGENT_ACTION.MOVE
                    next_cell_pos = self.guiding_path[0]
                # Agent is standing next to the wumpus, and can shoot it now.
                else:
                    action = AGENT_ACTION.SHOOT
                    next_cell_pos = self.guiding_path[1]
                    self.guiding_path = []
                    self.pending_action = None
                    self.prev_shoot_pos = next_cell_pos
            elif self.pending_action == AGENT_ACTION.CLIMB:
                if len(self.guiding_path) > 1:
                    self.guiding_path.pop(0)
                    action = AGENT_ACTION.MOVE
                    next_cell_pos = self.guiding_path[0]
                else:
                    action = AGENT_ACTION.CLIMB
                    next_cell_pos = self.guiding_path[0]
                    self.guiding_path = []
                    self.pending_action = None

        return action, next_cell_pos
