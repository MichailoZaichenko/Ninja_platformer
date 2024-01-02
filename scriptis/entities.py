import pygame

class PhysicsEntity:
    def __init__(self, game, entity_type, position, size):
        self.game = game
        self.entity_type = entity_type
        self.position = list(position)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.animation_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
        
        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.entity_type + '/'  + self.action].copy()

    def update(self, tilemap, movement = (0,0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        # X
        self.position[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.position[0] = entity_rect.x
        # Y
        self.position[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.position[1] = entity_rect.y
        # Flipping the img 
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()
    
    def render(self, surface, offset = (0, 0)):
        # surface.blit(self.game.assets['player'], (self.position[0]- offset[0], self.position[1] - offset[1]))
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.position[0] - offset[0] + self.animation_offset[0], self.position[1] - offset[1] + self.animation_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, position, size):
        super().__init__(game, 'player', position, size)
        self.air_time = 0
    
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement = movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')