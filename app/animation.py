# app/animation.py

import katagames_engine as kengi

kengi.init('hd')
pygame = kengi.pygame



class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_name, monster_size=(200, 200)):
        super(AnimateSprite, self).__init__()
        self.monster_size = monster_size
        self.image = pygame.image.load(f'src/{sprite_name}.png')
        self.image = pygame.transform.scale(self.image, monster_size)
        self.current_image = 0
        self.images = animations.get(sprite_name)
        self.animation = False

    def start_animate_sprite(self):
        self.animation = True

    def animate_sprite(self, loop=False):
        if self.animation:
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
                if loop is False:
                    self.animation = False
            self.image = self.images[self.current_image]
            self.image = pygame.transform.scale(self.image, self.monster_size)

def load_animation_images(sprite_name):
    images = []
    path = f"src/{sprite_name}/{sprite_name}"
    for num in range(1, 24):
        image_path = path + str(num) + '.png'
        images.append(pygame.image.load(image_path))
    return images

animations = {
    'mummy': load_animation_images('mummy'),
    'alien': load_animation_images('alien'),
    'player': load_animation_images('player')
}
