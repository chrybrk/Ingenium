from juice.core import *

class Layer:
    def __init__(self, position, image, speed, depth):
        self.position = list(position)
        self.image = image
        self.speed = speed
        self.depth = depth

    def update(self):
        self.position[0] += self.speed
        self.position[1] += self.speed

    def render(self, surface, offset=(0, 0)):
        render_position = (self.position[0] - offset[0] * self.depth, self.position[1] - offset[1] * self.depth)
        surface.blit(self.image, (render_position[0] % (surface.get_width() + self.image.get_width()) - self.image.get_width(), render_position[1] % (surface.get_height() + self.image.get_height()) - self.image.get_height()))

class Layers:
    def __init__(self, layer_images, count = 16):
        self.layers = []

        for i in range(count):
            self.layers.append(Layer((random.random() * 99999, random.random() * 99999), random.choice(layer_images), random.random() * 0.05 + 0.05, random.random() * 0.6 + 0.2))

        self.layers.sort(key=lambda x: x.depth)

    def update(self):
        for layer in self.layers: layer.update()

    def render(self, surface, offset=(0, 0)):
        for layer in self.layers: layer.render(surface, offset)
