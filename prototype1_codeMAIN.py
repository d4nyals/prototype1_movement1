import pygame
import sys
import os

# constants
WIDTH = 1280
HEIGHT = 720
PLAYER_SPEED = 5
BACKGROUND_COLOUR = (255, 255, 255)
SCALE_FACTOR = 2

# check image files exist
for name in ["playerUp.png", "playerDown.png", "playerLeft.png", "playerRight.png"]:
    print(name, "exists:", os.path.exists(name))

class Player:
    def __init__(self, position):
        self.load_images()
        self.direction = "down"
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center=position)

    def load_images(self):
        # load and scale all direction images
        raw_images = {
            "up": pygame.image.load("playerUp.png"),
            "down": pygame.image.load("playerDown.png"),
            "left": pygame.image.load("playerLeft.png"),
            "right": pygame.image.load("playerRight.png")
        }

        self.images = {}
        for direction, image in raw_images.items():
            width, height = image.get_size()
            scaled_image = pygame.transform.scale(
                image, (int(width * SCALE_FACTOR), int(height * SCALE_FACTOR))
            )
            self.images[direction] = scaled_image

    def handle_input(self):
        # move the player and change image based on direction
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
            self.direction = "up"
            moved = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED
            self.direction = "down"
            moved = True
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
            self.direction = "left"
            moved = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
            self.direction = "right"
            moved = True

        if moved:
            self.image = self.images[self.direction]

        # stop player leaving the screen
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, screen):
        # draw player on the screen
        screen.blit(self.image, self.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.setup_window()
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player((WIDTH // 2, HEIGHT // 2))

    def setup_window(self):
        # create the game window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("prototype1 - movement and menu ")

    def handle_events(self):
        # check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # update player movement
        self.player.handle_input()

    def draw(self):
        # draw background and player
        self.screen.fill(BACKGROUND_COLOUR)
        self.player.draw(self.screen)
        pygame.display.flip()

    def run(self):
        # main game loop
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


# main program
if __name__ == "__main__":
    game = Game()
    game.run()
