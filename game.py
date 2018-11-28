import pygame
import random
from enum import Enum
from utility import Colors, Fonts, Actions


class States(Enum):
    EMPTY = 0
    FILLED = 1
    MOVING = 2

class Cell: 
    def __init__(self, color, state):
        self.color = color
        self.state = state  

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Tetromino:
    def __init__(self, coordinates, pivot, color):
        self.coordinates = coordinates
        self.pivot = pivot
        self.color = color


class GameModel:

    TETROMINOS = [
        # L
        Tetromino([
            Coordinate(-1, 0), 
            Coordinate( 0, 0), 
            Coordinate( 1, 0), 
            Coordinate( 1, 1)
        ], 
        Coordinate(0, 0),
        Colors.YELLOW),

        # J
        Tetromino([
            Coordinate(-1, 1),
            Coordinate(-1, 0),
            Coordinate( 0, 0),
            Coordinate( 1, 0)
        ],
        Coordinate(0, 0),
        Colors.PINK),

        # S
        Tetromino([
            Coordinate(-1, 0),
            Coordinate( 0, 0),
            Coordinate( 0, 1),
            Coordinate( 1, 1)
        ],
        Coordinate(0, 0),
        Colors.RED),

        # Z
        Tetromino([
            Coordinate(-1, 1),
            Coordinate( 0, 1),
            Coordinate( 0, 0),
            Coordinate( 1, 0)
        ],
        Coordinate(0, 0),
        Colors.ORANGE),

        # T
        Tetromino([
            Coordinate(-1, 0),
            Coordinate( 0, 0), 
            Coordinate( 0, 1), 
            Coordinate( 1, 0)
        ],
        Coordinate(0, 0),
        Colors.PURPLE),

        # I
        Tetromino([
            Coordinate(-2, 0),
            Coordinate(-1, 0), 
            Coordinate( 0, 0), 
            Coordinate( 1, 0)
        ],
        Coordinate(0, 0),
        Colors.GREEN),

        # O
        Tetromino([
            Coordinate(-1, 0), 
            Coordinate(-1, 1), 
            Coordinate( 0, 0),
            Coordinate( 0, 1) 
        ],
        Coordinate(-0.5, 0.5),
        Colors.BLUE),
    ]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [[Cell(Colors.BLACK, States.EMPTY) for x in range(width)] for y in range(height)]
        self.score = 0
        self.lost = False
        self.pivot = None 
        self.next = random.choice(GameModel.TETROMINOS)
        self.insert()

    def next_tetromino(self):
        current = self.next
        self.next = random.choice(GameModel.TETROMINOS)
        return current

    def insert(self):
        next = self.next_tetromino()
        self.pivot = Coordinate(self.width // 2 + next.pivot.x, 2 - next.pivot.y)
        for i in next.coordinates: # = 4-szer, mert 4 cellából áll egy tetromino
            self.matrix[2 - i.y][self.width // 2 + i.x] = Cell(next.color, States.MOVING)

    def tick(self):
        fall = True
        # mehet-e lejjebb
        for y in range(self.height):
            for x in range(self.width):
                if (self.matrix[y][x].state == (States.MOVING or States.PIVOT) and 
                (y + 1 > self.height - 1 or self.matrix[y + 1][x].state == States.FILLED)):
                    fall = False
        # ha mehet lejjebb: alulról haladva cella kitörli magát majd maga alatt kitölt egyet   
        if fall: 
            self.pivot.y += 1
            for y in range(self.height - 1, 0 - 1, -1):
                for x in range(self.width):
                    if self.matrix[y][x].state == States.MOVING:
                        self.matrix[y+1][x].color = self.matrix[y][x].color
                        self.matrix[y+1][x].state = States.MOVING
                        self.matrix[y][x].color = Colors.BLACK
                        self.matrix[y][x].state = States.EMPTY
        # ha nem mehet lejjebb: nem mozgóvá teszi
        else:
            for y in range(self.height):
                    for x in range(self.width):
                        if self.matrix[y][x].state == States.MOVING:
                            self.matrix[y][x].state = States.FILLED
            self.line_clear()
            if not self.check_end_condition():
                self.insert()    
            else:
                self.lost = True      

    def move_left(self):
        """ballra mozgatja a tetrominót"""
        move = True
        for y in range(self.height):
            for x in range(self.width):
                if self.matrix[y][x].state == States.MOVING and (x - 1 < 0 or self.matrix[y][x-1].state == States.FILLED):
                    move = False
        if move:
            self.pivot.x -= 1
            for y in range(self.height):
                for x in range(self.width):
                    if self.matrix[y][x].state == States.MOVING:
                        self.matrix[y][x-1].state = States.MOVING
                        self.matrix[y][x-1].color = self.matrix[y][x].color
                        self.matrix[y][x].state = States.EMPTY
                        self.matrix[y][x].color = Colors.BLACK

    def move_right(self):
        """jobbra mozgatja a tetrominót"""
        move = True
        for y in range(self.height):
            for x in range(self.width):
                if self.matrix[y][x].state == States.MOVING and (x + 1 > self.width - 1 or self.matrix[y][x+1].state == States.FILLED):
                    move = False
        if move:
            self.pivot.x += 1
            stop = False
            for y in range(self.height):
                for x in range(self.width - 1, 0 - 1, -1):
                    if self.matrix[y][x].state == States.MOVING:
                        self.matrix[y][x+1].state = States.MOVING
                        self.matrix[y][x+1].color = self.matrix[y][x].color
                        self.matrix[y][x].state = States.EMPTY
                        self.matrix[y][x].color = Colors.BLACK

    def rotate(self):
        # létrehozunk egy üres mátrixot
        next_matrix = [[Cell(Colors.BLACK, States.EMPTY) for x in range(self.width)] for y in range(self.height)]
        # először a teli cellákat másoljuk bele az alapmátrixból
        for y in range(self.height):
            for x in range(self.width):
                if self.matrix[y][x].state == States.FILLED:
                    next_matrix[y][x] = self.matrix[y][x]
        # majd a mozgó cellákat másoljuk bele
        for y in range(self.height):
            for x in range(self.width):
                if self.matrix[y][x].state == States.MOVING:
                    # kiszámoljuk egy cella új, forgatott koordinátáít
                    # cella koordinátáiból kivonjuk a tengely koordinátáit -> "tengely origójú" relatív koordinátarendszerbe kerülünk, forgathatunk körülötte
                    dx = x - self.pivot.x
                    dy = y - self.pivot.y
                    # forgatás 90 fokkal óramutatóval ellentétesen (-> abszolút koordinátarendszerben majd így lesz óramutatóval megegyező)
                    dx, dy = -dy, dx
                    # visszaadjuk hozzá a tengely koordinátáit -> visszakerülünk az abszolút koordinátarendszerbe
                    dx += self.pivot.x
                    dy += self.pivot.y
                    # ha nem lógna ki az adott cella forgatás után a mátrixból, akkor átmásoljuk az új mátrixba
                    if dx >= 0 and dx < self.width and dy >= 0 and dy < self.height and self.matrix[int(dy)][int(dx)].state != States.FILLED:
                        next_matrix[int(dy)][int(dx)] = self.matrix[y][x] # int(), ha törtté (float, pl 5.0, bár egész) alakulna mert a pivot is tört
                    # ha kilógna a mátrixból/teli cellába ütközne akár egy cella is, visszatérünk a függvényből, nincs forgatás
                    else:
                        return
        # régi mátrix helyére az új mátrix
        self.matrix = next_matrix
    
    def line_clear(self):
        for y in range(self.height - 1, 0 - 1, -1):
            full = True
            while full:
                for x in range(self.width):
                    if self.matrix[y][x].state != States.FILLED:
                        full = False
                if full:
                    self.score += 100
                    for dy in range(y - 1, 0 - 1, -1):
                        for dx in range(self.width):
                            self.matrix[dy+1][dx].state = self.matrix[dy][dx].state
                            self.matrix[dy+1][dx].color = self.matrix[dy][dx].color

    def check_end_condition(self):
        for y in range(3): # felső 3 sor check
            for x in range(self.width):
                if self.matrix[y][x].state != States.EMPTY:
                    return True
        return False

class GameScreen:

    UNIT = 25 # cellaszélesség
    PREVIEW_WIDTH = 6
    PREVIEW_HEIGHT = 4

    def __init__(self, model):
        self.model = model
        self.paused = False

    def draw(self, surface):
        self.draw_field(surface, GameScreen.UNIT, GameScreen.UNIT)
        self.draw_preview(surface, (self.model.width + 2) * GameScreen.UNIT, GameScreen.UNIT)
        self.draw_scoreboard(surface, (self.model.width + 2) * GameScreen.UNIT, (GameScreen.PREVIEW_HEIGHT + 2)* GameScreen.UNIT)

    def draw_field(self, surface, cx, cy): # pálya megjelenítése, felső 2 sort nem rajzoljuk ki   
        for y in range(2, self.model.height):
            for x in range(self.model.width):
                pygame.draw.rect(surface, self.model.matrix[y][x].color.value, (x * GameScreen.UNIT + cx, (y-2) * GameScreen.UNIT + cy, GameScreen.UNIT, GameScreen.UNIT))

    def draw_preview(self, surface, cx, cy): 
        pygame.draw.rect(surface, Colors.BLACK.value, (cx, cy, GameScreen.PREVIEW_WIDTH * GameScreen.UNIT, GameScreen.PREVIEW_HEIGHT * GameScreen.UNIT))
        for i in self.model.next.coordinates:
            pygame.draw.rect(surface, self.model.next.color.value, (cx + (GameScreen.PREVIEW_WIDTH // 2 + i.x) * GameScreen.UNIT, cy + (GameScreen.PREVIEW_HEIGHT - 2 - i.y) * GameScreen.UNIT, GameScreen.UNIT, GameScreen.UNIT))

    def draw_scoreboard(self, surface, cx, cy):
        score_text = Fonts.SMALL.value.render("SCORE:", False, Colors.BLACK.value)
        surface.blit(score_text, (cx, cy))

        score_number = Fonts.SMALL.value.render("{:>10}".format(self.model.score), False, Colors.YELLOW.value, Colors.BLACK.value)
        surface.blit(score_number, (cx, cy + score_text.get_height() * 2))

    def show(self):
        # ablak méretei, létrehozása
        size = ((1 + self.model.width + 1 + GameScreen.PREVIEW_WIDTH + 1) * GameScreen.UNIT,
                (1 + (self.model.height - 2) + 1) * GameScreen.UNIT) # 2 sort nem rajzolunk ki
        window = pygame.display.set_mode(size)

        # órajel, ciklusidő megadásához
        clock = pygame.time.Clock()

        # timer event
        pygame.time.set_timer(pygame.USEREVENT, 1000) # eseményazonosító->felhasználó által létrehozott, legkisebb használható konstans; 1000 millisecods = 1 second

        # main loop, = 1db képernyőfrissítés
        while True:
            # event loop
            for event in pygame.event.get(): 
                # kilépés
                if event.type == pygame.QUIT:
                    return Actions.QUIT
                # lefele mozgás
                elif event.type == pygame.USEREVENT: 
                    self.model.tick()
                # gomblenyomás
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            pygame.time.set_timer(pygame.USEREVENT, 0) # feltakarítás, 0 -> letiltja
                            return Actions.CANCEL                      
                    elif event.key == pygame.K_SPACE:
                        if self.model.lost:
                            pygame.time.set_timer(pygame.USEREVENT, 0) 
                            return Actions.OK
                        elif self.paused:
                            pygame.time.set_timer(pygame.USEREVENT, 1000) # 1000 -> újra beállítja
                            self.model.tick()
                            self.paused = False
                        else:
                            pygame.time.set_timer(pygame.USEREVENT, 0)
                            self.paused = True
                    elif not self.paused:
                        if event.key == pygame.K_LEFT:
                            self.model.move_left()
                        elif event.key == pygame.K_RIGHT:
                            self.model.move_right()   
                        elif event.key == pygame.K_DOWN:
                            pygame.time.set_timer(pygame.USEREVENT, 0)
                            self.model.tick()
                        elif event.key == pygame.K_UP:
                            self.model.rotate() 
                # gombfelengedés
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN and not self.paused:
                        pygame.time.set_timer(pygame.USEREVENT, 1000)

            # kitölti az ablakot egy színnel
            window.fill(Colors.WHITE.value)

            # játéktér megrajzolása
            self.draw(window)

            # GAME OVER felirat
            if self.model.lost:
                pygame.draw.rect(window, Colors.WHITE.value, (0, window.get_height() // 2 - 50, window.get_width(), 100))

                text1 = Fonts.BIG.value.render("GAME OVER", False, Colors.BLACK.value)
                window.blit(text1, (window.get_width() // 2 - text1.get_width() // 2, window.get_height() // 2 - text1.get_height() // 2))
        
                text2 = Fonts.SMALL.value.render("press space to continue", False, Colors.BLACK.value)
                window.blit(text2, (window.get_width() // 2 - text2.get_width() // 2, window.get_height() // 2 + text1.get_height() // 2))

            # PAUSED felirat
            if self.paused:
                pygame.draw.rect(window, Colors.WHITE.value, (0, window.get_height() // 2 - 50, window.get_width(), 100))

                text1 = Fonts.BIG.value.render("PAUSED", False, Colors.BLACK.value)
                window.blit(text1, (window.get_width() // 2 - text1.get_width() // 2, window.get_height() // 2 - text1.get_height() // 2))

                text2 = Fonts.SMALL.value.render("press space to continue", False, Colors.BLACK.value)
                window.blit(text2, (window.get_width() // 2 - text2.get_width() // 2, window.get_height() // 2 + text1.get_height() // 2))


            # végén kirajzolja a képet
            pygame.display.update()

            # 1 ciklus hossza
            clock.tick(60) # 60fps


class SettingsScreen:
    def __init__(self):
        self.width = 10
        self.height = 20

    def show(self):
        window = pygame.display.set_mode((400, 600))

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return Actions.QUIT
                elif event.type == pygame.KEYDOWN: # width: 5-15, height: 10-20
                    if event.key == pygame.K_RIGHT and self.width < 15:
                        self.width += 1
                    elif event.key == pygame.K_LEFT and self.width > 5:
                        self.width -=1
                    elif event.key == pygame.K_UP and self.height < 20:
                        self.height += 1
                    elif event.key == pygame.K_DOWN and self.height > 10:
                        self.height -= 1
                    elif event.key == pygame.K_RETURN:
                        return Actions.OK
                    elif event.key == pygame.K_ESCAPE:
                        return Actions.CANCEL

            window.fill(Colors.WHITE.value)

            # title
            title = Fonts.SMALLTITLE.value.render("DIMENSIONS?", False, Colors.BLUE.value)
            window.blit(title, (window.get_width() // 2 - title.get_width() // 2, window.get_height() // 5 - title.get_height() // 2))
            
            # width
            width_text = Fonts.SMALL.value.render("width", False, Colors.PINK.value)
            window.blit(width_text, (window.get_width() // 4 - width_text.get_width() // 2, window.get_height() // 2.75 - width_text.get_height() // 2))

            width_number = Fonts.SMALL.value.render("{}".format(self.width), False, Colors.BLACK.value)
            window.blit(width_number, (window.get_width() // 4 - width_number.get_width() // 2, window.get_height() // 2 - width_number.get_height() // 2))

            width_arrows = Fonts.SMALL.value.render("<    >", False, Colors.PURPLE.value)
            window.blit(width_arrows, (window.get_width() // 4 - width_arrows.get_width() // 2, window.get_height() // 2 - width_arrows.get_height() // 2))

            # height
            height_text = Fonts.SMALL.value.render("height", False, Colors.PINK.value)
            window.blit(height_text, (window.get_width() // 4 * 3 - height_text.get_width() // 2, window.get_height() // 2.75 - height_text.get_height() // 2))

            height_number = Fonts.SMALL.value.render("{}".format(self.height), False, Colors.BLACK.value)
            window.blit(height_number, (window.get_width() // 4 * 3 - height_number.get_width() // 2, window.get_height() // 2 - height_number.get_height() // 2))

            height_arrows = pygame.transform.rotate(Fonts.SMALL.value.render("<    >", False, Colors.PURPLE.value), 90)
            window.blit(height_arrows, (window.get_width() // 4 * 3 - height_arrows.get_width() // 2, window.get_height() // 2 - height_arrows.get_height() // 2))

            # esc, enter
            esc = Fonts.SMALL.value.render("< ESC", False, Colors.BLACK.value)
            window.blit(esc, (10, window.get_height() - esc.get_height() - 10))

            enter = Fonts.SMALL.value.render("ENTER >", False, Colors.BLACK.value)
            window.blit(enter, (window.get_width() - enter.get_width() - 10, window.get_height() - esc.get_height() - 10))

            pygame.display.update()

            clock.tick(60)
