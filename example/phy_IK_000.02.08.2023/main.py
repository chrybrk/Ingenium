from juice.core import *
from juice.config import ConfigurationManager
from juice.assets import Assets, Animation
from juice.entities import Entity
from juice.font import Font
from juice.tilemap import Tilemap
from juice.camera import CameraType, Camera
from juice.physics import Vector, Arm, FKsystemArm, FKsystem, IKsystemArm, IKsystem

RENDER_SCALE = 1.8

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.configuration_manager = ConfigurationManager("./config")
        self.configuration_manager.load_config()

        self.width = self.configuration_manager.get_config("DISPLAY", "width", int)
        self.height = self.configuration_manager.get_config("DISPLAY", "height", int)
        self.title = self.configuration_manager.get_config("DISPLAY", "title", str)
        self.fps = self.configuration_manager.get_config("DISPLAY", "fps", int)
        self.scale = self.configuration_manager.get_config("DISPLAY", "scale", int)

        self.window = pygame.display.set_mode((self.width, self.height))
        self.surface = pygame.Surface((self.scale * self.window.get_size()[0] / 100, self.scale * self.window.get_size()[1] / 100))
        pygame.display.set_caption(self.title)

        self.alive = true

        self.dt = 0
        self.last_time = time.time()

        self.clear_color = (25, 25, 25)

        self.font = Font()
        self.font.set_font_renderer("./assets/font/dogica.ttf", 8, (255, 255, 255), 0)

        self.game_data()

    def game_data(self):
        self.movement = [0, 0]

        self.iks = IKsystem(self.surface.get_width() / 2, self.surface.get_height() / 2)
        for i in range(500):
            self.iks.add_arm(1)

        self.angle = 0

    def update(self, dt):
        self.font.draw(self.surface, (0, 0), f"FPS: { int(clock.get_fps()) }")

        self.mouse_position = pygame.mouse.get_pos()
        self.mouse_position = (self.mouse_position[0] / RENDER_SCALE, self.mouse_position[1] / RENDER_SCALE)
        self.iks.drag(*self.mouse_position)

        self.iks.render(self.surface)

        self.angle += 0.05

    def run(self):
        while self.alive:
            self.dt = time.time() - self.last_time
            self.dt *= self.fps
            self.last_time = time.time()

            self.surface.fill(self.clear_color)

            for event in pygame.event.get():
                # exit event
                if event.type == pygame.QUIT: self.alive = false
                
                # window resize event
                if event.type == 32779:
                    self.width = event.x
                    self.height = event.y

                if event.type == KEYDOWN:
                    if event.key == pygame.K_a: self.movement[0] =  1
                    if event.key == pygame.K_d: self.movement[0] = -1
                    if event.key == pygame.K_w: self.movement[1] =  1
                    if event.key == pygame.K_s: self.movement[1] = -1

                if event.type == KEYUP:
                    if event.key == pygame.K_a: self.movement[0] = 0
                    if event.key == pygame.K_d: self.movement[0] = 0
                    if event.key == pygame.K_w: self.movement[1] = 0
                    if event.key == pygame.K_s: self.movement[1] = 0

            self.update(self.dt)

            self.window.blit(pygame.transform.scale(self.surface, (self.width, self.height)), (0, 0))

            pygame.display.update()
            fpsLock(self.fps)

Game().run()
