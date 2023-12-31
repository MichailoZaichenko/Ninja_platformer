import pygame
import os

BASE_IMG_PATH = 'data/images/'
# Load 1 img from derictory and remove black back ground
def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0,0,0))
    return img
# Load imgs from derictory and remove black back ground
def load_images(path):
    images = []
    # use sorted to sort corectly for Linux users
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images
# Base for animatins
class Animation:
    def __init__(self, images, img_duration = 5, loop = True):
        self.images = images
        self.loop = loop
        self.img_duration = img_duration
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
        