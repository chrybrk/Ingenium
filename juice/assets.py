from juice.core import *

class Assets:
    def __init__(self):
        self.assets = {}
    
    def load_image(self, name, image_path, color_key = nil):
        im = pygame.image.load(image_path).convert()
        if color_key: im.set_colorkey(color_key)
        self.assets[name] = im

    def load_images(self, name, image_path, color_key = nil):
        images = []
        for img in sorted(os.listdir(image_path)):
            if img[-3] in ['png', 'jpg', 'bmp']:
                im = pygame.image.load(image_path + '/' + img).convert()
                if color_key: im.set_colorkey(color_key)
                images.append(im)
        self.assets[name] = images

    def load_tile(self, name, tilesheet, tile_size):
        image = Image.open(tilesheet).convert("RGBA")
        self.assets[name] = []
        for i in range(image.size[1] // tile_size[1]):
            for j in range(image.size[0] // tile_size[0]):
                cprd = image.crop((tile_size[1] * j, tile_size[0] * i, tile_size[1] * (j + 1), tile_size[0] * (i + 1)))
                tile = pygame.image.fromstring(cprd.tobytes(), cprd.size, cprd.mode)
                self.assets[name].append(tile)

    def return_load_images(self, image_path, color_key = nil):
        images = []
        for img in sorted(os.listdir(image_path)):
            if img[-3] in ['png', 'jpg', 'bmp']:
                im = pygame.image.load(image_path + '/' + img).convert()
                if color_key: im.set_colorkey(color_key)
                images.append(im)
        
        return images

    def create_animation(self, name, path, image_duration = 5, loop = true, color_key = nil):
        self.assets[name] = Animation(self.return_load_images(path, color_key), image_duration, loop)

    def get(self, name): return self.assets[name]

class Animation:
    def __init__(self, images, image_duration, loop=true):
        self.images = images
        self.image_duration = image_duration
        self.loop = loop
        self.done = false
        self.frame = 0

    def copy(self): return Animation(self.images, self.image_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.image_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.image_duration * len(self.images) - 1)
            if self.frame >= self.image_duration * len(self.images) - 1:
                self.done = true

    def image(self):
        return self.images[int(self.frame / self.image_duration)]
