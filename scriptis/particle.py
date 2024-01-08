X = 0
Y = 1

class Particlepos:
    def __init__(self, game, p_type, pos, velocity=[0, 0], frame=0):
        self.game = game
        self.type = p_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation = self.game.assets['particle/' + p_type].copy()
        self.animation.frame = frame
    
    def update(self):
        kill = False
        if self.animation.done:
            kill = True
        
        self.pos[X] += self.velocity[X]
        self.pos[Y] += self.velocity[Y]
        
        self.animation.update()
        
        return kill
    
    def render(self, surf, offset=(0, 0)):
        img = self.animation.img()
        surf.blit(img, (self.pos[X] - offset[X] - img.get_width() // 2, self.pos[Y] - offset[Y] - img.get_height() // 2))
    