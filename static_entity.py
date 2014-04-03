import pygame


class StaticEntity:
    def __init__(self, pos, width, height):
        self.pos = pos
        self.w = width
        self.h = height
        self.rect = pygame.Rect(pos[0] - (width/2), pos[1] - (height/2), width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)