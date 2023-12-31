import pygame
TILE_SIZE = 16
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}

class TIlemap:
    def __init__(self, game,  tile_size = TILE_SIZE ):
        self.game = game
        self.tile_size = tile_size
        # Phisics like objects with that you can interact
        self.tilemap = {}
        # Non-phiscs like decorations
        self.offgrid_tiles = []
        # where to draw
        for i in range(10):
                # Positon     X         Y
            self.tilemap[str(7 + i) + ';6'] = {'type': 'grass', 'variant': 1, 'position': (7 + i, 6)}
            self.tilemap[str(6 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'position': (6 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'position': (10, 5 + i)}

    def tiles_around(self, position):
        tiles = []
        tile_location = (int(position[0] // self.tile_size), int(position[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_location = str(tile_location[0] + offset[0]) + ';' + str(tile_location[1] + offset[1])
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])
        return tiles

    def physics_rects_around(self, position):
        rects = []
        for tile in self.tiles_around(position):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['position'][0] * self.tile_size, tile['position'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def render(self, surface, offset = (0, 0)):
    # Make rendering optimisations
        # Firstly decoration
        for tile in self. offgrid_tiles:
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['position'][0] - offset[0], tile['position'][1] - offset[1]))

        # Secondary decoration
        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                location = str(x) + ';' + str(y)
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['position'][0] * self.tile_size - offset[0], tile['position'][1] * self.tile_size - offset[1]))
