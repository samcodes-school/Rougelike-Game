import pygame
import random
import animation
screen=pygame.display.set_mode((660, 500))
black=(0, 0, 0)

class Boss(pygame.sprite.Sprite): #Boss Class - a buffed knight class
  def __init__(self, x, y, health):
    pygame.sprite.Sprite.__init__(self)
    self.surf = pygame.Surface((30, 30))
    self.frames=pygame.image.load("BossEnemy.png")
    self.images=animation.spriteSheet(self.frames)
    self.animation_list=[]
    self.animation_steps=[3, 3, 4, 4, 4, 4, 7, 7]
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
    self.health=health
    self.attackCooldown=250
    self.rangedCooldown=250
    self.damage=25
    self.rangedDamage=15
    self.maxHealth=health
    self.moving=True
    self.melee=False
    self.ranged=False
    self.shop=False
    self.speed=3

  def getImages(self):
    for i in self.animation_steps:
      tempList=[]
      for _ in range(i):
        tempList.append(self.images.get_image(self.counter, 32, 32, 2, black))
        self.counter+=1
      self.animation_list.append(tempList)

  def updateAnimation(self, sprite, sprite1):
    if self.shop==False:
      current_time=pygame.time.get_ticks()
      if current_time-self.last_update>=self.animation_cooldown:
        self.frame+=1
        self.last_update=current_time
        if self.frame>=len(self.animation_list[self.action]):
          self.frame=0
  
      if self.action==2 or self.action==3:
        if self.frame==3:
          self.melee=False
          if self.action==2:
            self.frame=0
            self.action=0
          else:
            self.frame=0
            self.action=1
  
      if self.action==4 or self.action==5:
        if self.frame==3:
          self.ranged=False
          if self.action==4:
            self.frame=0
            self.action=0
          else:
            self.frame=0
            self.action=1
  
      if self.action==6 or self.action==7:
        if self.frame==6 and sprite1.worldLevel%10==0:
          sprite.XP+=50
          sprite.money+=random.randint(25, 75)
          self.shop=True
        elif self.frame==6 and sprite1.worldLevel%10!=0:
          sprite.XP+=25
          sprite.money+=random.randint(25, 50)
          self.kill()
    else:
      pass

  def animate(self):
    if self.moving==True and self.direction==1:
      self.action=0
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0
    if self.moving==True and self.direction==-1:
      self.action=1
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0

    if self.melee==True and self.direction==1:
      self.action=2
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0
    if self.melee==True and self.direction==-1:
      self.action=3
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0

    if self.ranged==True and self.direction==1:
      self.action=4
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0
    if self.ranged==True and self.direction==-1:
      self.action=5
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0
    
    if self.health<=0 and self.direction==1:
      self.moving=False
      self.ranged=False
      self.melee=False
      self.action=6
      self.animation_cooldown=500
    if self.health<=0 and self.direction==-1:
      self.moving=False
      self.ranged=False
      self.melee=False
      self.action=7
      self.animation_cooldown=500
      
  def draw(self):
    screen.blit(self.animation_list[self.action][self.frame], (self.x-16, self.y-14))
    pygame.draw.rect(screen, ((128, 0, 128)), pygame.Rect(self.x, self.y-15, 30*(self.health/self.maxHealth), 10))

  def movement(self, sprite):
    if self.health>0:
      self.x+=self.speed*self.direction
      if self.x>sprite.x: #Follows the player
        self.direction=-1
      else:
        self.direction=1
      self.rect.x=self.x #Updates the hitbox
      self.rect.y=self.y
      if self.rangedCooldown>0: #Updates the ranged cooldown
        self.rangedCooldown-=10

  def attack(self, ranged, list, group):
    if self.health>0:
      for sprite in group:
        if self.x-sprite.x>150 or sprite.x-self.x>150: #If the boss is far enough away from the player, it shoots fireballs
          if self.rangedCooldown==0:
            self.ranged=True
            arrow=ranged(self.x, self.y, self.direction, self.rangedDamage) #Creating a fireball
            list.add(arrow) #And adding it to the enemy fireball list
            self.rangedCooldown=250 #Adding a cooldown
        else:
          if pygame.sprite.collide_rect(self, sprite) and self.attackCooldown==250: #Checking if the boss has collided with the player
            self.attackCooldown-=1
          if self.attackCooldown<250: #Once the boss has collided with the player, it attacks after a delay, which gives the player time to move out of range
            self.attackCooldown-=10
          if self.attackCooldown<=0:
            self.melee=True
            attackRect=pygame.Rect(self.x+(20*self.direction), self.y, 20, 30) #Creating a rectangle to detect collision with the player
            if attackRect.colliderect(sprite.rect) and sprite.invincibility==0: #Checking to see if the player has been hit by the boss
              if sprite.blocking:
                sprite.health-=(self.damage/2)-sprite.armour #Blocking halves the damage, and armour negates a part of the damage dealt
                sprite.invincibility=250 #Giving the player a short period of invincibility
              else:
                sprite.health-=self.damage-sprite.armour
                sprite.invincibility=250
            self.attackCooldown=250