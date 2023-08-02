from juice.core import *

class Tilemap:
    def __init__(self, game, tile_size = 16):
        self.game = game
        self.tile_size = tile_size
        self.layers = {}
        self.PHYSICS_TILES = {}

    def load_tilemap(self, path):
        with open(path, "r") as f:
            data = csv.reader(f, delimiter = ',')
            tilemap = {}
            variants = []
            for row in data:
                variant = []
                for clm in row:
                    variant.append(clm)
                variants.append(variant)

            for j in range(len(variants)):
                for i in range(len(variants[j])):
                    if int(variants[j][i]) != -1:
                        tile_loc = str(i) + ';' + str(j)
                        tilemap[tile_loc] = { 'type': 'tilesheet', 'variant': int(variants[j][i]), 'position': (i, j) }

            return tilemap

    def add_layer(self, path):
        if list(self.layers.keys()) == []:
            self.layers[0] = self.load_tilemap(path)
        else:
            self.layers[list(a.keys())[-1] + 1] = self.load_tilemap(path)

    def get_layer(self, index):
        return self.layers[index]

    def append(self, index, tilemap):
        self.layers[index].update(tilemap)

    def tiles_around(self, index_set):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            for layer in self.layers:
                if check_loc in self.layers[layer]:
                    tiles.append(self.layer[layer][check_loc])

        return tiles

    def extract(self, index, id_pairs, keep = false):
        matches = []

        for layer in self.layers:
            for loc in self.layers[layer].copy():
                tile = self.layers[layer][loc]
                if (tile['type'], tile['variant']) in id_pairs:
                    matches.append(tile.copy())
                    matches[-1]['position'] = matches[-1]['position'].copy()
                    matches[-1]['position'][0] *= self.tile_size
                    matches[-1]['position'][1] *= self.tile_size
                    if not keep:
                        del self.layers[layer][loc]

        return matches

    def physics_rects_around(self, position):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in self.PHYSICS_TILES:
                rects.append(pygame.Rect(tile['position'][0] * self.tile_size, tile['position'][1] * self.tile_size, self.tile_size, self.tile_size))

        return rects

    def solid_check(self, position):
        tile_loc = str(int(position[0] // self.tile_size)) + ';' + str(int(position[1] // self.tile_size))
        for layer in self.layers:
            if tile_loc in self.layers[layer]:
                if self.layers[layer][tile_loc]['type'] in PHYSICS_TILES:
                    return self.layers[layer][tile_loc]

    def render(self, surface, offset = (0, 0)):
        for x in range(offset[0] // self.tile_size, (offset[0] + surface.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surface.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                for layer in self.layers:
                    if loc in self.layers[layer]:
                        tile = self.layers[layer][loc]
                        surface.blit(self.game.assets.get(tile['type'])[tile['variant']], (tile['position'][0] * self.tile_size - offset[0], tile['position'][1] * self.tile_size - offset[1]))
