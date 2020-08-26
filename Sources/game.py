import sys
import pygame.freetype
from cell import *
from map import *
from setting import *

pygame.init()


class button:
    # rect = (x, y),
    # size = (width, height)

    def __init__(self, screen, button_color, text_color, outline_color,  rect, text_size, text=''):
        self.button_color = button_color
        self.text_color = text_color
        self.x, self.y, self.width, self.height = rect
        self.text = text
        self.screen = screen
        self.text_size = text_size
        self.outline_color = outline_color


    def draw(self, outline = False):
        # Call this method to draw the button on the screen
        if outline:
            self.AAfilledRoundedRect((self.x - 3, self.y - 3, self.width + 6, self.height + 6), self.outline_color)

        self.AAfilledRoundedRect((self.x, self.y, self.width, self.height), self.button_color)

        if self.text != '':
            font = pygame.font.SysFont('roboto', self.text_size)
            text = font.render(self.text, 1, pygame.Color(self.text_color))
            self.screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

    def AAfilledRoundedRect(self, rect, color, radius=0.4):

        """
        AAfilledRoundedRect(surface,rect,color,radius=0.4)

        surface : destination
        rect    : rectangle
        color   : rgb or rgba
        radius  : 0 <= radius <= 1
        """

        rect = pygame.Rect(rect)
        color = pygame.Color(color)
        alpha = color.a
        color.a = 0
        pos = rect.topleft
        rect.topleft = 0, 0
        rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

        circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
        pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
        circle = pygame.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

        radius = rectangle.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle, radius)
        radius.topright = rect.topright
        rectangle.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, radius)

        rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

        rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
        rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

        return self.screen.blit(rectangle, pos)

class game:

    def __init__(self):

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Catiop and Icon
        self.caption = pygame.display.set_caption(CAPTION)
        load_icon = pygame.image.load(IMG_ICON)
        self.icon = pygame.display.set_icon(load_icon)

        # Background
        self.background = pygame.image.load(IMG_BACKGROUND).convert()

        # Menu
        self.menu = pygame.image.load(IMG_MENU).convert()
        self.button_letsgo = button( self.screen, BUTTON_MENU_COLOR, TEXT_MENU_COLOR, BUTTON_MENU_BORDER_COLOR, RECT_LETSGO, TEXT_SIZE_MENU,  "LET'S GO")
        self.button_choosemap = button( self.screen, BUTTON_MENU_COLOR, TEXT_MENU_COLOR, BUTTON_MENU_BORDER_COLOR, RECT_CHOOSEMAP, TEXT_SIZE_MENU,  "CHOOSE MAP")
        self.button_tutorial = button(self.screen, BUTTON_MENU_COLOR, TEXT_MENU_COLOR, BUTTON_MENU_BORDER_COLOR, RECT_TUTORIAL, TEXT_SIZE_MENU, "TUTORIAL")
        self.button_exist = button(self.screen, BUTTON_MENU_COLOR, TEXT_MENU_COLOR, BUTTON_MENU_BORDER_COLOR, RECT_EXIST, TEXT_SIZE_MENU, "EXIT")

        # Cards
        self.cards = [pygame.image.load(IMG_CARD[i]) for i in range(len(IMG_CARD))]

        # Sword
        self.sword = [pygame.image.load(IMG_SWORD[i]) for i in range(len(IMG_SWORD))]

        # Game score
        self.score = 0

        # Gold remaining
        self.gold = 0

        # Back button (playing)
        self.button_backletsgo = button( self.screen, BUTTON_COLOR, TEXT_COLOR, BUTTON_BORDER_COLOR, RECT_BACKLETSGO, TEXT_SIZE_BACKLETSGO,  "BACK")


    def to_scr_pos(self, pos, add_x=0, add_y=0, shoot=False):
        if shoot:
            if add_x != 0:
                return (27 + pos[0] * (WIDTH_CARD + 5) + add_x + WIDTH_CARD/2 , 10 + pos[1] * (WIDTH_CARD + 5) + add_y + WIDTH_CARD/2 - 16)
            if add_y != 0:
                return (27 + pos[0] * (WIDTH_CARD + 5) + add_x + WIDTH_CARD/2 - 16 , 10 + pos[1] * (WIDTH_CARD + 5) + add_y + WIDTH_CARD/2)

        return (27 + pos[0] * (WIDTH_CARD + 5) + add_x, 10 + pos[1] * (WIDTH_CARD + 5) + add_y)


    def draw_cell(self, cell):
        self.screen.blit(self.cards[cell.state.value], self.to_scr_pos(cell.pos))


    def draw_map(self, cells):
        for row in cells:
            for cell in row:
                self.draw_cell(cell)


    def draw_bush(self, visited):
        for i in range(10):
            for j in range(10):
                if not visited[i][j]:
                    self.screen.blit(self.cards[CARD.BUSH.value], self.to_scr_pos((j, i)))


    def draw_frame_game(self, visited, cells):
        self.screen.blit(self.background, [0, 0])
        self.draw_map(cells)
        self.draw_bush(visited)
        self.button_backletsgo.draw(True)

        font = pygame.font.SysFont("comicsansms", TEXT_SIZE_SCORE)
        text = font.render("SCORE: " + str(self.score), True, (0,0,0))
        self.screen.blit(text, (10, 860))
        text = font.render("GOLD REMAINING: " + str(self.gold), True, (0,0,0))
        self.screen.blit(text, (305, 860))


    def knight_move_animation(self, knight, des_pos, visited, cells):
        running = True
        des_cell = cells[des_pos[1]][des_pos[0]]

        # Open the cell that knight move to
        visited[des_pos[1]][des_pos[0]] = True
        self.draw_frame_game(visited, cells)
        pygame.display.update()

        # Knight move animation
        knight.knight_leave()
        moved = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                mouse_pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_backletsgo.isOver(mouse_pos):
                        running = False

                if event.type == pygame.MOUSEMOTION:
                    if self.button_backletsgo.isOver(mouse_pos):
                        self.button_backletsgo.outline_color = BUTTON_BORDER_COLOR_OVER
                        self.button_backletsgo.text_color = TEXT_COLOR_OVER
                        self.button_backletsgo.button_color = BUTTON_COLOR_OVER
                    else:
                        self.button_backletsgo.outline_color = BUTTON_BORDER_COLOR
                        self.button_backletsgo.text_color = TEXT_COLOR
                        self.button_backletsgo.button_color = BUTTON_COLOR

            self.draw_frame_game(visited, cells)

            # RIGHT or DOWN
            if des_pos[0] > knight.pos[0] or des_pos[1] > knight.pos[1] : moved += KNIGHT_MOVE_PIXELS_PER_STEP
            # LEFT or UP
            else: moved -= KNIGHT_MOVE_PIXELS_PER_STEP

            # UP or DOWN
            if des_pos[0] == knight.pos[0]: self.screen.blit(self.cards[CARD.KNIGHT.value], self.to_scr_pos(knight.pos, add_y=moved))
            # LEFT or RIGHT
            else: self.screen.blit(self.cards[CARD.KNIGHT.value], self.to_scr_pos(knight.pos, add_x=moved))

            pygame.display.update()

            pygame.time.delay(30)
            if moved == -DISTANCE_CARD or moved == DISTANCE_CARD : break


        # Knight come to the cell
        knight = des_cell

        if knight.is_gold_exist():
            self.gold -= 1

        score = knight.knight_come()
        self.draw_frame_game(visited, cells)
        pygame.display.update()


        # Update game score
        self.score += score

        if knight.is_wumpus_exist() or knight.is_hole_exist():
            knight = None

        pygame.time.delay(500)
        return knight, running


    def sword_shoot_animation(self, knight, des_pos, visited, cells):
        running = True
        des_cell = cells[des_pos[1]][des_pos[0]]
        self.score += PEN_SHOOTING_ARROW

        # Open the cell that containt wumpus
        if des_cell.is_wumpus_exist():
            visited[des_pos[1]][des_pos[0]] = True
            self.draw_frame_game(visited, cells)
            pygame.display.update()

        # Shoot animation
        moved = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                mouse_pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_backletsgo.isOver(mouse_pos):
                        running = False

                if event.type == pygame.MOUSEMOTION:
                    if self.button_backletsgo.isOver(mouse_pos):
                        self.button_backletsgo.outline_color = BUTTON_BORDER_COLOR_OVER
                        self.button_backletsgo.text_color = TEXT_COLOR_OVER
                        self.button_backletsgo.button_color = BUTTON_COLOR_OVER
                    else:
                        self.button_backletsgo.outline_color = BUTTON_BORDER_COLOR
                        self.button_backletsgo.text_color = TEXT_COLOR
                        self.button_backletsgo.button_color = BUTTON_COLOR

            self.draw_frame_game(visited, cells)

            # RIGHT or DOWN
            if des_pos[0] > knight.pos[0] or des_pos[1] > knight.pos[1]:
                moved += SHOOT_PIXELS_PER_STEP
                if des_pos[0] > knight.pos[0]: sword = self.sword[3]
                else: sword = self.sword[1]

            # LEFT or UP
            else:
                moved -= SHOOT_PIXELS_PER_STEP
                if des_pos[0] < knight.pos[0]: sword = self.sword[2]
                else: sword = self.sword[0]


            # UP or DOWN
            if des_pos[0] == knight.pos[0]: self.screen.blit(sword, self.to_scr_pos(knight.pos, add_y=moved, shoot=True))
            # LEFT or RIGHT
            else: self.screen.blit(sword, self.to_scr_pos(knight.pos, add_x=moved, shoot=True))

            pygame.display.update()

            pygame.time.delay(10)
            if moved == -DISTANCE_SHOOT or moved == DISTANCE_SHOOT: break

        # Wumpus die
        if des_cell.is_wumpus_exist():
            score = des_cell.wumpus_killed()
            self.draw_frame_game(visited, cells)
            pygame.display.update()

        # Update game score
        self.score += score

        pygame.time.delay(500)

        return running


    def letsgo(self):
        # Init a visited list show that the KNIGHT pass the cell yet?
        visited = [[False for _ in range(10)] for _ in range(10)]

        # Create cell, number of gold on the map
        raw_map = input_raw(MAP[0])
        cells, self.gold = raw_to_cells(raw_map)

        # Random knight spawn
        #knight = random_knight_spawn(cells, visited)

        # For simplistic
        knight = cells[0][1]
        knight.knight_come()
        visited[knight.pos[1]][knight.pos[0]] = True

        # Move
        # pos (x, y)
        pos = (1, 1)
        knight, running = self.knight_move_animation(knight, pos, visited, cells)

        pos = (1, 2)
        knight, running = self.knight_move_animation(knight, pos, visited, cells)


        #pos = (2, 2)
        running = self.sword_shoot_animation(knight, pos, visited, cells)

        running = True
        while running:
            # Draw frame while game is running and update all to the screen
            self.draw_frame_game(visited, cells)
            pygame.display.update()


            # Event of user interact with the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                mouse_pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_backletsgo.isOver(mouse_pos):
                        running = False

                if event.type == pygame.MOUSEMOTION:
                    if self.button_backletsgo.isOver(mouse_pos):
                        self.button_backletsgo.outline_color = BUTTON_BORDER_COLOR_OVER
                        self.button_backletsgo.text_color = TEXT_COLOR_OVER
                        self.button_backletsgo.button_color = BUTTON_COLOR_OVER
                    else:
                        self.button_backletsgo.outline_color = BUTTON_BORDER_COLOR
                        self.button_backletsgo.text_color = TEXT_COLOR
                        self.button_backletsgo.button_color = BUTTON_COLOR

            # KNIGHT move, ...



    def scr_menu_draw(self):
        self.screen.blit(self.menu, [0, 0])
        self.button_letsgo.draw(True)
        self.button_choosemap.draw(True)
        self.button_tutorial.draw(True)
        self.button_exist.draw(True)


    def scr_menu(self):
        running = True

        while running:

            self.scr_menu_draw()
            pygame.display.update()

            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if self.button_letsgo.isOver(mouse_pos):
                        self.letsgo()


                    if self.button_choosemap.isOver(mouse_pos):
                        running = False

                    if self.button_tutorial.isOver(mouse_pos):
                        running = False

                    if self.button_exist.isOver(mouse_pos):
                        running = False


                if event.type == pygame.MOUSEMOTION:
                    if self.button_letsgo.isOver(mouse_pos):
                        self.button_letsgo.outline_color = BUTTON_MENU_BORDER_COLOR_OVER
                        self.button_letsgo.text_color = TEXT_MENU_COLOR_OVER
                        self.button_letsgo.button_color = BUTTON_MENU_COLOR_OVER
                    else:
                        self.button_letsgo.outline_color = BUTTON_MENU_BORDER_COLOR
                        self.button_letsgo.text_color = TEXT_MENU_COLOR
                        self.button_letsgo.button_color = BUTTON_MENU_COLOR

                    if self.button_choosemap.isOver(mouse_pos):
                        self.button_choosemap.outline_color = BUTTON_MENU_BORDER_COLOR_OVER
                        self.button_choosemap.text_color = TEXT_MENU_COLOR_OVER
                        self.button_choosemap.button_color = BUTTON_MENU_COLOR_OVER
                    else:
                        self.button_choosemap.outline_color = BUTTON_MENU_BORDER_COLOR
                        self.button_choosemap.text_color = TEXT_MENU_COLOR
                        self.button_choosemap.button_color = BUTTON_MENU_COLOR

                    if self.button_tutorial.isOver(mouse_pos):
                        self.button_tutorial.outline_color = BUTTON_MENU_BORDER_COLOR_OVER
                        self.button_tutorial.text_color = TEXT_MENU_COLOR_OVER
                        self.button_tutorial.button_color = BUTTON_MENU_COLOR_OVER
                    else:
                        self.button_tutorial.outline_color = BUTTON_MENU_BORDER_COLOR
                        self.button_tutorial.text_color = TEXT_MENU_COLOR
                        self.button_tutorial.button_color = BUTTON_MENU_COLOR

                    if self.button_exist.isOver(mouse_pos):
                        self.button_exist.outline_color = BUTTON_MENU_BORDER_COLOR_OVER
                        self.button_exist.text_color = TEXT_MENU_COLOR_OVER
                        self.button_exist.button_color = BUTTON_MENU_COLOR_OVER
                    else:
                        self.button_exist.outline_color = BUTTON_MENU_BORDER_COLOR
                        self.button_exist.text_color = TEXT_MENU_COLOR
                        self.button_exist.button_color = BUTTON_MENU_COLOR


    def run(self):
        self.scr_menu()


