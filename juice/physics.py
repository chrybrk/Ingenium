from juice.core import *

class Vector(object):
    def __init__(self, x: int = 0, y: int = 0, z: int = 0) -> nil:
        self.x: int = x
        self.y: int = y
        self.z: int = z

    def __add__(self, vec2: object) -> object:  return Vector(self.x + vec2.x, self.y + vec2.y, self.z + vec2.z)

    def __sub__(self, vec2: object) -> object:  return Vector(self.x - vec2.x, self.y - vec2.y, self.z - vec2.z)

    def __mul__(self, vec2: object) -> object:  return Vector(self.x * vec2.x, self.y * vec2.y, self.z * vec2.z)

    def dot(self, vec2: object) -> object:      return Vector(self.x * vec2.x, self.y * vec2.y, self.z * vec2.z)

    def cross(self, vec2: object) -> object:    return Vector((self.y * vec2.z + vec2.y * self.z), (self.x * vec2.z + vec2.x * self.z), (self.x * vec2.y + vec2.x * self.y))

    def scalar(self, value: int) -> object:     return Vector(self.x * value, self.y * value)

    @property
    def value3(self): return (self.x, self.y, self.z)

    @property
    def value2(self): return (self.x, self.y)

    def lerp(a, b, t) -> object:                return a.scalar(t) + b.scalar((1.0 - t))

    def magnitude(self) -> int:                 return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self) -> object:
        m = self.magnitude()
        return Vector(self.x / m, self.y / m, self.z / m)

    def rotation(self, value):
        theta = (value / 180) * math.pi
        new_x = self.x * math.cos(theta) - self.y * math.sin(theta)
        new_y = self.x * math.sin(theta) + self.y * math.cos(theta)

        return Vector(new_x, new_y)

    def length(self, vec2):
        return math.sqrt((self.x - vec2.x) ** 2 + (self.y - vec2.y) ** 2)

    def __repr__(self) -> str: return f"Vector({self.x}, {self.y}, {self.z})"

class Arm:
    def __init__(self, x, y, length, angle):
        self.x = x
        self.y = y
        self.length = length
        self.angle = angle
        self.parent = nil

    @property
    def get_ex(self):
        angle = self.angle
        parent = self.parent
        while (parent):
            angle += parent.angle
            parent = parent.parent

        return self.x + math.cos(self.angle) * self.length

    @property
    def get_ey(self):
        angle = self.angle
        parent = self.parent
        while (parent):
            angle += parent.angle
            parent = parent.parent

        return self.y + math.sin(self.angle) * self.length

    def render(self, surface, offset = (0, 0)):
        pygame.draw.line(surface, (255, 255, 255), (self.x, self.y), (self.get_ex, self.get_ey), 3)

class FKsystemArm(Arm):
    def __init__(self, length, center_angle, rotation_range = math.pi / 4, phase_offset = 0):
        super().__init__(0, 0, length, 0)
        self.center_angle = center_angle
        self.rotation_range = rotation_range
        self.phase_offset = phase_offset

    def set_phase(self, phase):
        self.angle = self.center_angle + math.sin(phase + self.phase_offset) * self.rotation_range

class IKsystemArm(Arm):
    def __init__(self, x, y, length, angle):
        super().__init__(x, y, length, angle)

    @property
    def get_ex(self):
        return self.x + math.cos(self.angle) * self.length

    @property
    def get_ey(self):
        return self.y + math.sin(self.angle) * self.length

    def point_at(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.angle = math.atan2(dy, dx)

    def drag(self, x, y):
        self.point_at(x, y)
        self.x = x - math.cos(self.angle) * self.length
        self.y = y - math.sin(self.angle) * self.length
        if self.parent:
            self.parent.drag(self.x, self.y)

class FKsystem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.phase = 0
        self.speed = 0.02
        self.arms = []
        self.lastArm = nil

    def add_arm(self, length, center_angle, rotation_range = math.pi / 4, phase_offset = 0):
        arm = FKsystemArm(length, center_angle, rotation_range, phase_offset)
        self.arms.append(arm)
        if self.lastArm: arm.parent = self.lastArm
        self.lastArm = arm

        self.update()

    def rotate_arm(self, index, angle):
        self.arms[index].angle = angle

    def update(self):
        for i in range(len(self.arms)):
            arm = self.arms[i]
            arm.set_phase(self.phase)
            if arm.parent:
                arm.x = arm.parent.get_ex
                arm.y = arm.parent.get_ey
            else:
                arm.x = self.x
                arm.y = self.y

        self.phase += self.speed

    def render(self, surface, offset = (0, 0)):
        for i in range(len(self.arms)):
            self.arms[i].render(surface)

class IKsystem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.arms = []
        self.lastArm = nil

    def add_arm(self, length):
        arm = IKsystemArm(0, 0, length, 0)
        if self.lastArm:
            arm.x = self.lastArm.get_ex
            arm.y = self.lastArm.get_ey
            arm.parent = self.lastArm
        else:
            arm.x = self.x
            arm.y = self.y

        self.arms.append(arm)
        self.lastArm = arm

    def update(self):
        for i in range(len(self.arms)):
            arm = self.arms[i]
            if arm.parent:
                arm.x = arm.parent.get_ex
                arm.y = arm.parent.get_ey
            else:
                arm.x = self.x
                arm.y = self.y

    def drag(self, x, y):
        self.lastArm.drag(x, y)

    def render(self, surface, offset = (0, 0)):
        for i in range(len(self.arms)):
            self.arms[i].render(surface)
