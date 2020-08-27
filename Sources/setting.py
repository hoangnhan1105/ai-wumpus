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

re = 0.8

# Card
WIDTH_CARD = int(80 * re)
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
WIDTH, HEIGHT = int(900 * re), int(900 * re)
CAPTION = r"Wumpus"


# Image
IMG_MENU = r"../Assets/game_menu.png"
IMG_ICON_WUMPUS = r"../Assets/icon_wumpus.png"
IMG_ICON_GOLD = r"../Assets/icon_gold.png"
IMG_ICON_SCORE = r"../Assets/icon_score.png"
IMG_WUMPUS = r"../Assets/wumpus.png"
IMG_BACKGROUND = r"../Assets/bg.jpg"
IMG_VICTORY = r"../Assets/victory.png"
IMG_LOSE = r"../Assets/lose.png"

# Map
MAP = [r"../Maps/map1.txt",
       r"../Maps/map2.txt",
       r"../Maps/map3.txt",
       r"../Maps/map4.txt",
       r"../Maps/map5.txt"]

IMG_MAP = [r"../Assets/Maps/map1.png",
           r"../Assets/Maps/map2.png",
           r"../Assets/Maps/map3.png",
           r"../Assets/Maps/map4.png",
           r"../Assets/Maps/map5.png"]

# Sword
IMG_SWORD = [r"../Assets/sword_up.png",
             r"../Assets/sword_down.png",
             r"../Assets/sword_left.png",
             r"../Assets/sword_right.png"]

# Button
TEXT_SIZE_MENU = int(44 * re)
TEXT_COLOR = BUTTON_BORDER_COLOR = TEXT_MENU_COLOR = BUTTON_MENU_BORDER_COLOR = "#000000"
TEXT_COLOR_OVER = BUTTON_BORDER_COLOR_OVER = TEXT_MENU_COLOR_OVER = BUTTON_MENU_BORDER_COLOR_OVER = "#eaedff"
BUTTON_COLOR = BUTTON_MENU_COLOR = "#eaedff"
BUTTON_COLOR_OVER = BUTTON_MENU_COLOR_OVER = "#b5b9ff"

RECT_LETSGO = (int(75 * re), int(340 * re), int(300 * re), int(75 * re))
RECT_CHOOSEMAP = (int(75 * re), int(460 * re), int(300 * re), int(75 * re))
RECT_TUTORIAL = (int(75 * re), int(580 * re), int(300 * re), int(75 * re))
RECT_EXIST = (int(75 * re), int(700 * re), int(300 * re), int(75 * re))

TEXT_SIZE_BACKLETSGO = int(28 * re)
RECT_BACKLETSGO = (int(810 * re), int(865 * re), int(80 * re), int(25 * re))
TEXT_SIZE_SUB = int(18 * re)
RECT_PREV = (int(315 * re), int(870 * re), int(60 * re), int(15 * re))
RECT_SELECT = (int(385 * re), int(865 * re), int(150 * re), int(25 * re))
RECT_NEXT = (int(545 * re), int(870 * re), int(60 * re), int(15 * re))



# Score frame
TEXT_SIZE_SCORE = int(26 * re)
TEXT_SCORE_COLOR = "#000000"
BUTTON_SCORE_COLOR = "#eaedff"

RECT_SCORE = (int(10 * re), int(860 * re), int(150 * re), int(35 * re))

# Knight move animation
DISTANCE_CARD = int(85 * re)
KNIGHT_MOVE_PIXELS_PER_STEP = int(5 * re)

# Shoot animation
DISTANCE_SHOOT = 42 #int(52 * re)
SHOOT_PIXELS_PER_STEP = 2

# Game score
PEN_DIE = -10000
PEN_SHOOTING_ARROW = -100
PEN_MOVE = -10
SCORE_PICKING_GOLD = 100
SCORE_CLIMBING_OUT = 10
SCORE_KILL_WUMPUS = 1000

LETSGO = "letsgo"
CHOOSEMAP = "choosemap"
MENU = "menu"
VICTORY = "victory"
LOSE = "lose"
