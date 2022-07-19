import pygame
from Source.GUI.Font import Font

class Label:
    def __init__(self, text, color, pos, font_string=Font.font_string, font_size=Font.font_size):
        pygame.font.init()
        self.text = text
        self.color = color
        self.pos = pos
        self.font = pygame.font.SysFont(font_string, int(font_size))
        self.obj = self.font.render(self.text, 1, self.color)
        self.rect = self.obj.get_rect()
        self.rect.topleft = self.pos
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

    def centerX(self, x):
        self.centerx = x
    
    def centerY(self, y):
        self.centery = y

    def update(self, surface):
        self.obj = self.font.render(self.text, 1, self.color)
        self.rect = self.obj.get_rect()
        if self.centerx != self.rect.centerx or self.centery != self.rect.centery:
            self.rect.centerx = self.centerx
            self.rect.centery = self.centery
        else:
            self.rect.topleft = self.pos
        surface.blit(self.obj, self.rect)
