import random

import pygame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player properties
player_width = 50
player_height = 50
player_speed = 10
player_jump = 10

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple Platformer')

clock = pygame.time.Clock()
background = pygame.image.load('ratLevel1BIG.png')
bgScroll = 0

#define obstacles - yellow
class GameObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Your object's image
        self.image = pygame.Surface((20, 20))  # Change size and image for your specific objects
        self.image.fill((255, 255, 0))  # Yellow color for demonstration
        self.rect = self.image.get_rect()
        # Set initial position (randomize as needed)
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = random.randint(0, SCREEN_HEIGHT)  # Adjust for your object's height
        # Add the object to the all_sprites group
        all_sprites.add(self)

# Define the player object
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.on_ground = False

    def update(self):
        self.acceleration = pygame.math.Vector2(0, 0.5)
        keys = pygame.key.get_pressed()
        self.velocity += self.acceleration
        self.collide(self.velocity.x, 0)
        self.rect.y += self.velocity.y
        self.on_ground = False
        self.collide(0, self.velocity.y)

    def collide(self, x, y):
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if x > 0:
                    self.rect.right = platform.rect.left
                    self.velocity.x = 0
                if x < 0:
                    self.rect.left = platform.rect.right
                    self.velocity.x = 0
                if y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.on_ground = True
                if y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0

# Define the platform object
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Add platforms to the game
platform = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
platforms.add(platform)
all_sprites.add(platform)

# Create the player
player = Player()
all_sprites.add(player)

#create objects
gamethings = []

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.on_ground:
                player.velocity.y = -player_jump

    all_sprites.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
       # player.rect.x -= player_speed
        bgScroll += player_speed/3
    if keys[pygame.K_RIGHT]:
        #player.rect.x += player_speed
        bgScroll -= player_speed/3

    #randomly spawned objects
    if random.randint(1,100) < 10:
        newObject = GameObject()
        gamethings.append(newObject)

    for obj in gamethings:
        obj.rect.x -= player_speed / 3

    game_objects = [obj for obj in gamethings if obj.rect.x > -20]

    if len(game_objects) < 10:  # Control the total number of objects
        x = random.randint(int(bgScroll), SCREEN_WIDTH + int(bgScroll))
        y = random.randint(0, SCREEN_HEIGHT - 20)  # Adjust for your object's height
        new_object = GameObject()
       # new_object.
        gamethings.append(new_object)

    screen.fill(WHITE)
    screen.blit(background, (bgScroll,0))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

