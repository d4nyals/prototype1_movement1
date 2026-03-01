import pygame  # imports pygame

# variables
width = 1280  # width of screen - original value = 1280
height = 720  # height of screen - original value = 720
playerSpeed = 3  # original value = 3
background_colour = (100, 90, 100)  # original value = (0,0,51)
scale_factor = 1.5  # scales the playerImage - original value = 1.75
menu_colour = (100, 100, 100)  # grey menu background

bulletSpeed = 11  # speed of bullets


class Wall(pygame.sprite.Sprite):  # wall class
    def __init__(self, rect):
        super().__init__()  # used to initialise parent class correctly
        self.rect = pygame.Rect(rect)  # creates rect (pos + size of wall) , used for collision
        self.image = pygame.Surface(self.rect.size) # creates surface same size as the wall
        self.image.fill((0, 0, 0))  # fill image colour with black


class Player:  # player class
    def __init__(self, pos):
        self.loadImages()  # loads and scales all sprites / images
        self.direction = "down" # sets the player to face down when the game starts
        self.image = self.images[self.direction] # selects the playerDown image
        self.rect = self.image.get_rect(center=pos) # create rect

    def loadImages(self):  # load and scale the player sprites
        playerImages = {"up": pygame.image.load("playerUp.png"),
                        "down": pygame.image.load("playerDown.png"),
                        "left": pygame.image.load("playerLeft.png"),
                        "right": pygame.image.load("playerRight.png")}  # player images for each direction
        self.images = {} # stores scaled images
        for direction, image in playerImages.items():
            w, h = image.get_size() # gets original width + height of image
            self.images[direction] = pygame.transform.scale(image, (int(w * scale_factor), int(h * scale_factor)))
            # scales image using scale_factor then stores it

    def collisionMovement(self, dx, dy, walls):  # moves then check for collisions
        self.rect.x += dx # moves player horizontally
        for wall in walls:
            if self.rect.colliderect(wall.rect): # if a collision occurs
                if dx > 0:
                    self.rect.right = wall.rect.left # stops at left edge of wall
                elif dx < 0:
                    self.rect.left = wall.rect.right # stop at right edge of wall
        self.rect.y += dy  # move vertically then check for collisions
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0:
                    self.rect.bottom = wall.rect.top # stop at top of wall
                elif dy < 0:
                    self.rect.top = wall.rect.bottom # stop at bottom of wall

    def handleInput(self, walls):  # handles the input in game (key movements (WASD) also arrow keys)
        keys = pygame.key.get_pressed() # gets info on keyboard
        dx, dy = 0, 0 # movement amount

        # movement controls (works with WASD + Arrow keys) only one direction can work at a time
        if keys[pygame.K_w] or keys[pygame.K_UP]: # if W key / UP arrow key is pressed
            dy = -playerSpeed
            self.direction = "up" # updates player direction to look up
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]: # if S key / DOWN arrow key is pressed
            dy = playerSpeed
            self.direction = "down" # updates player direction to look down
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]: # if A key / LEFT arrow key is pressed
            dx = -playerSpeed
            self.direction = "left" # updates player direction to look left
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: # if D key / RIGHT arrow key is pressed
            dx = playerSpeed
            self.direction = "right" # updates player direction to look right
        if dx or dy: # if player moves
            self.image = self.images[self.direction] # updates the player's image
            self.collisionMovement(dx, dy, walls) # collision detection
        self.rect.clamp_ip(pygame.Rect(0, 0, width, height))  # stops the player from leaving the screen

    def draw(self, screen): # draws rect representing player
        screen.blit(self.image, self.rect)


class House:  # house structure class, primarily used for dimensions of the house
    def __init__(self, x, y, width, height, door_width=60, door_side=None, vertical_door=None):
        # creates the walls for house and adds the door gaps
        self.walls = pygame.sprite.Group() # group which stores wall objects
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.door_width = door_width # width of the door
        self.door_side = door_side # which horizontal wall contains a door gap
        self.vertical_door = vertical_door # which vertical wall contains a door gap
        self.create_walls() # creates and builds the house walls

    def create_walls(self):  # creates the walls needed for the houses / structures
        door_size = self.door_width  # gap created for the player to enter the structures
        sides = ['top', 'bottom', 'left', 'right']  # labels for the walls and wall position
        for side in sides:
            if (side == self.door_side or side == self.vertical_door): # wall has door
                if side in ['top', 'bottom']:
                    y = self.y if side == 'top' else self.y + self.height - 10
                    self.walls.add(Wall((self.x, y, (self.width - door_size) // 2, 10))) # left half
                    self.walls.add(Wall((self.x + (self.width + door_size) // 2, y, (self.width - door_size) // 2, 10))) # right half
                else:  # vertical door
                    x = self.x if side == 'left' else self.x + self.width - 10
                    self.walls.add(Wall((x, self.y, 10, (self.height - door_size) // 2)))
                    self.walls.add(Wall((x, self.y + (self.height + door_size) // 2, 10, (self.height - door_size) // 2)))
            else:  # regular wall
                if side == 'top':
                    self.walls.add(Wall((self.x, self.y, self.width, 10)))
                elif side == 'bottom':
                    self.walls.add(Wall((self.x, self.y + self.height - 10, self.width, 10)))
                elif side == 'left':
                    self.walls.add(Wall((self.x, self.y, 10, self.height)))
                elif side == 'right':
                    self.walls.add(Wall((self.x + self.width - 10, self.y, 10, self.height)))


class Bullet:  # bullet class
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 6, 6) # creates a small rectangle (6x6) as the bullet
        self.direction = direction # bullet travels in the direction where player is facing

    def moveBullet(self, walls=None): # bullet movement with wall collision
        if self.direction == "up":  # bullet goes up
            self.rect.y -= bulletSpeed
        elif self.direction == "down":  # bullet goes down
            self.rect.y += bulletSpeed
        elif self.direction == "left":  # bullet goes left
            self.rect.x -= bulletSpeed
        elif self.direction == "right":  # bullet goes right
            self.rect.x += bulletSpeed

        # check collision with walls
        if walls:  # only check if walls group is provided
            for wall in walls:
                if self.rect.colliderect(wall.rect):  # bullet hits wall
                    return True  # indicate bullet should be removed
        return False

    def draw(self, screen): # draws rect representing the bullet
        pygame.draw.rect(screen, (255, 255, 0), self.rect)


class Game:  # game class
    def __init__(self):  # sets up everything for the game
        pygame.init() # initialises pygame modules
        self.setupWindow() # create window
        self.clock = pygame.time.Clock()  # controls FPS (frames per second)
        self.running = True # controls main game loop
        self.menuScreen()  # show menu before starting the game
        self.player = Player((width // 2, height // 2)) # creates / spawns player in the centre of the screen
        self.structures()  # creates the houses
        self.bullets = []  # creates a list to store any active bullets

    def setupWindow(self):  # method which is used to create the game window
        self.screen = pygame.display.set_mode((width, height))
        # creates the main game window (surface object)
        pygame.display.set_caption("Top-down Zombie Game")  # sets window caption at the top

    def menuScreen(self):  # displays start menu before the main game begins
        playButton = pygame.Rect(width // 2 - 100, height // 2 - 25, 200, 50)
        # ^ creates a rect for a play button
        font = pygame.font.Font(None, 50) # create a font object
        runningMenu = True # boolean used to control the menu loop
        while runningMenu: # main menu loop  (runs until runningMenu is False)
            self.screen.fill(menu_colour) # fills screen with background colour
            mouse_pos = pygame.mouse.get_pos() # gets current mouse position
            for event in pygame.event.get(): # checks every event (keyboard, mouse)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit() # Fully closes the program
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if playButton.collidepoint(mouse_pos):
                        # ^ checks if mouse click happened inside button
                        runningMenu = False # Ends menu loop and starts the game

            if playButton.collidepoint(mouse_pos):  # if mouse is currently hovering over the button
                pygame.draw.rect(self.screen, (255, 255, 0), playButton, 3) # draws yellow outline around button
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), playButton, 3) # becomes normal when not hovering

            text = font.render("PLAY", True, (255, 255, 255))  # Play text button
            text_rect = text.get_rect(center=playButton.center) # creates a rectangle for text
            self.screen.blit(text, text_rect) # draws the text onto the screen (at text_rect position)

            title_font = pygame.font.Font(None, 70) # creates the title font
            title_text = title_font.render("ZOMBIE RUSH", True, (0, 255, 0))  # renders title caption
            title_rect = title_text.get_rect(center=(width // 2, height // 4)) # puts title in the middle but slightly higher
            self.screen.blit(title_text, title_rect) # draws the title onto the screen
            pygame.display.flip() # updates display
            self.clock.tick(60)# 60 FPS menu

    def structures(self): # creates structures, such as houses for the player to use as cover
        self.walls = pygame.sprite.Group() # creates group to store all wall objects
        top_left_house = House(200, 120, 300, 150, door_side='bottom', vertical_door='left')
        # first house with 2 doors
        self.walls.add(top_left_house.walls) # adds all wall sprites from first house into main wall group
        bottom_right_house = House(900, 400, 180, 180, door_side='top', vertical_door='right')
        # second house with 2 doors
        self.walls.add(bottom_right_house.walls) # adds second house walls to wall group

    def handleEvents(self):  # handles all the runtime events (keyboard, quit, etc)
        for event in pygame.event.get(): # loops through event
            if event.type == pygame.QUIT:  # if player chooses to close the window
                self.running = False # stop main game loop
            if event.type == pygame.KEYDOWN: # detects when down key is pressed
                if event.key == pygame.K_SPACE:  # if the space button is pressed
                    bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, self.player.direction)  # bullet
                    self.bullets.append(bullet) # add bullet to the active bullet list

    def update(self):  # update actions
        self.player.handleInput(self.walls)
        for bullet in self.bullets[:]:  # looping through a copy of the bullet list
            if bullet.moveBullet(self.walls):  # remove bullet if it collides with wall
                self.bullets.remove(bullet)
            elif bullet.rect.right < 0 or bullet.rect.left > width or bullet.rect.bottom < 0 or bullet.rect.top > height:
                self.bullets.remove(bullet)  # removes bullet once it leaves the screen

    def draw(self):  # draw background and objects
        self.screen.fill(background_colour)
        for wall in self.walls:
            self.screen.blit(wall.image, wall.rect)
        for bullet in self.bullets:
            bullet.draw(self.screen)  # draws the bullet onto the screen
        self.player.draw(self.screen)  # draw screen
        pygame.display.flip()  # update the contents of the entire display


game = Game()  # create Game object

while game.running:
    game.handleEvents()  # handling events in game
    game.update()  # update game (positions)
    game.draw()  # draws everything
    game.clock.tick(60)  # FPS for the game -- LIMITED TO 60
