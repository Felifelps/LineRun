import pygame
from Source.GUI.Label import Label
from Source.GUI.color import Color
class Tile:
    def __init__(self, x, y, width, height, value):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.value = value
        self.rect = pygame.Rect([x, y, width, height])
        self.clicked = False
    
    def update(self, surface, click_event):
        font_color = Color.main_purple
        if click_event and self.rect.collidepoint(click_event.pos):
            self.clicked = True
        
        #Tile background color
        #when clicked
        if self.clicked:
            pygame.draw.rect(surface, Color.ligther_purple, self.rect)
        #when hovered
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, Color.main_purple, self.rect)
            font_color = Color.ligther_purple
        #anywhen
        else:
            pygame.draw.rect(surface, Color.black, self.rect)

        
        #Tile value
        value = Label(self.value, font_color, self.rect.topleft, "Impact", 180/(480/self.w))
        value.centerX(self.rect.centerx)
        value.centerY(self.rect.centery)
        value.update(surface)


        
