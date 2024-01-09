import sys
import os
import math
import pygame
import random
import time
# import files
from scriptis.entities import PhysicsEntity, Player, Enemy
from scriptis. tilemap import TIlemap, TILE_SIZE
from scriptis.utils import load_image, load_images, Animation
from scriptis.clouds import Clouds, COUNT_OF_CLOUDS
from scriptis.particle import Particlepos as Particle
from scriptis.spark import Spark

SCREEN_WIDTH = 1280//2
SCREEN_HIGHT = 960//2
PLAYER_BOX_WIDTH = 8
PLAYER_BOX_HIGHT = 15
BLACK = (255, 255, 255)
WHITE = (0,0,0)
PLAYER_SPAWN_POS = (100, 50)
X = 0
Y = 1
class Game:
    def __init__(self):
        pygame.init()

        # Name of window
        pygame.display.set_caption("NINJA")

        # Some constands
        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
        # Camera
        self.display = pygame.Surface((SCREEN_WIDTH//2, SCREEN_HIGHT//2), pygame.SRCALPHA) 
        # Surface
        self.display_2 = pygame.Surface((SCREEN_WIDTH//2, SCREEN_HIGHT//2))
        self.FPS = 60
        self.CLOCK = pygame.time.Clock()
        # Draw on smaller surfas to extend it and get pixel efect
        self.movement = [False, False]

        self.assets = { 
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle_kovriga'), img_duration=6),
            'enemy/run': Animation(load_images('entities/enemy/run_kovriga'), img_duration=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_duration=6),
            'player/run': Animation(load_images('entities/player/run'), img_duration=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_duration=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_duration=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }

        self.sfx = {
            'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
        }
        
        self.sfx['ambience'].set_volume(0.8)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.4)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.4)
        
        # Useage on class clouds
        self.clouds = Clouds(self.assets['clouds'], count = COUNT_OF_CLOUDS)
        # Useage on class PhysicsEntity 
        self.player = Player(self, PLAYER_SPAWN_POS, (PLAYER_BOX_WIDTH, PLAYER_BOX_HIGHT)) 
        # Useage on class Tilemap
        self.tilemap = TIlemap(self, TILE_SIZE)
        self.level = 0
        self.load_level(self.level)
        
        self.screenshake = 0
        
        

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')
        
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep = True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][X],  4 + tree['pos'][Y], 23, 13))

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (PLAYER_BOX_WIDTH, PLAYER_BOX_HIGHT)))

        self.projectiles = []
        self.particles = []
        self.sparks = []

        #Camera scrolling
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30
    
    def run(self):
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.sfx['ambience'].play(-1)
        # Main loop
        while True:
            self.display.fill((0, 0, 0, 0))
            # self.display_2.blit(pygame.transform.scale2x(self.assets['background']), (0, 0))
            # self.display_2.blit(load_image('intro/0.png'), (0, 0))
            # time.sleep(3)
            # self.display_2.blit(load_image('intro/1.png'), (0, 0))
            # time.sleep(3)
            self.display_2.blit(self.assets['background'], (0, 0))
            
            self.screenshake = max(0, self.screenshake - 1)
            
            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 1
            
            if self.dead:
                self.dead += 1
                if self.dead >= 10:
                    self.transition = min(30, self.transition + 1)
                if self.dead > 40:
                    self.load_level(self.level)

            # Finding where cam is on X
            self.scroll[X] += ( self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[X]) / 30
            # Finding where cam is on Y
            self.scroll[Y] += ( self.player.rect().centery - self.display.get_height() / 2 - self.scroll[Y]) / 30
            # Executing the float in scroll
            render_scroll = (int(self.scroll[X]), int(self.scroll[Y]))
            # spawning leafs
            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            # Render clouds
            self.clouds.update()
            self.clouds.render(self.display, offset = render_scroll)

            # Update and render part
            self.tilemap.render(self.display, offset = render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            if not self.dead:
                self.player.update(self.tilemap, (self.movement[Y] - self.movement[X], 0))
                self.player.render(self.display, offset=render_scroll)
            
            # [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][X] += projectile[Y]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][X] - img.get_width() / 2 - render_scroll[X], projectile[0][Y] - img.get_height() / 2 - render_scroll[Y]))
                if self.tilemap.solid_check(projectile[X]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[X], random.random() - 0.5 + (math.pi if projectile[Y] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.atacking)< 50:
                    if self.player.rect().collidepoint(projectile[X]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.sfx['hit'].play()
                        self.screenshake = max(16, self.screenshake)
                        for i in range(30):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 2
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                        
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)
                    
            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_sillhouette, offset)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset = render_scroll)
                if particle.type == 'leaf':
                    particle.pos[X] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.movement[X] = True
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.movement[Y] = True
                    if event.key == pygame.K_UP or event.key == ord('w'):
                       if self.player.jump():
                            self.sfx['jump'].play()
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.velocity[Y] = 3
                    if event.key == pygame.K_x:
                        self.player.dash()
                    if event.key == pygame.K_SPACE:
                        self.player.atack()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.movement[X] = False
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.movement[Y] = False
            # Resize the display
            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, BLACK, (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey(BLACK)
                self.display.blit(transition_surf, (0, 0))
                
            self.display_2.blit(self.display, (0, 0))
            
            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
            self.SCREEN.blit(pygame.transform.scale(self.display_2, self.SCREEN.get_size()), screenshake_offset)
            pygame.display.update()
            # Setting the FPS limits
            self.CLOCK.tick(self.FPS)

Game().run()


