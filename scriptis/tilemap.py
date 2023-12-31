import pygame
import json
TILE_SIZE = 16
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}
AUTOTILE_TYPES = {'grass', 'stone'}
X = 0
Y = 1

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2, 
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

class TIlemap:
    def __init__(self, game,  tile_size = TILE_SIZE ):
        self.game = game
        self.tile_size = tile_size
        # Phisics like objects with that you can interact
        self.tilemap = {}
        # Non-phiscs like decorations
        self.offgrid_tiles = []

    def extract(self, id_pairs, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
                    
        for location in self.tilemap:
            tile = self.tilemap[location]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()
                matches[-1]['pos'][X] *= self.tile_size
                matches[-1]['pos'][Y] *= self.tile_size
                if not keep:
                    del self.tilemap[location]
        
        return matches
    
    def tiles_around(self, pos):
        tiles = []
        tile_location = (int(pos[X] // self.tile_size), int(pos[Y] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_location = str(tile_location[X] + offset[X]) + ';' + str(tile_location[Y] + offset[Y])
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])
        return tiles

    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()
        
    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()
        
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
    
    def solid_check(self, pos):
        tile_location = str(int(pos[X] // self.tile_size)) + ';' + str(int(pos[Y] // self.tile_size))
        if tile_location in self.tilemap:
            if self.tilemap[tile_location]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_location]

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][X] * self.tile_size, tile['pos'][Y] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def autotile(self):
        for location in self.tilemap:
            tile = self.tilemap[location]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][X] + shift[X]) + ';' + str(tile['pos'][Y] + shift[Y])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]

    def render(self, surface, offset = (0, 0)):
    # Make rendering optimisations
        # Firstly decoration
        for tile in self. offgrid_tiles:
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][X] - offset[X], tile['pos'][Y] - offset[Y]))

        # Secondary decoration
        for x in range(offset[X] // self.tile_size, (offset[X] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[Y] // self.tile_size, (offset[Y] + surface.get_height()) // self.tile_size + 1):
                location = str(x) + ';' + str(y)
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][X] * self.tile_size - offset[X], tile['pos'][Y] * self.tile_size - offset[Y]))
