from tiles import Tile
import pygame
from settings import tileSize, screen_width
from player import Player
from imageOverlay import ImageOverlay


class Level:
    def __init__(self, level_data, surface, image_path, initPos):

        #level setup
        self.display_surface = surface
        self.level_data = level_data
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0
        #self.background = '../sunhacks2023/graphics/level1Backgroundnew'.convertAlpha()
        #self.rect = self.background.get_rect(topLeft=(0, 0))
        self.image_overlay = ImageOverlay(image_path, self.display_surface, initPos)
        self.trueBack = pygame.image.load('../sunhacks2023/graphics/dirty_tiles.jpg')  # Load your overlay image
        self.tBRect = self.trueBack.get_rect()
        self.tBRect.topleft = (0, 0)  # Initial position
        self.initialPos = (0,0)
        self.nextLevel = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.hazard_tiles = pygame.sprite.Group()
        self.finish_tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index,row in enumerate(layout):
            for col_index,cell in enumerate(row):
                if cell == 2:
                    x = col_index * tileSize
                    y = row_index * tileSize
                    tile = Tile((x, y), tileSize)
                    self.hazard_tiles.add(tile)
                if cell == 1:
                    x = col_index * tileSize
                    y = row_index * tileSize
                    tile = Tile((x, y), tileSize)
                    self.tiles.add(tile)
                if cell == 3:
                    x = col_index * tileSize
                    y = row_index * tileSize
                    player_sprite = Player((x, y))
                    self.initialPos = (x, y)
                    self.player.add(player_sprite)
                if cell == 4:
                    x = col_index * tileSize
                    y = row_index * tileSize
                    tile = Tile((x, y), tileSize)
                    self.finish_tiles.add(tile)



    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 2.5 and direction_x<0:
            self.world_shift = 5
            player.speed = 0
        elif player_x > screen_width - (screen_width/2.5) and direction_x>0:
            self.world_shift = -5
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

        if player.rect.top > 1200:
            print('you died you cheeky wanker')
            self.setup_level(self.level_data)
            self.image_overlay.reset()

    def hazard_collision(self):
        player = self.player.sprite

        # Check for collisions with hazard tiles
        for sprite in self.hazard_tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                print('you died you cheeky wanker')
                self.setup_level(self.level_data)
                self.image_overlay.reset()

    def finish_collision(self):
        player = self.player.sprite

        for sprite in self.finish_tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                print('good work you cheeky wanker')
                self.nextLevel = 1

    def run(self):

        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        #self.display_surface.blit(self.trueBack, self.tBRect)

        self.image_overlay.update(self.world_shift)
        self.image_overlay.draw()

        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.hazard_collision()
        self.player.draw(self.display_surface)

        return self.nextLevel

