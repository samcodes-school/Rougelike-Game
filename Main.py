import pygame


class Player(pygame.sprite.Sprite):  #Making our player class

    def __init__(self):
        self.x = 200
        self.y = 50
        self.width = 20
        self.height = 20
        self.vel = 5
        self.direction = 1
        self.dashCooldown = 0
        self.isJump = False
        self.jumpCount = 7

        self.g = 5

    def keys(self):  #Making the controls
        keys = pygame.key.get_pressed()
        if keys[
            pygame.
                    K_RIGHT] and self.x < 670:  #Adding boundaries EVENTUALLY NOT NEEDED
            self.x += self.vel
            self.direction = 1
        elif keys[pygame.K_LEFT] and self.x > 5:
            self.x -= self.vel
            self.direction = -1
        if keys[pygame.K_DOWN] and self.dashCooldown <= 0:  #Dashing and boundaries
            if self.x < 100 and self.direction == -1:
                self.x += (self.x * self.direction)
            elif self.x > 570 and self.direction == 1:
                self.x += ((670 - self.x) * self.direction)
            else:
                self.x += (100 * self.direction)
            self.dashCooldown = 250

    def jump(self):  #Jumping
        keys = pygame.key.get_pressed()
        if self.isJump == False and self.y == 200:
            if keys[pygame.K_UP]:
                self.isJump = True
        else:
            if self.isJump == True:
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5  #Parabola
                self.jumpCount -= 1
            else:
                self.jumpCount = 7
                self.isJump = False
        if self.y < 200 and self.isJump == False:
            self.y += self.g
        if self.y > 200:  ## Boundry
            self.y = 200
            print(self.isJump)

    def draw(self):  #Drawing the player (at the moment it is a rectangle)
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.x, self.y, self.width, self.height))

    def update(self):  #Updates the cooldown
        if self.dashCooldown > 0:
            self.dashCooldown -= 10

## SETUP ##
pygame.init()
screen = pygame.display.set_mode((700, 350))
pygame.display.set_caption("First Game")

player = Player()  #Instantiating the player
clock = pygame.time.Clock()

## RUNNING ##
running = True
while running:  #The game loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    player.keys()  #Calling all of the things the player can do
    player.jump()
    screen.fill((0, 0, 0))
    player.draw()  #Drawing the player
    pygame.display.update()  #And updating the screen
    clock.tick(60)
    player.update()

pygame.quit()