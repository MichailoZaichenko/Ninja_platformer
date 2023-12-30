import sys
import pygame
# import files
from scriptis.entities import PhysicsEntity
from scriptis. tilemap import TIlemap, TILE_SIZE
from scriptis.utils import load_image, load_images

class Game:
    def __init__(self):
        pygame.init()
        # Name of window
        pygame.display.set_caption("NINJA")

        # Some constands
        SCREEN_WIDTH = 1280//2
        SCREEN_HIGHT = 960//2
        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT)) 
        self.FPS = 60
        self.CLOCK = pygame.time.Clock()

        self.display = pygame.Surface((SCREEN_WIDTH//2, SCREEN_HIGHT//2))

        self.img = pygame.image.load('data/images/clouds/cloud_1.png')
        self.img.set_colorkey((0,0,0))

        self.img_pos = [160, 260]
        self.movement = [False, False]

        self.assets = { 
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),\
            'spawners' : load_images('tiles/spawners'),
            'stone' : load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
        }

        self.collision_area = pygame.Rect(50, 50, 300, 50)
        # useage on class PhysicsEntity 
        self.player = PhysicsEntity(self, 'player', (100, 50), (8, 15)) 

        self.tilemap = TIlemap(self, TILE_SIZE)
    def run(self):
        # Main loop
        while True:
            self.display.fill((14, 143, 134))

            self.tilemap.render(self.display)
            
            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.movement[1] = False

            self.SCREEN.blit(pygame.transform.scale(self.display, self.SCREEN.get_size()), (0,0))
            pygame.display.update()
            self.CLOCK.tick(self.FPS)

Game().run()


