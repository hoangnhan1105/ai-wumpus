from setting import *

class cell:
    def __init__(self, pos, state):
        self.pos = pos
        self.state = state
        self.prev_state = state

    def knight_come(self):
        res = PEN_MOVE

        if self.state in [CARD.GOLD, CARD.GOLD_BREEZE, CARD.GOLD_STENCH, CARD.GOLD_STENCH_BREEZE]:
            self.gold_colected()
            res += SCORE_PICKING_GOLD

        if self.state == CARD.GOLD or self.state == CARD.EMPTY or self.state == CARD.KILL or self.state == CARD.START:
            self.state = CARD.KNIGHT

        if self.state == CARD.GOLD_BREEZE or self.state == CARD.KILL_BREEZE or self.state == CARD.BREEZE:
            self.state = CARD.KNIGHT_BREEZE

        if self.state == CARD.GOLD_STENCH or self.state == CARD.KILL_STENCH or self.state == CARD.STENCH:
            self.state = CARD.KNIGHT_STENCH

        if self.state == CARD.GOLD_STENCH_BREEZE or self.state == CARD.KILL_STENCH_BREEZE or self.state == CARD.STENCH_BREEZE:
            self.state = CARD.KNIGHT_STENCH_BREEZE

        if self.state in [CARD.HOLE, CARD.HOLE_BREEZE, CARD.HOLE_STENCH, CARD.HOLE_STENCH_BREEZE,
                          CARD.WUMPUS, CARD.WUMPUS_BREEZE, CARD.WUMPUS_STENCH, CARD.WUMPUS_STENCH_BREEZE]:
            res += PEN_DIE

        return res

    def knight_leave(self):
        self.state = self.prev_state

    def gold_colected(self):
        if self.state == CARD.GOLD:
            self.prev_state = self.state = CARD.EMPTY

        if self.state == CARD.GOLD_BREEZE:
            self.prev_state = self.state = CARD.BREEZE

        if self.state == CARD.GOLD_STENCH:
            self.prev_state = self.state = CARD.STENCH

        if self.state == CARD.GOLD_STENCH_BREEZE:
            self.prev_state = self.state = CARD.STENCH_BREEZE

    def wumpus_killed(self):
        if self.state == CARD.WUMPUS:
            self.prev_state = self.state = CARD.KILL

        if self.state == CARD.WUMPUS_BREEZE:
            self.prev_state = self.state = CARD.KILL_BREEZE

        if self.state == CARD.WUMPUS_STENCH:
            self.prev_state = self.state = CARD.KILL_STENCH

        if self.state == CARD.WUMPUS_STENCH_BREEZE:
            self.prev_state = self.state = CARD.KILL_STENCH_BREEZE

        return SCORE_KILL_WUMPUS

    def is_wumpus_exist(self):
        return self.state in [CARD.WUMPUS, CARD.WUMPUS_BREEZE, CARD.WUMPUS_STENCH, CARD.WUMPUS_STENCH_BREEZE]

    def is_gold_exist(self):
        return self.state in [CARD.GOLD, CARD.GOLD_BREEZE, CARD.GOLD_STENCH, CARD.GOLD_STENCH_BREEZE]

    def is_hole_exist(self):
        return self.state in [CARD.HOLE, CARD.HOLE_BREEZE, CARD.HOLE_STENCH, CARD.HOLE_STENCH_BREEZE]

    def set_spawn(self):
        self.state = self.prev_state = CARD.START

    def is_able_to_escape(self):
        return self.state == CARD.START

    def remove_stench(self):
        new_state = None

        if self.state == CARD.STENCH:
            new_state = CARD.EMPTY
        if self.state == CARD.GOLD_STENCH:
            new_state = CARD.GOLD
        if self.state == CARD.STENCH_BREEZE:
            new_state = CARD.BREEZE
        if self.state == CARD.KILL_STENCH:
            new_state = CARD.KILL

        if self.state == self.prev_state:
            self.state = self.prev_state = new_state

        if self.state == CARD.KNIGHT_STENCH:
            self.prev_state = CARD.EMPTY
            self.state = CARD.KNIGHT

        if self.state == CARD.KNIGHT_STENCH_BREEZE:
            self.prev_state = CARD.BREEZE
            self.state = CARD.KNIGHT_BREEZE


