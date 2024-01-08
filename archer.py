import pygame
import random
import animation
screen=pygame.display.set_mode((660, 500))
black=(0, 0, 0)

class archerEnemy(pygame.sprite.Sprite): #Enemy archer
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.surf = pygame.Surface((30, 30))
    self.frames=pygame.image.load("MageEnemy.png")
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
    self.health=50
    self.maxHealth=50
    self.attackCooldown=0
    self.damage=10
    self.moving=True
    self.attacking=False

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
        sprite.XP+=10
        sprite.money+=random.randint(5, 10)
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

  def movement(self, sprite): #The archer slowly moves away from the player, while still facing it, so fireballs go towards the player
    if self.health>0:
      if self.x>100 and self.x<550:
        self.x+=-1*self.direction
      if self.x>=600 and self.direction==-1: #Setting up boundaries 
        self.x+=1*self.direction
      if self.x>=600 and self.direction==1:
        self.x-=1*self.direction
      if self.x<=100 and self.direction==1: 
        self.x+=1*self.direction
      if self.x<=100 and self.direction==-1: 
        self.x-=1*self.direction
        
      if self.x>sprite.x:
        self.direction=-1
      else:
        self.direction=1
      if self.attackCooldown>0:
        self.attackCooldown-=10
      self.rect.x=self.x
      self.rect.y=self.y

  def attack(self, ranged, list):
    if self.health>0:
      if self.attackCooldown==0:
        self.attacking=True
        arrow=ranged(self.x, self.y, self.direction, self.damage)
        list.add(arrow)
        self.attackCooldown=500