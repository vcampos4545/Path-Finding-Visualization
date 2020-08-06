import pygame
pygame.font.init()
from constants import *

class Button:
    def __init__(self, rect, text):
        self.rect = rect
        self.x = rect[0]
        self.y = rect[1]
        self.w = rect[2]
        self.h = rect[3]
        self.text = text
        self.selected = False

    def draw(self, WIN):
        if self.selected:
            pygame.draw.rect(WIN, GREY, self.rect)

        else:
            pygame.draw.rect(WIN, BLUE, self.rect, 1)
        font = pygame.font.Font('freesansbold.ttf',10)
        display = font.render(self.text,True,BLACK)
        textRect = display.get_rect()
        textRect.topleft = (self.x+5,self.y+5)
        WIN.blit(display,textRect)

    def contains(self, pos):
        if pos[0] >= self.x and pos[0] <= self.x + self.w:
            if pos[1] >= self.y and pos[1] <= self.y + self.h:
                return True

        return False
