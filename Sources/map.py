from setting import *
from cell import *
import random

def input_raw(map_input_path):
    try:
        f = open(map_input_path, "r")
    except:
        print("Can not read file \'" + map_input_path + "\'. Please check again!")
        return None

    raw_map = [[cell.rstrip("\n") for cell in line.split('.')] for line in f]

    return raw_map

def raw_to_cells(raw_map):
    cells = []
    gold = 0


    for i in range(10):
        row = []
        for j in range(10):
            state = None

            if raw_map[i][j] == "b": state = CARD.BREEZE
            if raw_map[i][j][0] == "-": state = CARD.EMPTY
            if raw_map[i][j] == "g": state = CARD.GOLD
            if raw_map[i][j] == "gb": state = CARD.GOLD_BREEZE
            if raw_map[i][j] == "gs": state = CARD.GOLD_STENCH
            if raw_map[i][j] == "gbs": state = CARD.GOLD_STENCH_BREEZE
            if raw_map[i][j] == "p": state = CARD.HOLE
            if raw_map[i][j] == "ps": state = CARD.HOLE_STENCH
            if raw_map[i][j] == "pb": state = CARD.HOLE_BREEZE
            if raw_map[i][j] == "pbs": state = CARD.HOLE_STENCH_BREEZE
            if raw_map[i][j] == "s": state = CARD.STENCH
            if raw_map[i][j] == "bs": state = CARD.STENCH_BREEZE
            if raw_map[i][j] == "w": state = CARD.WUMPUS
            if raw_map[i][j] == "wb": state = CARD.WUMPUS_BREEZE
            if raw_map[i][j] == "ws": state = CARD.WUMPUS_STENCH
            if raw_map[i][j] == "wbs": state = CARD.WUMPUS_STENCH_BREEZE

            if raw_map[i][j] in ["g", "gb", "gbs", "gs"]: gold += 1

            # (j, i) == (x, y)
            row.append(cell((j, i), state))

        cells.append(row)

    return cells, gold

def random_knight_spawn(cells, visited):
    empty_pos = []

    for i in range(10):
        for j in range(10):
            if cells[i][j].state == CARD.EMPTY:
                empty_pos += [cells[i][j]]

    rand = random.choice(empty_pos)
    rand.knight_come()
    visited[rand.pos[1]][rand.pos[0]] = True

    return rand