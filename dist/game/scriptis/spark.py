import math
import pygame
X = 0
Y = 1

class Spark:
    def __init__(self, pos, angle, speed):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        
    def update(self):
        self.pos[X] += math.cos(self.angle) * self.speed
        self.pos[Y] += math.sin(self.angle) * self.speed
        
        self.speed = max(0, self.speed - 0.1)
        return not self.speed
    
    def render(self, surface, offset=(0, 0)):
        render_points = [
            (self.pos[X] + math.cos(self.angle) * self.speed * 3 - offset[X], self.pos[Y] + math.sin(self.angle) * self.speed * 3 - offset[Y]),
            (self.pos[X] + math.cos(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[X], self.pos[Y] + math.sin(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[Y]),
            (self.pos[X] + math.cos(self.angle + math.pi) * self.speed * 3 - offset[X], self.pos[Y] + math.sin(self.angle + math.pi) * self.speed * 3 - offset[Y]),
            (self.pos[X] + math.cos(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[X], self.pos[Y] + math.sin(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[Y]),
        ]
        
        pygame.draw.polygon(surface, (255, 255, 255), render_points)