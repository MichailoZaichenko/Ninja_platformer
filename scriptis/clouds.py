from random import random, choice
COUNT_OF_CLOUDS = 16
X = 0
Y = 1

class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[X] += self.speed

    def render(self, surface, offset = (0, 0)):
        render_pos = (self.pos[X] - offset[X] * self.depth, self.pos[Y] - offset[Y] * self.depth)
        surface.blit(self.img, (render_pos[X] % (surface.get_width() + self.img.get_width()) - self.img.get_width(), render_pos[Y] % (surface.get_height() + self.img.get_height()) - self.img.get_height()))

class Clouds:
    def __init__(self, cloud_images, count = COUNT_OF_CLOUDS):
        self.clouds = []
        # Add random clounds
        for i in range(count):
            self.clouds.append(Cloud((random() * 99999, random() * 99999), choice(cloud_images), random() * 0.05 + 0.05, random() * 0.6 + 0.2))
        # Sorting by depth
        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surface, offset = (0, 0)):
        for cloud in self.clouds:
            cloud.render(surface, offset = offset)

