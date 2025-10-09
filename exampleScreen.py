import pygame # uses pygame
import sys # used to end the game effectively

# Screen dimensions
WIDTH = 1280
HEIGHT = 720
SPEED = 2  # Movement speed of player # 2 for normal, 5 for speed increase, # 1 for slowness

# Player class
class Player:
    def __init__(self, image_path, position): # use of __init__ initialises class Player
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=position) # sets the player at the center of the screen
  
# Keys which enable player movement
    def move(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= SPEED  # move UP
        if keys[pygame.K_s]:
            self.rect.y += SPEED  # move DOWN
        if keys[pygame.K_a]:
            self.rect.x -= SPEED  # move LEFT
        if keys[pygame.K_d]:
            self.rect.x += SPEED  # move RIGHT

    def draw(self, screen):
        screen.blit(self.image, self.rect) # draws the screen (display)

# game class
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Player Movement")
        self.clock = pygame.time.Clock()
        self.player = Player("player.png", (WIDTH // 2, HEIGHT // 2))
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed() # key registering
            self.player.move(keys)

            self.screen.fill((255, 255, 255))  # White background
            self.player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# Run the game
# possible to use Game().run()
