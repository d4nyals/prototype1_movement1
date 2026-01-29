import pygame
import sys # not needed
import os # not needed

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


