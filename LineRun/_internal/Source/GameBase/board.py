from Source.GameBase.boardmap import BoardMap
from Source.GUI.position import Position
from Source.GameBase.tile import Tile
from Source.GUI.color import Color

import pygame

from Source.GameBase.relation import Relation

class Board(BoardMap):
    def __init__(self, level):
        super().__init__(level)
        self.main_rect = pygame.Rect([Position.relx(60), Position.rely(280), Position.relw(480), Position.relh(480)])
        self.tile_size = [Position.relw(480/self.size[0]), Position.rely(480/self.size[0])]
        self.tiles = []
        index = 0
        y = self.main_rect.y
        for i in range(0, self.size[0]):
            x = self.main_rect.x
            for j in range(0, self.size[1]):
                tile = Tile(x, y, self.tile_size[0], self.tile_size[1], self.map[index])
                self.tiles.append(tile)
                x += self.tile_size[0]
                index += 1
            y += self.tile_size[1]
        self.player_sequence = []
        self.player_tile_sequence = []
        self.sequence_counter = 0
    
    def update(self, surface, click_event):
        for tile in self.tiles:
            pygame.draw.rect(surface, Color.white, [tile.x - 5, tile.y - 5, tile.w + 10, tile.h + 10])
            tile.update(surface, click_event)
            if tile.clicked:
                if tile.value != " " and tile.value in self.player_sequence:
                    pass
                else:
                    self.player_sequence.append(tile.value)
                    self.player_tile_sequence.append(tile)
                    self.sequence_counter += 1
                    if len(self.player_sequence) == len(self.sequence):
                        return 2
                    elif self.sequence[0:self.sequence_counter] != self.player_sequence[0:self.sequence_counter]:
                        if self.player_sequence[-1] == " ":
                            return -1
                        return -1
        index = 0
        for tile in self.player_tile_sequence:
            if len(self.player_tile_sequence) > index + 1:
                next_tile = self.player_tile_sequence[index + 1]
                pygame.draw.line(surface, Color.middle_purple, [tile.rect.centerx, tile.rect.centery], [next_tile.rect.centerx, next_tile.rect.centery], Relation.line_width_relation[self.size[0]])
            index += 1
        return 1
                
        


