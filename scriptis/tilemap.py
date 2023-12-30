import pygame
TILE_SIZE = 16

class TIlemap:
    def __init__(self, game,  tile_size = TILE_SIZE ):
        self.game = game
        self.tile_size = tile_size
        # Phisics like objects with that you can interact
        self.tilemap = {}
        # Non-phiscs like decorations
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str(3+i) + ';10'] = {'type': 'grass', 'variant': 1, 'position': (3 + i, 10)}
            self.tilemap[';10' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'position': (10, 5 + i)}

    def render(self, surface):
        # Firstly decoration
        for tile in self. offgrid_tiles:
            surface.blit(self.game.assets[tile['tile']][tile['variant']], tile['position'])
        # Secondary physic objects
        for location in self.tilemap:
            tile = self.tilemap[location]
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['position'][0] * self.tile_size, tile['position'][1] * self.tile_size))
