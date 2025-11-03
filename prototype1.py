import pygame

# constants
width = 1280  # width of screen
height = 720  # height of screen
playerSpeed = 5  # speed of the player
background_colour = (0, 105, 0)
scale_factor = 1.75


class Player:
    def __init__(self, pos):
        self.loadImages()
        self.direction = "down"
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center=pos)

    def loadImages(self):
        # all images, showing direction. direction: image.png
        playerImages = {
            "up": pygame.image.load("playerUp.png"),
            "down": pygame.image.load("playerDown.png"),
            "left": pygame.image.load("playerLeft.png"),
            "right": pygame.image.load("playerRight.png") }

        self.images = {} # stores scaled images in this empty part
        for direction, image in playerImages.items():
            width, height = image.get_size()
            scaled_image = pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))
            self.images[direction] = scaled_image

    def handleInput(self):
        # move the player and change image based on direction
        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_w] or keys[pygame.K_UP]: # up arrow key
            self.rect.y -= playerSpeed
            self.direction = "up"
            moved = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]: # down arrow key
            self.rect.y += playerSpeed
            self.direction = "down"
            moved = True
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]: # left arrow key
            self.rect.x -= playerSpeed
            self.direction = "left"
            moved = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: # right arrow key
            self.rect.x += playerSpeed
            self.direction = "right"
            moved = True
        if moved:
            self.image = self.images[self.direction]
        # stop player leaving the screen
        self.rect.clamp_ip(pygame.Rect(0, 0, width, height))

    def draw(self, screen):
        # draw player on the screen
        screen.blit(self.image, self.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.setupWindow()
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player((width // 2, height // 2))

    def setupWindow(self):
        # create the game window
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Prototype 1 - movement and menu")

    def handleEvents(self):
        # check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # update player movement
        self.player.handleInput()

    def draw(self):
        # draw background and player
        self.screen.fill(background_colour)
        self.player.draw(self.screen)
        pygame.display.flip()


# below runs the game:
game = Game()

# main game loop (outside the class)
while game.running:
    game.handleEvents()
    game.update()
    game.draw()
    game.clock.tick(60)
