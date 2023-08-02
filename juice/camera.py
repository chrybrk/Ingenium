from juice.core import *

"""
p 222 > 6
p 221 > 31 > 168
"""

class CameraType(Enum):
    target_centered = 0
    box_view = 1
    fixed_view = 2
    keyboard_control = 3
    fixed_position = 4

class Camera:
    def __init__(self, game, c_type, position = (0, 0), target = nil, box_size = nil, movement = nil, fixed_position = nil):
        self.game = game
        self.type = c_type
        self.position = list(position)
        self.target = target
        self.box_size = box_size
        self.movement = movement
        self.fixed_position = fixed_position

    def get_offset(self):
        match self.type.value:
            case 0:
                if not self.target:
                    print("target_centered `camera` expected `target`."); exit(0)
                else:
                    self.position[0] += (self.target.rect().centerx - self.game.surface.get_width() / 2 - self.position[0]) / 30
                    self.position[1] += (self.target.rect().centery - self.game.surface.get_height() / 2 - self.position[1]) / 30
                    return (int(self.position[0]), int(self.position[1]))

            case 1:
                if not self.box_size:
                    print("box_view `camera` expected `box_size`."); exit(0)

            case 3:
                if not self.movement:
                    print("keyboard_control `camera` expected `movement`."); exit(0)
                else:
                    if self.movement[0] > 0:
                        self.position[0] += 1
                    elif self.movement[0] < 0:
                        self.position[0] -= 1

                    if self.movement[1] > 0:
                        self.position[1] += 1
                    elif self.movement[1] < 0:
                        self.position[1] -= 1

                    return self.position

            case 4:
                if not self.fixed_position:
                    print("fixed_position `camera` expected `fixed_position`."); exit(0)
                else:
                    self.position[0] += self.fixed_position[0]
                    self.position[1] += self.fixed_position[1]
                    return (int(self.position[0]), int(self.position[1]))
