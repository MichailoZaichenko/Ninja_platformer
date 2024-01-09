import sys
import pygame
# import files
from scriptis. tilemap import TIlemap, TILE_SIZE
from scriptis.utils import load_image, load_images, Animation
RENDER_SCALE = 2.0
X = 0
Y = 1
Editing_level = 3

class Editor:
    def __init__(self):
        pygame.init()

        # Name of window
        pygame.display.set_caption("editor")

        # Some constands
        SCREEN_WIDTH = 1280//2
        SCREEN_HIGHT = 960//2
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
            }

        self.movement = [False, False, False, False]
        # Useage on class Tilemap
        self.tilemap = TIlemap(self, TILE_SIZE)

        try:
            self.tilemap.load(f'data/maps/{Editing_level}.json')
        except FileNotFoundError:
            pass

        #Camera scrolling
        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
    
    def run(self):
        # Main loop
        while True:
            # Filling display with black
            self.display.fill((0,0,0))
                                # right             left
            self.scroll[X] += (self.movement[Y] - self.movement[X]) * 2
                                # down              up
            self.scroll[Y] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[X]), int(self.scroll[Y]))

            self.tilemap.render(self.display, offset = render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)
            # Some pos verables
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[X] / RENDER_SCALE, mouse_pos[Y] / RENDER_SCALE)
            tile_pos = (int((mouse_pos[X] + self.scroll[X]) // self.tilemap.tile_size), int((mouse_pos[Y] + self.scroll[Y]) // self.tilemap.tile_size))

            if self.ongrid:
                # Preview of tile placing
                self.display.blit(current_tile_img, (tile_pos[X] * self.tilemap.tile_size - self.scroll[X], tile_pos[Y] * self.tilemap.tile_size - self.scroll[Y]))
            else:
                self.display.blit(current_tile_img, mouse_pos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[X]) + ';' + str(tile_pos[Y])]  = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos }
            if self.right_clicking:
                tile_location = str(tile_pos[X]) + ';' + str(tile_pos[Y])
                if tile_location in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_location]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][X] - self.scroll[X], tile['pos'][Y] - self.scroll[Y], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mouse_pos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5, 5))


            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if  not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mouse_pos[X] + self.scroll[X], mouse_pos[Y] + self.scroll[Y])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                                                                    # looping
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                                                                    # looping
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                                                                    # looping
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                                                                    # looping
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                    
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.movement[X] = True
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.movement[Y] = True
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save(f'data/maps/{Editing_level}.json')
                    if event.key == pygame.K_LSHIFT or event.mod & pygame.KMOD_SHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.movement[X] = False
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.movement[Y] = False
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT or event.mod & pygame.KMOD_SHIFT:
                        self.shift = False
            # Resize the display
            self.SCREEN.blit(pygame.transform.scale(self.display, self.SCREEN.get_size()), (0, 0))
            pygame.display.update()
            # Setting the FPS limits
            self.CLOCK.tick(self.FPS)

Editor().run()


