import pygame
screen=pygame.display.set_mode((660, 500))

class smallHazard(pygame.sprite.Sprite):
  def __init__ (self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.x=x
    self.y=y
    self.surf=pygame.Surface((40, 30))
    self.image=pygame.image.load("smallHazard.png")
    self.image=pygame.transform.scale(self.image, (40, 30))
    self.rect=self.surf.get_rect()
    self.rect.x=self.x
    self.rect.y=self.y
    
  def draw(self):
    screen.blit(self.image, (self.x, self.y-1))

  def collision(self, sprite): #Checking for collision with the player
    if pygame.sprite.collide_rect(self, sprite):
      sprite.health-=1 #Deals damage to the player

class largeHazard(pygame.sprite.Sprite):
  def __init__ (self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.x=x
    self.y=y
    self.surf=pygame.Surface((100, 30)) #Making the hazard larger
    self.image=pygame.image.load("largeHazard.png")
    self.image=pygame.transform.scale(self.image, (100, 30)) 
    self.rect=self.surf.get_rect()
    self.rect.x=self.x
    self.rect.y=self.y

  def draw(self):
    screen.blit(self.image, (self.x, self.y))

  def collision(self, sprite):
    if pygame.sprite.collide_rect(self, sprite):
      sprite.health-=1