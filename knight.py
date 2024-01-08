import pygame
import random
import animation
screen=pygame.display.set_mode((660, 500))
black=(0, 0, 0)

class Knight(pygame.sprite.Sprite): #Knight class
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.surf = pygame.Surface((30, 30))
    self.frames=pygame.image.load("KnightEnemy.png")
    self.images=animation.spriteSheet(self.frames)
    self.animation_list=[]
    self.animation_steps=[3, 3, 4, 4, 4, 4]
    self.action=0
    self.last_update=pygame.time.get_ticks()
    self.animation_cooldown=75
    self.frame=0
    self.counter=0
    self.rect=self.surf.get_rect()
    self.x=x
    self.y=y
    self.direction=1
    self.width=20
    self.height=20
    self.health=100
    self.attackCooldown=250
    self.damage=20
    self.maxHealth=100
    self.moving=True
    self.attacking=False
    self.fastSpeed=random.randint(5, 7)
    self.normalSpeed=random.randint(2, 4)

  def getImages(self):
    for i in self.animation_steps:
      tempList=[]
      for _ in range(i):
        tempList.append(self.images.get_image(self.counter, 32, 32, 2, black))
        self.counter+=1
      self.animation_list.append(tempList)

  def updateAnimation(self, sprite):
    current_time=pygame.time.get_ticks()
    if current_time-self.last_update>=self.animation_cooldown:
      self.frame+=1
      self.last_update=current_time
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0

    if self.action==2 or self.action==3:
      if self.frame==3:
        self.attacking=False
        if self.action==2:
          self.frame=0
          self.action=0
        else:
          self.frame=0
          self.action=1

    if self.action==4 or self.action==5:
      if self.frame==3:
        sprite.XP+=15
        sprite.money+=random.randint(10, 20)
        self.kill()

  def animate(self):
    if self.moving==True and self.direction==1:
      self.action=0
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0
    if self.moving==True and self.direction==-1:
      self.action=1
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0

    if self.attacking==True and self.direction==1:
      self.action=2
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0
    if self.attacking==True and self.direction==-1:
      self.action=3
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0

    if self.health<=0 and self.direction==1:
      self.action=4
      self.animation_cooldown=500
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0
    if self.health<=0 and self.direction==-1:
      self.action=5
      self.animation_cooldown=500
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0
  
  def draw(self):
    screen.blit(self.animation_list[self.action][self.frame], (self.x-16, self.y-14))
    pygame.draw.rect(screen, ((128, 0, 128)), pygame.Rect(self.x, self.y-15, 30*(self.health/self.maxHealth), 10))

  def movement(self, sprite):
    if self.health>0:
      if self.x-sprite.x>150 or sprite.x-self.x>150: #Making it so the enemy speeds up if it is far enough away from the player
        self.x+=self.fastSpeed*self.direction
      else:
        self.x+=self.normalSpeed*self.direction
      if self.x>sprite.x:
        self.direction=-1
      else:
        self.direction=+1
      self.rect.x=self.x
      self.rect.y=self.y

  def attack(self, group):
    if self.health>0:
      for sprite in group:
        if pygame.sprite.collide_rect(self, sprite) and self.attackCooldown==250:
          self.attackCooldown-=1
        if self.attackCooldown<250:
          self.attackCooldown-=10
        if self.attackCooldown<=0:
          self.attacking=True
          attackRect=pygame.Rect(self.x+(20*self.direction), self.y, 20, 30)
          if attackRect.colliderect(sprite.rect) and sprite.invincibility==0:
            if sprite.blocking:
              sprite.health-=(self.damage/2)-sprite.armour
              sprite.invincibility=250
            else:
              sprite.health-=self.damage-sprite.armour
              sprite.invincibility=250
          self.attackCooldown=250