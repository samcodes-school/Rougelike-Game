import pygame
screen=pygame.display.set_mode((660, 500))

class Arrow(pygame.sprite.Sprite): 
  def __init__(self, x, y, direction, damage): 
    pygame.sprite.Sprite.__init__(self)
    self.surf = pygame.Surface((20, 20))
    self.image = pygame.image.load("Fireball.png")
    self.image=pygame.transform.scale(self.image, (100, 100))
    self.surf.set_colorkey((0, 0, 0))
    self.rect=self.surf.get_rect()
    self.x=x
    self.y=y
    self.direction=direction
    self.damage=damage

  def draw(self):
    screen.blit(self.image, (self.x-40, self.y-40))

  def movement(self, group):
    self.x+=10*self.direction
    if self.x>700:
      self.kill()
    if self.x<0:
      self.kill()
    for sprite in group:
      if pygame.sprite.collide_rect(self, sprite):
        sprite.health-=self.damage
        self.kill()
    self.rect.x=self.x
    self.rect.y=self.y