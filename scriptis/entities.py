import pygame
import random
import math
from scriptis.particle import Particlepos as Particle
from scriptis.spark import Spark

X = 0
Y = 1

class PhysicsEntity:
    def __init__(self, game, entity_type, pos, size):
        self.game = game
        self.type = entity_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.animation_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
        self.atack_time = 50
        self.atack_lenth = 8
        
        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[X], self.pos[Y], self.size[X], self.size[Y])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/'  + self.action].copy()

    def update(self, tilemap, movement = (0,0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[X] + self.velocity[X], movement[Y] + self.velocity[Y])
        # X
        self.pos[X] += frame_movement[X]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[X] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[X] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[X] = entity_rect.x
        # Y
        self.pos[Y] += frame_movement[Y]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[Y] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[Y] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[Y] = entity_rect.y
        # Flipping the img 
        if movement[X] > 0:
            self.flip = False
        if movement[X] < 0:
            self.flip = True

        self.last_movement = movement

        self.velocity[Y] = min(5, self.velocity[Y] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[Y] = 0

        self.animation.update()
    
    def render(self, surface, offset = (0, 0)):
        # surface.blit(self.game.assets['player'], (self.pos[X]- offset[X], self.pos[Y] - offset[Y]))
        surface.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[X] - offset[X] + self.animation_offset[X], self.pos[Y] - offset[Y] + self.animation_offset[Y]))

class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)
        
        self.walking = 0
        
    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[Y] + 23)):
                if (self.collisions['right'] or self.collisions['left']):
                    self.flip = not self.flip
                else:
                    movement = (movement[X] - 0.5 if self.flip else 0.5, movement[Y])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
            if not self.walking:
                dis = (self.game.player.pos[X] - self.pos[X], self.game.player.pos[Y] - self.pos[Y])
                if (abs(dis[Y]) < 16):
                    if (self.flip and dis[X] < 0):
                        self.game.sfx['shoot'].play()
                        self.game.projectiles.append([[self.rect().centerx - 7, self.rect().centery], -1.5, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][X], random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and dis[X] > 0):
                        self.game.sfx['shoot'].play()
                        self.game.projectiles.append([[self.rect().centerx + 7, self.rect().centery], 1.5, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][X], random.random() - 0.5, 2 + random.random()))
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)
        
        super().update(tilemap, movement=movement)
        
        if movement[X] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
            
        if abs(self.game.player.atacking) >= self.atack_time:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screenshake = max(16, self.game.screenshake)
                self.game.sfx['hit'].play()
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                return True

        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screenshake = max(16, self.game.screenshake)
                self.game.sfx['hit'].play()
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                return True
            
    def render(self, surface, offset=(0, 0)):
        super().render(surface, offset=offset)
        
        if self.flip:
            surface.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[X], self.rect().centery - offset[Y]))
        else:
            surface.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[X], self.rect().centery - offset[Y]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0
        self.atacking = 0
    
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        TIME_FLYING_AFTER_THAT_PLAYER_DIE = 135
        self.air_time += 1
        
        if self.air_time > TIME_FLYING_AFTER_THAT_PLAYER_DIE:
            if not self.game.dead:
                self.game.screenshake = max(16, self.game.screenshake)
            self.game.dead += 1
        
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1
            
        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[Y] = min(self.velocity[Y], 0.5)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')
        
        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[X] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')
        # Dash
        if abs(self.dashing) in {60, 50}:
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity[X] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[X] *= 0.1
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))

        # Atack particles
        if abs(self.atacking) in {self.atack_time + 10, self.atack_time}:
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                particle_velocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=particle_velocity, frame=random.randint(0, 7)))
        if self.atacking > 0:
            self.atacking = max(0, self.atacking - 1)
        if self.atacking < 0:
            self.atacking = min(0, self.atacking + 1)
        if abs(self.atacking) > self.atack_time:
            self.velocity[X] = abs(self.atacking) / self.atacking * self.atack_lenth
            if abs(self.atacking) == self.atack_time + 1:
                self.velocity[X] *= 0.1
            particle_velocity = [abs(self.atacking) / self.atacking * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=particle_velocity, frame=random.randint(0, 7)))
                
        if self.velocity[X] > 0:
            self.velocity[X] = max(self.velocity[X] - 0.1, 0)
        else:
            self.velocity[X] = min(self.velocity[X] + 0.1, 0)
    
    def render(self, surface, offset=(0, 0)):
        if abs(self.atacking) <= self.atack_time:
            super().render(surface, offset=offset)
        if abs(self.dashing) <= 50:
            super().render(surface, offset=offset)
            
    def jump(self):
        X_VELOSITY_WALL_JUMP = 3
        Y_VELOSITY_WALL_JUMP = -3
        Y_VELOSITY_JUMP = -3.5

        if self.wall_slide:
            if self.flip and self.last_movement[X] < 0:
                self.velocity[X] = X_VELOSITY_WALL_JUMP
                self.velocity[Y] = Y_VELOSITY_WALL_JUMP
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[X] > 0:
                self.velocity[X] = -X_VELOSITY_WALL_JUMP
                self.velocity[Y] = Y_VELOSITY_WALL_JUMP
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
                
        elif self.jumps:
            self.velocity[Y] = Y_VELOSITY_JUMP
            self.jumps -= 1
            self.air_time = 5
            return True
    
    def dash(self):
        if not self.dashing:
            self.game.sfx['dash'].play()
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60

    def atack(self):
        if not self.atacking:
            self.game.sfx['dash'].play()
            if self.flip:
                self.atacking = -(self.atack_time + 3)
            else:
                self.atacking = self.atack_time + 3
    



