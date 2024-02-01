import pygame
from .color import Color
from os.path import join

class Button:
    def __init__(self, surface, background_image_path, rect, command, **kwargs):
        pygame.font.init()

        self.settings = kwargs

        self.surface = surface
        if isinstance(rect, list):
            self.rect = pygame.Rect(rect)
        self.background_image = pygame.transform.scale(pygame.image.load(join(background_image_path)), (self.rect.w, self.rect.h))
        self.command = command

        self.settings["surface"] = self.surface
        self.settings["background_image"] = self.background_image
        self.settings["x"] = self.rect.x
        self.settings["y"] = self.rect.y
        self.settings["w"] = self.rect.w
        self.settings["h"] = self.rect.h
        self.settings["command"] = self.command
        self.hover = False
        self.text = False
        self.font_family = "Arial"
        self.font_size = 35
        self.font_color = Color.black
        self.font = pygame.font.SysFont(self.font_family, self.font_size)

        self._settings()
        
    def _settings(self):
        self.surface = self.settings["surface"]
        self.background_image = self.settings["background_image"]
        self.rect.x = self.settings["x"]  
        self.rect.y = self.settings["y"]  
        self.rect.w = self.settings["w"]  
        self.rect.h = self.settings["h"] 
        self.command = self.settings["command"]
        
        for setting in self.settings:
            if setting == "centerx":
                self.rect.centerx = self.settings["centerx"]
            elif setting == "centery":
                self.rect.centery = self.settings["centery"]
            elif setting == "hover_path":
                self.hover = pygame.image.load(self.settings[setting])
            elif setting == "text":
                self.text = self.settings[setting]
            elif setting == "font_family":
                self.font_family = self.settings[setting]
                self.font = pygame.font.SysFont(self.font_family, self.font_size)
            elif setting == "font_size":
                self.font_size = self.settings[setting]
                self.font = pygame.font.SysFont(self.font_family, self.font_size)
            elif setting == "font_color":
                self.font_color = self.settings[setting]

    def update(self, click_event):
        self._settings()
        if click_event != False and click_event.type == pygame.MOUSEBUTTONDOWN and click_event.button == 1 and self.rect.collidepoint(click_event.pos):
            return self.command()
 
        if self.hover != False and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surface.blit(self.hover, self.rect)
        else:
            self.surface.blit(self.background_image, self.rect)

        if self.text != False:
            self.textobj = self.font.render(self.text, 1, self.font_color) 
            self.surface.blit(self.textobj, [self.rect.centerx - self.textobj.get_rect().w/2, self.rect.centery - self.textobj.get_rect().h/2])

        
