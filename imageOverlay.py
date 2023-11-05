import pygame

class ImageOverlay:
    def __init__(self, image_path, surface, pos):
        self.display_surface = surface
        self.image = pygame.image.load('../sunhacks2023/graphics/level1BackgroundFixed.png')  # Load your overlay image
        self.rect = self.image.get_rect()
        self.initPos = pos
        self.rect.topleft = self.initPos  # Initial position

    def update(self, world_shift):
        self.rect.x += world_shift

    def reset(self):
        self.rect.topleft = self.initPos

    def draw(self):
        self.display_surface.blit(self.image, self.rect)
