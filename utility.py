import pygame
from enum import Enum

pygame.font.init()

class Colors(Enum):
    BLACK  = (  0,   0,   0)
    WHITE  = (255, 255, 255)
    RED    = (255, 204, 204)
    GREEN  = (229, 255, 204)
    BLUE   = (204, 229, 255)
    PINK   = (255, 204, 229)
    YELLOW = (255, 255, 204)
    PURPLE = (229, 204, 255)
    ORANGE = (255, 229, 204)

class Fonts(Enum):
    BIGTITLE   = pygame.font.Font("fonts/Nightmare Codehack.otf", 170)
    SMALLTITLE = pygame.font.Font("fonts/Nightmare Codehack.otf", 85)
    SMALL      = pygame.font.Font("fonts/PressStart2P.ttf", 15)
    BIG        = pygame.font.Font("fonts/PressStart2P.ttf", 30)

class Actions(Enum):
    QUIT   = 0
    CANCEL = 1
    OK     = 2