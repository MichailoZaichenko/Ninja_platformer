import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()
        # Name of window
        pygame.display.set_caption("NINJA")

        # Some constands
        SCREEN_WIDTH = 1280
        SCREEN_HIGHT = 960
        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT)) 
        self.FPS = 60
        self.CLOCK = pygame.time.Clock()

        self.img = pygame.image.load('data/images/clouds/cloud_1.png')
        self.img.set_colorkey((0,0,0))

        self.img_pos = [160, 260]
        self.movement = [False, False]

        self.collision_area = pygame.Rect(50, 50, 300, 50)
    
    def run(self):
        # Main loop
        while True:
            self.SCREEN.fill((14, 143, 134))

            # Make cloud move. And convert bullians(True(1)/False(0)) to int
            self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5
            self.SCREEN.blit(self.img, self.img_pos)

            img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())
            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.SCREEN, (0, 100, 255), self.collision_area)
            else:
                pygame.draw.rect(self.SCREEN, (0, 50, 155), self.collision_area)

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.movement[1] = False

            pygame.display.update()
            self.CLOCK.tick(self.FPS)

Game().run()


