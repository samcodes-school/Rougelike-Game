import pygame
import random
screen=pygame.display.set_mode((660, 500))

class enemyArrow(pygame.sprite.Sprite): 
  def __init__(self, x, y, direction, damage): 
    pygame.sprite.Sprite.__init__(self)
    self.surf = pygame.Surface((20, 20))
    self.image=pygame.image.load("Fireball.png")
    self.image=pygame.transform.scale(self.image, (100, 100))
    self.surf.set_colorkey((0, 0, 0)) #Getting rid of the black background around the fireball image
    self.rect=self.surf.get_rect()
    self.x=x
    self.y=y
    self.direction=direction
    self.damage=damage
    self.speed=random.randint(8, 12) #Making the speed random, to add more variety

  def draw(self):
    screen.blit(self.image, (self.x-40, self.y-40))

  def movement(self, group):
    self.x+=self.speed*self.direction #Goes in the direction of whatever spawned it
    if self.x>700: #Boundaries
      self.kill() #Prevents the buildup of fireballs at the edges of the screen 
    if self.x<0: #Boundaries
      self.kill()
    for sprite in group:
      if pygame.sprite.collide_rect(self, sprite):
        if sprite.invincibility==0: #Checks if the player is not invincible
          if sprite.blocking:
            sprite.health-=(self.damage/2)-sprite.armour #Blocking halves the damage, and armour subtracts a set amount of the damage
          else:
            sprite.health-=self.damage-sprite.armour
          sprite.invincibility=250 #Adds a period of invincibility to the player
        self.kill()
    self.rect.x=self.x #Updating the hitbox
    self.rect.y=self.y