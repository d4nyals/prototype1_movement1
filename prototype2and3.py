
import pygame  # imports pygame
import random  # used for zombie spawning

# start variables
width = 1280  # width of screen - original value = 1280
height = 720  # height of screen - original value = 720
playerSpeed = 3  # original value = 3
background_colour = (100, 90, 100)  # original value = (0,0,51)
scale_factor = 1.5  # scales the playerImage - original value = 1.75
menu_colour = (100, 100, 100)  # grey menu background
bulletSpeed = 11  # speed of bullets

class Wall(pygame.sprite.Sprite):  # wall class
    def __init__(self, rect):
        super().__init__()  # initialise parent class correctly
        self.rect = pygame.Rect(rect)  # rect stores position + size for collisions
        self.image = pygame.Surface(self.rect.size)  # surface same size as wall
        self.image.fill((0, 0, 0))  # wall colour black

class Player:  # player class
    def __init__(self, pos):
        self.loadImages()  # loads and scales all sprites / images
        self.direction = "down"  # initial facing direction
        self.image = self.images[self.direction]  # select starting image
        self.rect = self.image.get_rect(center = pos)  # rectangle for collision
        self.health = 100  # player health
        self.score = 0  # player score

    def loadImages(self):  # load and scale player sprites
        playerImages = {"up": pygame.image.load("playerUp.png"),
                        "down": pygame.image.load("playerDown.png"),
                        "left": pygame.image.load("playerLeft.png"),
                        "right": pygame.image.load("playerRight.png")}  # images per direction
        self.images = {}
        for direction, image in playerImages.items():
            w, h = image.get_size()  # original width + height
            self.images[direction] = pygame.transform.scale(image, (int(w * scale_factor), int(h * scale_factor)))  # scale image

    def collisionMovement(self, dx, dy, walls):  # moves player and checks collisions
        self.rect.x += dx  # horizontal move
        for wall in walls:  # check horizontal collisions
            if self.rect.colliderect(wall.rect):
                if dx > 0: self.rect.right = wall.rect.left  # stop at left of wall
                elif dx < 0: self.rect.left = wall.rect.right  # stop at right of wall
        self.rect.y += dy  # vertical move
        for wall in walls:  # check vertical collisions
            if self.rect.colliderect(wall.rect):
                if dy > 0: self.rect.bottom = wall.rect.top  # stop at top of wall
                elif dy < 0: self.rect.top = wall.rect.bottom  # stop at bottom of wall

    def handleInput(self, walls):  # handle keyboard input
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]: dy = -playerSpeed; self.direction = "up"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]: dy = playerSpeed; self.direction = "down"
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]: dx = -playerSpeed; self.direction = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = playerSpeed; self.direction = "right"
        if dx or dy:  # if moving
            self.image = self.images[self.direction]  # update sprite
            self.collisionMovement(dx, dy, walls)  # check collisions
        self.rect.clamp_ip(pygame.Rect(0, 0, width, height))  # stay on screen

    def draw(self, screen): screen.blit(self.image, self.rect)  # draw player

class House:  # house structure class
    def __init__(self, x, y, width, height, door_width = 60, door_side = None, vertical_door = None):
        self.walls = pygame.sprite.Group()  # group to store all wall objects
        self.x = x; self.y = y; self.width = width; self.height = height
        self.door_width = door_width; self.door_side = door_side; self.vertical_door = vertical_door
        self.create_walls()  # build house walls

    def create_walls(self):  # creates walls with door gaps
        door_size = self.door_width
        sides = ['top', 'bottom', 'left', 'right']
        for side in sides:
            if (side == self.door_side or side == self.vertical_door):  # wall has door
                if side in ['top', 'bottom']:
                    y = self.y if side == 'top' else self.y + self.height - 10
                    self.walls.add(Wall((self.x, y, (self.width - door_size) // 2, 10)))  # left part
                    self.walls.add(Wall((self.x + (self.width + door_size) // 2, y, (self.width - door_size) // 2, 10)))  # right part
                else:  # vertical wall with door
                    x = self.x if side == 'left' else self.x + self.width - 10
                    self.walls.add(Wall((x, self.y, 10, (self.height - door_size) // 2)))  # top
                    self.walls.add(Wall((x, self.y + (self.height + door_size) // 2, 10, (self.height - door_size) // 2)))  # bottom
            else:  # normal wall
                if side == 'top': self.walls.add(Wall((self.x, self.y, self.width, 10)))
                elif side == 'bottom': self.walls.add(Wall((self.x, self.y + self.height - 10, self.width, 10)))
                elif side == 'left': self.walls.add(Wall((self.x, self.y, 10, self.height)))
                elif side == 'right': self.walls.add(Wall((self.x + self.width - 10, self.y, 10, self.height)))

class Zombie:  # enemy zombie class
    def __init__(self, pos):
        img = pygame.image.load("zombie.png") # zombie image
        w, h = img.get_size()
        self.image = pygame.transform.scale(img, (int(w * scale_factor), int(h * scale_factor)))
        self.rect = self.image.get_rect(center = pos)
        self.speed = 1.5

    def moveTowardsPlayer(self, player, walls):  # simple pathfinding towards player
        zombieX = self.rect.x; zombieY = self.rect.y
        playerX = player.rect.x; playerY = player.rect.y
        dx, dy = 0, 0
        if playerX > zombieX: dx = self.speed
        elif playerX < zombieX: dx = -self.speed
        if playerY > zombieY: dy = self.speed
        elif playerY < zombieY: dy = -self.speed
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: self.rect.right = wall.rect.left
                elif dx < 0: self.rect.left = wall.rect.right
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0: self.rect.bottom = wall.rect.top
                elif dy < 0: self.rect.top = wall.rect.bottom

    def draw(self, screen): screen.blit(self.image, self.rect)  # draw zombie

class Bullet:  # player bullet class
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 6, 6)  # small rectangle
        self.direction = direction  # bullet direction

    def moveBullet(self, walls = None):  # move bullet and check wall collision
        if self.direction == "up": self.rect.y -= bulletSpeed
        elif self.direction == "down": self.rect.y += bulletSpeed
        elif self.direction == "left": self.rect.x -= bulletSpeed
        elif self.direction == "right": self.rect.x += bulletSpeed
        if walls:
            for wall in walls:
                if self.rect.colliderect(wall.rect): return True
        return False

    def draw(self, screen): pygame.draw.rect(screen, (255, 255, 0), self.rect)  # draw bullet

class PowerUp:  # POWERUP CLASS
    def __init__(self, x, y, type):
        self.type = type
        img = pygame.image.load("powerupIcon.png")  # powerup image
        w, h = img.get_size()
        self.image = pygame.transform.scale(img, (int(w * 1), int(h * 1)))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self):
        pygame.init()  # initialise pygame
        self.setupWindow()  # create game window
        self.clock = pygame.time.Clock()  # FPS controller
        self.running = True  # main loop flag
        # wave variables
        self.wave = 1
        self.zombiesKilled = 0
        # powerup variables
        self.powerups = []
        self.freezeActive = False
        self.rapidFireActive = False
        self.freezeTimer = 0
        self.rapidTimer = 0
        self.activeText = ""  # text display for powerup
        self.textTimer = 0
        self.lastShot = 0  # shoot timer
        self.shootCooldown = 300

        self.menuScreen()  # display main menu
        self.startGame()  # initialise game

        self.gunshot_sound = pygame.mixer.Sound("gunshot.mp3")  # gunshot sound
        self.gunshot_sound.set_volume(0.05)  # set volume to 50
        self.waveComplete = pygame.mixer.Sound("waveComplete.mp3")  # sound for wave completion
        self.waveComplete.set_volume(0.20)
        self.gameOverMusic = pygame.mixer.Sound("gameOverMusic.mp3")  # game over sound
        self.gameOverMusic.set_volume(0.05)

    def structures(self): # strucutre class
        self.walls = pygame.sprite.Group()
        top_left_house = House(200, 120, 300, 150, door_side = 'bottom', vertical_door = 'left')
        self.walls.add(top_left_house.walls)
        bottom_right_house = House(900, 400, 180, 180, door_side = 'top', vertical_door = 'right')
        self.walls.add(bottom_right_house.walls)

    def startGame(self):
        self.player = Player((width // 2, height // 2))
        self.wave = 1  # reset wave to 1
        self.zombiesKilled = 0  # reset kill count
        self.structures()  # add houses/walls
        self.bullets = []
        self.zombies = []
        self.powerups = []
        # Reset powerup states when game restarts
        self.freezeActive = False
        self.rapidFireActive = False
        self.freezeTimer = 0
        self.rapidTimer = 0
        self.activeText = ""
        self.textTimer = 0
        for i in range(3):
            self.spawnZombie()  # initial zombies

    def setupWindow(self):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Top-down Zombie Game")

    def menuScreen(self):
        playButton = pygame.Rect(width // 2 - 100, height // 2 - 25, 200, 50)
        font = pygame.font.Font(None, 50)
        runningMenu = True
        while runningMenu:
            self.screen.fill(menu_colour)
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if playButton.collidepoint(mouse_pos): runningMenu = False
            if playButton.collidepoint(mouse_pos): pygame.draw.rect(self.screen, (255, 255, 0), playButton, 3)
            else: pygame.draw.rect(self.screen, (255, 255, 255), playButton, 3)
            text = font.render("PLAY", True, (255, 255, 255))
            text_rect = text.get_rect(center = playButton.center)
            self.screen.blit(text, text_rect)
            title_font = pygame.font.Font(None, 70)
            title_text = title_font.render("ZOMBIE RUSH", True, (0, 255, 0))
            title_rect = title_text.get_rect(center = (width // 2, height // 4))
            self.screen.blit(title_text, title_rect)
            pygame.display.flip()
            self.clock.tick(60)

    def spawnZombie(self):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            pos = (random.randint(0, width), 0)
        elif side == "bottom":
            pos = (random.randint(0, width), height)
        elif side == "left":
            pos = (0, random.randint(0, height))
        else:
            pos = (width, random.randint(0, height))
        if len(self.zombies) < 5 + self.wave:
            self.zombies.append(Zombie(pos))

    def gameOverScreen(self):
        button = pygame.Rect(width // 2 - 100, height // 2 + 50, 200, 50)
        font = pygame.font.Font(None, 70)
        small = pygame.font.Font(None, 30)
        running = True
        while running:
            self.screen.fill(menu_colour)
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.collidepoint(mouse_pos): running = False
            if button.collidepoint(mouse_pos): pygame.draw.rect(self.screen, (255, 255, 0), button, 3)
            else: pygame.draw.rect(self.screen, (255, 255, 255), button, 3)
            text = font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(text, text.get_rect(center = (width // 2, height // 3)))
            playAgainButton = small.render("PLAY AGAIN?", True, (255, 255, 255))
            self.screen.blit(playAgainButton, playAgainButton.get_rect(center = button.center))
            pygame.display.flip()
            self.clock.tick(60)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    now = pygame.time.get_ticks()
                    cooldown = 100 if self.rapidFireActive else self.shootCooldown  # RAPID FIRE REDUCES COOLDOWN
                    if now - self.lastShot > cooldown:
                        self.bullets.append(Bullet(self.player.rect.centerx, self.player.rect.centery, self.player.direction))
                        self.gunshot_sound.play()
                        self.lastShot = now

    def update(self): # update method
        self.player.handleInput(self.walls)
        for bullet in self.bullets[:]:
            if bullet.moveBullet(self.walls):
                self.bullets.remove(bullet)
            elif bullet.rect.right < 0 or bullet.rect.left > width or bullet.rect.bottom < 0 or bullet.rect.top > height:
                self.bullets.remove(bullet)

        for zombie in self.zombies[:]:
            if not self.freezeActive:  # FREEZE POWERUP STOPS MOVEMENT
                zombie.moveTowardsPlayer(self.player, self.walls)
            if zombie.rect.colliderect(self.player.rect):
                self.player.health -= 1

            for bullet in self.bullets[:]:
                if zombie.rect.colliderect(bullet.rect):
                    self.zombies.remove(zombie)
                    self.bullets.remove(bullet)
                    self.player.score += 1
                    self.zombiesKilled += 1
                    if self.zombiesKilled % 5 == 0:
                        self.wave += 1  # increase wave by 1
                        self.waveComplete.play()
                    if random.random() < 0.1: # 10% drop chance of powerup
                        pType = random.choice(["freeze","rapid","hp"])
                        self.powerups.append(PowerUp(zombie.rect.centerx, zombie.rect.centery, pType))
                    self.spawnZombie()
                    break

        # POWERUP COLLECTION
        for powerup in self.powerups[:]:
            if powerup.rect.colliderect(self.player.rect):
                now = pygame.time.get_ticks()
                if powerup.type == "freeze": # freeze powerup
                    self.freezeActive = True
                    self.freezeTimer = now
                    self.activeText = "FREEZE (10s)"
                    self.textTimer = now
                elif powerup.type == "rapid": # rapid fire powerup
                    self.rapidFireActive = True
                    self.rapidTimer = now
                    self.activeText = "RAPID FIRE (10s)"
                    self.textTimer = now
                elif powerup.type == "hp": # health powerup
                    if self.player.health < 100: # only used if player is low
                        self.player.health = min(100, self.player.health + 20)
                        self.activeText = "HP +20"
                        self.textTimer = now
                self.powerups.remove(powerup) # removes powerup when done
        # POWERUP TIMERS
        now = pygame.time.get_ticks()
        if self.freezeActive:
            remaining = 10 - int((now - self.freezeTimer)/1000)
            self.activeText = "FREEZE (" + str(max(0,remaining)) + "s)" # displays freeze text
            if now - self.freezeTimer > 10000:
                self.freezeActive = False
        if self.rapidFireActive:
            remaining = 10 - int((now - self.rapidTimer)/1000)
            self.activeText = "RAPID FIRE (" + str(max(0,remaining)) + "s)" # displays rapid text
            if now - self.rapidTimer > 10000:
                self.rapidFireActive = False
        # CLEAR POWERUP TEXT AFTER 10 SECONDS
        if self.activeText != "" and pygame.time.get_ticks() - self.textTimer > 10000:
            if now - self.textTimer > 10000:
                self.activeText = ""

        if self.player.health <= 0:  # if player's hp reaches 0
            self.gameOverMusic.play()  # PLAY GAME OVER MUSIC
            self.gameOverScreen()  # show game over screen
            self.startGame()  # reset game if play again

    def draw(self):
        self.screen.fill(background_colour)
        for wall in self.walls:
            self.screen.blit(wall.image, wall.rect)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for zombie in self.zombies:
            zombie.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)
        self.player.draw(self.screen)

        pygame.draw.rect(self.screen, (255, 0, 0), (20, 20, 200, 20))
        pygame.draw.rect(self.screen, (0, 255, 0), (20, 20, self.player.health * 2, 20))
        font = pygame.font.Font(None, 40)
        score_text = font.render("Score: " + str(self.player.score), True, (255, 255, 255))
        self.screen.blit(score_text, (20, 50))
        wave_font = pygame.font.Font(None, 40)
        wave_text = wave_font.render("Wave: " + str(self.wave), True, (255,255,255))
        self.screen.blit(wave_text, (width - 150, 20))
        if self.activeText != "":
            pfont = pygame.font.Font(None, 50)
            ptext = pfont.render(self.activeText, True, (255,255,0))
            self.screen.blit(ptext, ptext.get_rect(center=(width//2,40)))
        pygame.display.flip()

# game
game = Game()
while game.running:
    game.handleEvents()
    game.update()
    game.draw()
    game.clock.tick(60)
