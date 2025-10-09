import pygame
import sys

# Screen size (default resolution is set to 1280x720)
WIDTH = 1280
HEIGHT = 720

class Player:
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Player Display")
        self.clock = pygame.time.Clock()
        self.player = Player("player.png", (WIDTH // 2, HEIGHT // 2))
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))  # White background
            self.player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# Run the game
Game().run()
