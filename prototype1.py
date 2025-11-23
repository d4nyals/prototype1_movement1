import pygame # imports pygame

# variables
width = 1280 # original value = 1280
height = 720 # original value = 720
playerSpeed = 3 # original value = 3
background_colour = (0, 0, 70) # original value = (0,0,51)
scale_factor = 1.75 # original value = 1.75


class Wall(pygame.sprite.Sprite): # wall class
    def __init__(self, rect):
        super().__init__() # super used
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((0, 0, 0))


class Player: # player class
    def __init__(self, pos):
        self.loadImages() # generates image for my player
        self.direction = "down"
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center=pos)

    def loadImages(self):
        # load and scale the player sprites
        playerImages = {"up": pygame.image.load("playerUp.png"), "down": pygame.image.load("playerDown.png"), "left": pygame.image.load("playerLeft.png"), "right": pygame.image.load("playerRight.png")}

        self.images = {}
        for direction, image in playerImages.items():
            w, h = image.get_size()
            self.images[direction] = pygame.transform.scale(image, (int(w * scale_factor), int(h * scale_factor)))

    def collisionMovement(self, dx, dy, walls):
        # move sideways then check for collisions
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                elif dx < 0:
                    self.rect.left = wall.rect.right

        # move vertically then check for collisions
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                elif dy < 0:
                    self.rect.top = wall.rect.bottom

    def handleInput(self, walls): # handles the key movements (WASD) also arrow keys
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -playerSpeed
            self.direction = "up"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = playerSpeed
            self.direction = "down"
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -playerSpeed
            self.direction = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = playerSpeed
            self.direction = "right"

        if dx or dy:
            self.image = self.images[self.direction]
            self.collisionMovement(dx, dy, walls)

        # stops the player from leaving the screen
        self.rect.clamp_ip(pygame.Rect(0, 0, width, height))

    def draw(self, screen): # draws the screen
        screen.blit(self.image, self.rect)


class House: # house class
    def __init__(self, x, y, width, height, door_width=60, door_side=None): # creates the walls for house and adds the door gaps
        self.walls = pygame.sprite.Group()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.door_width = door_width
        self.door_side = door_side
        self.create_walls()

    def create_walls(self): # creates the walls needed for the houses / structures
        door_size = 60
        sides = ['top', 'bottom', 'left', 'right']
        for side in sides:
            if self.door_side == side:
                if side in ['top', 'bottom']:
                    y = self.y if side == 'top' else self.y + self.height - 10
                    self.walls.add(Wall((self.x, y, (self.width - door_size) // 2, 10)))
                    self.walls.add(Wall((self.x + (self.width + door_size) // 2, y, (self.width - door_size) // 2, 10)))
                else:  # left // right
                    x = self.x if side == 'left' else self.x + self.width - 10
                    self.walls.add(Wall((x, self.y, 10, (self.height - door_size) // 2)))
                    self.walls.add(
                        Wall((x, self.y + (self.height + door_size) // 2, 10, (self.height - door_size) // 2)))
            else:  # normal wall
                if side == 'top':
                    self.walls.add(Wall((self.x, self.y, self.width, 10)))
                elif side == 'bottom':
                    self.walls.add(Wall((self.x, self.y + self.height - 10, self.width, 10)))
                elif side == 'left':
                    self.walls.add(Wall((self.x, self.y, 10, self.height)))
                elif side == 'right':
                    self.walls.add(Wall((self.x + self.width - 10, self.y, 10, self.height)))


class Game: # game class
    def __init__(self): # sets up everything for the game
        pygame.init()
        self.setupWindow()
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player((width // 2, height // 2))
        self.structures()  # creates teh houses

    def setupWindow(self): # changes the window title
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Top-down Zombie Game ~ Prototype 1")

    def structures(self):
        # creates structures, such as houses for the player to use as cover
        self.walls = pygame.sprite.Group()

        # top house (rectangle)
        top_left_house = House(200, 120, 300, 150, door_side='bottom')
        self.walls.add(top_left_house.walls)
        # bottom house
        bottom_right_house = House(900, 400, 180, 180, door_side='top')
        self.walls.add(bottom_right_house.walls)

    def handleEvents(self):
        # basic quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        # update player movement
        self.player.handleInput(self.walls)

    def draw(self):
        # draw background and objects
        self.screen.fill(background_colour)
        for wall in self.walls:
            self.screen.blit(wall.image, wall.rect)
        self.player.draw(self.screen)
        pygame.display.flip()

game = Game() # used to execute the game

while game.running:
    game.handleEvents()
    game.update()
    game.draw()
    game.clock.tick(60) # FPS for game
