import pygame
import enum

class CARD(enum.Enum):
    BREEZE = 0
    BUSH = 1
    EMPTY = 2
    GOLD = 3
    GOLD_BREEZE = 4
    GOLD_STENCH = 5
    GOLD_STENCH_BREEZE = 6
    HOLE = 7
    HOLE_BREEZE = 8
    HOLE_STENCH = 9
    HOLE_STENCH_BREEZE = 10
    KILL = 11
    KILL_BREEZE = 12
    KILL_STENCH = 13
    KILL_STENCH_BREEZE = 14
    KNIGHT = 15
    KNIGHT_BREEZE = 16
    KNIGHT_STENCH = 17
    KNIGHT_STENCH_BREEZE = 18
    STENCH = 19
    STENCH_BREEZE = 20
    WUMPUS = 21
    WUMPUS_BREEZE = 22
    WUMPUS_STENCH = 23
    WUMPUS_STENCH_BREEZE = 24
    START = 25


# Card
WIDTH_CARD = 80
IMG_CARD = [r"../Assets/Cards/breeze.png",
            r"../Assets/Cards/bush.png",
            r"../Assets/Cards/empty.png",
            r"../Assets/Cards/gold.png",
            r"../Assets/Cards/gold_breeze.png",
            r"../Assets/Cards/gold_stench.png",
            r"../Assets/Cards/gold_stench_breeze.png",
            r"../Assets/Cards/hole.png",
            r"../Assets/Cards/hole_breeze.png",
            r"../Assets/Cards/hole_stench.png",
            r"../Assets/Cards/hole_stench_breeze.png",
            r"../Assets/Cards/kill.png",
            r"../Assets/Cards/kill_breeze.png",
            r"../Assets/Cards/kill_stench.png",
            r"../Assets/Cards/kill_stench_breeze.png",
            r"../Assets/Cards/knight.png",
            r"../Assets/Cards/knight_breeze.png",
            r"../Assets/Cards/knight_stench.png",
            r"../Assets/Cards/knight_stench_breeze.png",
            r"../Assets/Cards/stench.png",
            r"../Assets/Cards/stench_breeze.png",
            r"../Assets/Cards/wumpus.png",
            r"../Assets/Cards/wumpus_breeze.png",
            r"../Assets/Cards/wumpus_stench.png",
            r"../Assets/Cards/wumpus_stench_breeze.png",
            r"../Assets/Cards/start.png"]

# Window
WIDTH, HEIGHT = 900, 900
CAPTION = r"Wumpus"
FPS = 60


# Image
IMG_MENU = r"../Assets/game_menu.png"
IMG_ICON = r"../Assets/icon.png"
IMG_WUMPUS = r"../Assets/wumpus.png"
IMG_BACKGROUND = r"../Assets/bg.jpg"

# Map
MAP = [r"../Maps/map1.txt"]

# Sword
IMG_SWORD = [r"../Assets/sword_up.png",
             r"../Assets/sword_down.png",
             r"../Assets/sword_left.png",
             r"../Assets/sword_right.png"]

# Button
TEXT_SIZE_MENU = 44
TEXT_COLOR = BUTTON_BORDER_COLOR = TEXT_MENU_COLOR = BUTTON_MENU_BORDER_COLOR = "#000000"
TEXT_COLOR_OVER = BUTTON_BORDER_COLOR_OVER = TEXT_MENU_COLOR_OVER = BUTTON_MENU_BORDER_COLOR_OVER = "#eaedff"
BUTTON_COLOR = BUTTON_MENU_COLOR = "#eaedff"
BUTTON_COLOR_OVER = BUTTON_MENU_COLOR_OVER = "#b5b9ff"

RECT_LETSGO = (75, 340, 300, 75)
RECT_CHOOSEMAP = (75, 460, 300, 75)
RECT_TUTORIAL = (75, 580, 300, 75)
RECT_EXIST = (75, 700, 300, 75)

TEXT_SIZE_BACKLETSGO = 28
RECT_BACKLETSGO = (810,865,80,25)



# Score frame
TEXT_SIZE_SCORE = 26
TEXT_SCORE_COLOR = "#000000"
BUTTON_SCORE_COLOR = "#eaedff"

RECT_SCORE = (10, 860, 150, 35)

# Knight move animation
DISTANCE_CARD = 85
KNIGHT_MOVE_PIXELS_PER_STEP = 5

# Shoot animation
DISTANCE_SHOOT = 52
SHOOT_PIXELS_PER_STEP = 4

# Game score
PEN_DIE = -10000
PEN_SHOOTING_ARROW = -100
PEN_MOVE = -10
SCORE_PICKING_GOLD = 100
SCORE_CLIMBING_OUT = 10
SCORE_KILL_WUMPUS = 1000