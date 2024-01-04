import sys
import math
import pygame
import random
# import files
from scriptis.entities import PhysicsEntity, Player
from scriptis. tilemap import TIlemap, TILE_SIZE
from scriptis.utils import load_image, load_images, Animation
from scriptis.clouds import Clouds, COUNT_OF_CLOUDS
from scriptis.particle import Particle

class Game:
    def __init__(self):
        pygame.init()

        # Name of window
        pygame.display.set_caption("NINJA")

        # Some constands
        SCREEN_WIDTH = 1280//2
        SCREEN_HIGHT = 960//2
        PLAYER_BOX_WIDTH = 8
        PLAYER_BOX_HIGHT = 15
        PLAYER_SPAWN_POSITION = (100, 50)
        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
        self.display = pygame.Surface((SCREEN_WIDTH//2, SCREEN_HIGHT//2)) 
        self.FPS = 60
        self.CLOCK = pygame.time.Clock()
        # Draw on smaller surfas to extend it and get pixel efect
        self.movement = [False, False]

        self.assets = { 
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'spawners' : load_images('tiles/spawners'),
            'stone' : load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background' : load_image('background.png'),
            'clouds' : load_images('clouds'),
            'player/idle' : Animation(load_images('entities/player/idle'), img_duration = 6),
            'player/run' : Animation(load_images('entities/player/run')),
            'player/jump' : Animation(load_images('entities/player/jump')),
            'player/slide' : Animation(load_images('entities/player/slide')),
            'player/wall_slide' : Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_duration=20, loop=False),
        }
        
        # Useage on class clouds
        self.clouds = Clouds(self.assets['clouds'], count = COUNT_OF_CLOUDS)
        # Useage on class PhysicsEntity 
        self.player = Player(self, PLAYER_SPAWN_POSITION, (PLAYER_BOX_WIDTH, PLAYER_BOX_HIGHT)) 
        # Useage on class Tilemap
        self.tilemap = TIlemap(self, TILE_SIZE)
        self.tilemap.load('map.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep = True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['position'][0],  4 + tree['position'][1], 23, 13))

        self.particles = []

        #Camera scrolling
        self.scroll = [0, 0]
    
    def run(self):
        # Main loop
        while True:
            self.display.blit(self.assets['background'], (0, 0))
            # Finding where cam is on X
            self.scroll[0] += ( self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            # Finding where cam is on Y
            self.scroll[1] += ( self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            # Executing the float in scroll
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            # spawning leafs
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    position = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', position, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            # Render clouds
            self.clouds.update()
            self.clouds.render(self.display, offset = render_scroll)

            # Update and render part
            self.tilemap.render(self.display, offset = render_scroll)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset = render_scroll)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset = render_scroll)
                if particle.type == 'leaf':
                    particle.position[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.movement[1] = True
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.player.velocity[1] = -3
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.velocity[1] = 3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.movement[1] = False
            # Resize the display
            self.SCREEN.blit(pygame.transform.scale(self.display, self.SCREEN.get_size()), (0, 0))
            pygame.display.update()
            # Setting the FPS limits
            self.CLOCK.tick(self.FPS)

Game().run()


