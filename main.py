import pygame

import Platforms
from Platforms import platforms
from Platforms import platformList
screen = pygame.display.set_mode((700, 350))

class Player(pygame.sprite.Sprite):  # Making our player class

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("penguin.JPG")
        self.surf = pygame.transform.scale(self.surf, (30, 30))
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.vel = 5
        self.direction = 1
        self.isColliding = False
        self.dashCooldown = 0
        self.attackCooldown=0
        self.isJump = False
        self.jumpCount = 7
        self.startingPos = 1
        self.isGravity = False
        self.health=100
        self.invincibility=0
        self.blocking=False
        self.activeWeapon="Sword"
        self.damage=10

        self.g = 7
        self.yDirection = 0
        self.canMoveLeft = True
        self.canMoveRight = True

    def keys(self): #Making the controls
        keys=pygame.key.get_pressed()
        if keys[pygame.K_d] and self.x<670 and self.canMoveRight: #Adding boundaries
            self.x+=self.vel
            self.direction=1
        elif keys[pygame.K_a] and self.x>5 and self.canMoveLeft:
            self.x-=self.vel
            self.direction=-1
        if keys[pygame.K_s] and self.dashCooldown<=0: #Dashing and boundaries
            if self.x<100 and self.direction==-1 and self.canMoveLeft:
                self.x+=(self.x*self.direction)
            elif self.x>570 and self.direction==1 and self.canMoveRight:
                self.x+=((670-self.x)*self.direction)
            else:
                self.x+=(100*self.direction)
            self.dashCooldown=250

    def horizontalCollisions(self):

        for i in Platforms.platforms.sprites():
            if i.rect.colliderect(self.rect):
                print("Woah! Colliding!")
                if self.direction > 0:
                    self.rect.right = i.rect.left
                    return
                if self.direction < 0:
                    self.rect.left = i.rect.right
                    return

    def verticalCollisions(self):

        for i in Platforms.platforms.sprites():
            if i.rect.colliderect(self.rect):
                if self.yDirection < 0:
                    self.rect.top = i.rect.bottom
                    self.jumpCount = 0
                    return
                elif self.yDirection > 0:
                    self.rect.bottom = i.rect.top
                    self.isColliding = True
                    self.jumpCount = 7
                    print("Woah!! Collisions!")
                    self.isGravity = True
                    return
            else:
                self.isColliding = False

    def gravity(self):

        if self.isGravity:
            self.yDirection = 1
        elif self.isJump:
            self.yDirection = -1

        if self.isColliding is False and self.isJump is False: # Gravity if not jumping.
            self.isGravity = True
        else:
            self.isGravity = False

        if self.isGravity:
            self.y += self.g
        elif self.isGravity is False:
            self.y = self.y

    def jump(self):  # Jumping
        keys = pygame.key.get_pressed()

        # if self.isColliding and self.y == platformList[self.platform].rect.top:
        #     self.y = platformList[self.platform].rect.y - self.height # Vertical collisions
        # if self.isColliding and self.y == platformList[self.platform].rect.bottom and platformList[self.platform].passthrough == False:
        #     pass # Going to be a head bump mechanic. Still need to code.
        # if self.isColliding and self.rect.bottom > platformList[self.platform].rect.y and self.direction == 1:
        #     self.x = platformList[self.platform].rect.x #Horizontal collisions
        # if self.isColliding and self.rect.bottom > platformList[self.platform].rect.y and self.direction == -1:
        #     self.x = platformList[self.platform].rect.x + platformList[self.platform].rect.width

        if self.isJump is False and self.isColliding: ## If on ground, and not jumping
            if keys[pygame.K_SPACE]:
                self.isJump = True # Jump
                self.isGravity = False


        if self.y > 350: # BOUNDARY. SWIYCH WITH DEATH SCREEN.
            self.y = 1

        if keys[pygame.K_SPACE] and self.isColliding:
            self.isJump = True

        elif self.isJump:
            if self.jumpCount >= -7:
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5 #Simulates a parabola, where jumpCount are the x coordinates and self.y is the y coordinate, and the x intercepts are at -7 and 7
                self.jumpCount -= 1
            else:
                self.jumpCount = 7 #At jumpCount=7 the player is back on the ground
                self.isJump = False



    # import pygame
    # class Player(pygame.sprite.Sprite): #Making our player class
    #     def __init__(self, x, y):
    #         pygame.sprite.Sprite.__init__(self)
    #         self.x = x
    #         self.y = y
    #         self.surf = pygame.image.load("penguin.JPG")
    #         self.surf = pygame.transform.scale(self.surf, (30, 30))
    #         self.surf.set_colorkey((0, 0, 0))
    #         self.rect = self.surf.get_rect()
    #         self.vel = 5
    #         self.direction=1
    #         self.dashCooldown=0
    #         self.attackCooldown=0
    #         self.isJump = False
    #         self.jumpCount = 7

    def weapons(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.activeWeapon="Sword"
        if keys[pygame.K_2]:
            self.activeWeapon="Bow"

    def attack(self, group, ranged, list): #A bit finnicky - probably not the best but it works
        left, middle, right=pygame.mouse.get_pressed()
        if left and self.attackCooldown==0:
            if self.activeWeapon=="Sword":
                print("Sword attack")
                for sprite in group:
                    if sprite.x>self.x and self.x+100>sprite.x and self.direction==1:
                        sprite.health-=self.damage
                        print(sprite.health)
                    if sprite.x<self.x and self.x-100<sprite.x and self.direction==-1:
                        sprite.health-=self.damage
                        print(sprite.health)
                self.attackCooldown=250
            elif self.activeWeapon=="Bow":
                print("Bow attack")
                arrow=ranged(self.x, self.y, self.direction)
                list.add(arrow)
                self.attackCooldown=250
        elif right:
            self.blocking=True
        elif not right:
            self.blocking=False

    def draw(self): #Drawing the player (at the moment it is a rectangle)
        screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, ((255, 0, 0)), self.rect, 2)

    def update(self): #Updates the cooldown
        if self.dashCooldown>0:
            self.dashCooldown-=10
        if self.attackCooldown>0:
            self.attackCooldown-=10
        if self.invincibility>0:
            self.invincibility-=10
        self.rect.x = self.x
        self.rect.y = self.y
        if self.health<=0:
            print("Game Over")
            pygame.quit()


player = Player(20, 20)  # Instantiating the player