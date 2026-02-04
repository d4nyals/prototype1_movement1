import pygame # imports pygame

# variables
width = 1280 # width of screen - original value = 1280
height = 720 # height of screen - original value = 720
playerSpeed = 3 # original value = 3
background_colour = (0, 0, 70) # original value = (0,0,51)
scale_factor = 1.75 # scales the playerImage - original value = 1.75
menu_colour = (100, 100, 100) # grey menu background
# --- ADDED ---
bulletSpeed = 8 # speed of bullets


class Wall(pygame.sprite.Sprite): # wall class
    def __init__(self, rect):
        super().__init__() # used to initialise parent class correctly
        self.rect = pygame.Rect(rect) # pos + size of wall, using for collision
        self.image = pygame.Surface(self.rect.size)
        self.image.fill((0, 0, 0)) # fill image colour with black

class Player: # player class
    def __init__(self, pos):
        self.loadImages() # generates image for my player
        self.direction = "down"
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center=pos)

    def loadImages(self): # load and scale the player sprites
        playerImages = {"up": pygame.image.load("playerUp.png"), "down": pygame.image.load("playerDown.png"), "left": pygame.image.load("playerLeft.png"), "right": pygame.image.load("playerRight.png")} # PLAYER IMAGES
        self.images = {}
        for direction, image in playerImages.items():
            w, h = image.get_size()
            self.images[direction] = pygame.transform.scale(image, (int(w * scale_factor), int(h * scale_factor)))

    def collisionMovement(self, dx, dy, walls):  # move sideways then check for collisions
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

    def handleInput(self, walls): # handles the input in game (key movements (WASD) also arrow keys)
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
        self.rect.clamp_ip(pygame.Rect(0, 0, width, height)) # stops the player from leaving the screen

    def draw(self, screen): # draws the screen
        screen.blit(self.image, self.rect)

# --- ADDED ---
class Bullet: # bullet class
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 6, 6) # bullet size
        self.direction = direction
        
    def move(self):
        if self.direction == "up": # player goes up
            self.rect.y -= bulletSpeed
        elif self.direction == "down": # player goes down
            self.rect.y += bulletSpeed
        elif self.direction == "left": # player goes left
            self.rect.x -= bulletSpeed
        elif self.direction == "right": # player goes right
            self.rect.x += bulletSpeed
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.rect) # draws bullet 

class House: # house structure class, primarily used for dimensions of the house
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
        door_size = 60 # gap created for the player to enter the structures
        sides = ['top', 'bottom', 'left', 'right'] # labels for the walls and wall position
        for side in sides:
            if self.door_side == side:
                if side in ['top', 'bottom']:
                    y = self.y if side == 'top' else self.y + self.height - 10
                    self.walls.add(Wall((self.x, y, (self.width - door_size) // 2, 10)))
                    self.walls.add(Wall((self.x + (self.width + door_size) // 2, y, (self.width - door_size) // 2, 10)))
                else:  # left // right
                    x = self.x if side == 'left' else self.x + self.width - 10
                    self.walls.add(Wall((x, self.y, 10, (self.height - door_size) // 2)))
                    self.walls.add(Wall((x, self.y + (self.height + door_size) // 2, 10, (self.height - door_size) // 2)))
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
        self.clock = pygame.time.Clock() # acts as a time counter
        self.running = True
        self.menuScreen()  # show menu before player can move
        self.player = Player((width // 2, height // 2))
        self.structures()  # creates the houses
        self.bullets = [] # creates a list for bullets

    def setupWindow(self): # changes the window title
        self.screen = pygame.display.set_mode((width, height)) # dimensions related to window title
        pygame.display.set_caption("Top-down Zombie Game") # window caption

    def menuScreen(self): # menu screen
        playButton = pygame.Rect(width//2 - 100, height//2 - 25, 200, 50)
        font = pygame.font.Font(None, 50)
        runningMenu = True
        while runningMenu:
            self.screen.fill(menu_colour)
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if playButton.collidepoint(mouse_pos):
                        runningMenu = False

            if playButton.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (200, 200, 200), playButton, 3)
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), playButton, 3)

            text = font.render("PLAY", True, (255, 255, 255)) # Play text button
            text_rect = text.get_rect(center=playButton.center)
            self.screen.blit(text, text_rect)

            title_font = pygame.font.Font(None, 80)
            title_text = title_font.render("TOP-DOWN ZOMBIE GAME", True, (255, 255, 255)) # title caption
            title_rect = title_text.get_rect(center=(width//2, height//4))
            self.screen.blit(title_text, title_rect)

            pygame.display.flip()
            self.clock.tick(60)

    def structures(self): # creates structures, such as houses for the player to use as cover
        self.walls = pygame.sprite.Group()
        top_left_house = House(200, 120, 300, 150, door_side='bottom')  # top house (rectangle)
        self.walls.add(top_left_house.walls)
        bottom_right_house = House(900, 400, 180, 180, door_side='top') # bottom house
        self.walls.add(bottom_right_house.walls)

    def handleEvents(self): # handles the events needed to close game, use items etc.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit event
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, self.player.direction) # bullet
                    self.bullets.append(bullet)

    def update(self):  # update actions
        self.player.handleInput(self.walls)
        for bullet in self.bullets[:]: # making a copy of the bullet list using iteration
            bullet.move()
            if bullet.rect.right < 0 or bullet.rect.left > width or bullet.rect.bottom < 0 or bullet.rect.top > height:
                self.bullets.remove(bullet) # removes bullet once it leaves the screen
      
    def draw(self): # draw background and objects
        self.screen.fill(background_colour)
        for wall in self.walls:
            self.screen.blit(wall.image, wall.rect) 
        for bullet in self.bullets:
            bullet.draw(self.screen) # draws the bullet onto the screen
      

        self.player.draw(self.screen)
        pygame.display.flip() # update the contents of the entire display

game = Game() # used to execute the game

while game.running:
    game.handleEvents() # handling events in game
    game.update() # update game
    game.draw() # draw in game
    game.clock.tick(60) # FPS for game -- SET TO 60
