import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, type):
        super().__init__()
        self.image = pygame.Surface((size, size))
        if type == 1:
            self.image.fill('grey')
        else:
            self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift
