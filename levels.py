import pygame
screen=pygame.display.set_mode((660, 500))

class door(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.surf=pygame.Surface((30, 30))
    self.image=pygame.image.load("doorRed.png") #The images for the door
    self.image=pygame.transform.scale(self.image, (30, 30))
    self.image1=pygame.image.load("doorPurple.png")
    self.image1=pygame.transform.scale(self.image1, (30, 30))
    self.rect=self.surf.get_rect()
    self.rect.x=x
    self.rect.y=y
    self.worldLevel=1 #The level the player is on
    self.open=True #Whether or not the door is open
    self.spawnCooldown=1000 #The spawn cooldown for boss fights

  def draw(self):
    if self.open==True: #If the door is open, it draws the red door
      screen.blit(self.image, (self.rect.x, self.rect.y))
    else: #Otherwise it draws the purple one (for boss fights)
      screen.blit(self.image1, (self.rect.x, self.rect.y))

  def newLevel(self, sprite, list1, list2, list3, list4, list5, list6, list7, list8, class1, class2, class3, class4, class5, class6): #All of the lists and classes are to instantiate enemies and add them to lists depending on what level it is
    if pygame.sprite.collide_rect(self, sprite) and sprite.y==200 and self.open==True: #If the player is touching the door, it sets up the next level, and sprite.y==200 is necessary to prevent the player's y values from going crazy because of the way jumping works
      sprite.x=10 #Resets the player's position
      sprite.y=200
      self.rect.x=620 #Resets the door's position
      self.rect.y=198
      self.worldLevel+=1 #Increases the level by one

      #Gets rid of all old enemies, fireballs, and enemy fireballs
      pygame.sprite.Group.empty(list1) 
      pygame.sprite.Group.empty(list2)
      pygame.sprite.Group.empty(list3)
      pygame.sprite.Group.empty(list4)
      pygame.sprite.Group.empty(list5)
      pygame.sprite.Group.empty(list6)
      pygame.sprite.Group.empty(list7)
      pygame.sprite.Group.empty(list8)
      
      if self.worldLevel==6: #Based on the level, it creates enemies and adds them to enemyList as well as their own list
        grunt=class1(500, 200)
        list1.add(grunt)
        list5.add(grunt)
        for sprite in list5: #Gets the images for the enemies, so animation works
          sprite.getImages()
      elif self.worldLevel==7:
        mage=class2(500, 200)
        list2.add(mage)
        list5.add(mage)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==8:
        knight=class3(500, 200)
        list3.add(knight)
        list5.add(knight)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==10:
        boss=class4(700, 200, 150)
        list4.add(boss)
        list5.add(boss)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==12:
        grunt=class1(500, 200)
        grunt1=class1(600, 200)
        list1.add(grunt, grunt1)
        list5.add(grunt, grunt1)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==13:
        mage=class2(200, 200)
        mage1=class2(500, 200)
        list2.add(mage, mage1)
        list5.add(mage, mage1)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==14:
        grunt=class1(500, 200)
        mage=class2(500, 200)
        list1.add(grunt)
        list2.add(mage)
        list5.add(grunt, mage)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==15:
        grunt=class1(500, 200)
        knight=class3(600, 200)
        list1.add(grunt)
        list3.add(knight)
        list5.add(grunt, knight)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==16:
        mage=class2(500, 200)
        knight=class3(600, 200)
        list2.add(mage)
        list3.add(knight)
        list5.add(mage, knight)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==17:
        grunt=class1(500, 200)
        grunt1=class1(550, 200)
        knight=class3(600, 200)
        list1.add(grunt, grunt1)
        list3.add(knight)
        list5.add(grunt, grunt1, knight)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==18:
        knight=class3(600, 200)
        knight1=class3(500, 200)
        list3.add(knight, knight1)
        list5.add(knight, knight1)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==20:
        self.spawnCooldown=1000
        boss=class4(700, 200, 200)
        list4.add(boss)
        list5.add(boss)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==21:
        grunt=class1(500, 200)
        grunt1=class1(600, 200)
        grunt2=class1(700, 200)
        list1.add(grunt, grunt1, grunt2)
        list5.add(grunt, grunt1, grunt2)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==22:
        grunt=class1(500, 200)
        mage=class2(300, 200)
        mage1=class2(500, 200)
        list1.add(grunt)
        list2.add(mage, mage1)
        list5.add(grunt, mage, mage1)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==23:
        mage=class2(500, 200)
        mage1=class2(600, 200)
        mage2=class2(700, 200)
        list2.add(mage, mage1, mage2)
        list5.add(mage, mage1, mage2)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==24:
        mage=class2(500, 200)
        mage1=class2(600, 200)
        knight=class3(700, 200)
        list2.add(mage, mage1)
        list3.add(knight)
        list5.add(mage, mage1, knight)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==25:
        grunt=class1(500, 200)
        grunt1=class1(600, 200)
        grunt2=class1(700, 200)
        grunt3=class1(400, 200)
        list1.add(grunt, grunt1, grunt2, grunt3)
        list5.add(grunt, grunt1, grunt2, grunt3)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==26:
        knight=class3(600, 200)
        knight1=class3(500, 200)
        knight2=class3(400, 200)
        list3.add(knight, knight1, knight2)
        list5.add(knight, knight1, knight2)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==27:
        knight=class3(600, 200)
        knight1=class3(500, 200)
        grunt=class1(400, 200)
        grunt1=class1(700, 200)
        list1.add(grunt, grunt1)
        list3.add(knight, knight1)
        list5.add(knight, knight1, grunt, grunt1)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==28:
        knight=class3(600, 200)
        knight1=class3(500, 200)
        grunt=class1(400, 200)
        grunt1=class1(700, 200)
        mage=class2(100, 200)
        list1.add(grunt, grunt1)
        list2.add(mage)
        list3.add(knight, knight1)
        list5.add(knight, knight1, grunt, grunt1, mage)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==30:
        self.spawnCooldown=1000
        boss=class4(700, 200, 250)
        list4.add(boss)
        list5.add(boss)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==31:
        smallHazard=class5(300, 229)
        list8.add(smallHazard)
      elif self.worldLevel==32:
        largeHazard=class6(300, 229)
        list8.add(largeHazard)
      elif self.worldLevel==33:
        smallHazard=class5(150, 229)
        smallHazard1=class5(300, 229)
        smallHazard2=class5(450, 229)
        list8.add(smallHazard, smallHazard1, smallHazard2)
      elif self.worldLevel==34:
        grunt=class1(400, 200)
        smallHazard=class5(300, 229)
        list1.add(grunt)
        list5.add(grunt)
        list8.add(smallHazard)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==35:
        mage=class2(400, 200)
        largeHazard=class6(300, 229)
        list2.add(mage)
        list5.add(mage)
        list8.add(largeHazard)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==36:
        grunt=class1(400, 200)
        mage=class2(400, 200)
        smallHazard=class5(350, 229)
        smallHazard1=class5(200, 229)
        list1.add(grunt)
        list2.add(mage)
        list5.add(grunt, mage)
        list8.add(smallHazard, smallHazard1)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==37:
        grunt=class1(400, 200)
        grunt1=class1(500, 200)
        knight=class3(600, 200)
        largeHazard=class6(200, 229)
        largeHazard1=class6(400, 229)
        list1.add(grunt, grunt1)
        list3.add(knight)
        list5.add(grunt, grunt1, knight)
        list8.add(largeHazard, largeHazard1)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==38:
        mage=class2(500, 200)
        knight=class3(600, 200)
        largeHazard=class6(200, 229)
        largeHazard1=class6(500, 229)
        list2.add(mage)
        list3.add(knight)
        list5.add(mage, knight)
        list8.add(largeHazard, largeHazard1)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==39:
        smallHazard=class5(100, 229)
        smallHazard1=class5(250, 229)
        smallHazard2=class5(400, 229)
        smallHazard3=class5(550, 229)
        smallHazard4=class5(700, 229)
        list8.add(smallHazard, smallHazard1, smallHazard2, smallHazard3, smallHazard4)
      elif self.worldLevel==40:
        self.spawnCooldown=1000
        boss=class4(700, 200, 300)
        list4.add(boss)
        list5.add(boss)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==41:
        knight=class3(600, 200)
        knight1=class3(500, 200)
        largeHazard=class6(100, 229)
        largeHazard1=class6(300, 229)
        largeHazard2=class6(500, 229)
        list3.add(knight, knight1)
        list5.add(knight, knight1)
        list8.add(largeHazard, largeHazard1, largeHazard2)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==42:
        knight=class3(600, 200)
        knight1=class3(500, 200)
        knight2=class3(400, 200)
        knight3=(class3(300, 200))
        largeHazard=class6(100, 229)
        largeHazard1=class6(300, 229)
        largeHazard2=class6(500, 229)
        list3.add(knight, knight1, knight2, knight3)
        list5.add(knight, knight1, knight2, knight3)
        list8.add(largeHazard, largeHazard1, largeHazard2)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==43:
        knight=class3(600, 200)
        knight1=class3(500, 200)
        mage=class2(400, 200)
        mage1=class2(300, 200)
        grunt=class1(200, 200)
        grunt1=class1(100, 200)
        largeHazard=class6(100, 229)
        largeHazard1=class6(300, 229)
        largeHazard2=class6(500, 229)
        list1.add(grunt, grunt1)
        list2.add(mage, mage1)
        list3.add(knight, knight1)
        list5.add(knight, knight1, grunt, grunt1, mage, mage1)
        list8.add(largeHazard, largeHazard1, largeHazard2)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==44:
        knight=class3(600, 200)
        knight1=class3(500, 200)
        knight2=class3(400, 200)
        mage=(class2(300, 200))
        largeHazard=class6(100, 229)
        largeHazard1=class6(300, 229)
        largeHazard2=class6(500, 229)
        list2.add(mage)
        list3.add(knight, knight1, knight2)
        list5.add(knight, knight1, knight2, mage)
        list8.add(largeHazard, largeHazard1, largeHazard2)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==45:
        boss=class4(700, 200, 150)
        knight=class3(600, 200)
        knight1=class3(500, 200)
        largeHazard=class6(100, 229)
        largeHazard1=class6(300, 229)
        largeHazard2=class6(500, 229)
        list3.add(knight, knight1)
        list4.add(boss)
        list5.add(knight, knight1, boss)
        list8.add(largeHazard, largeHazard1, largeHazard2)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==46:
        mage=class2(500, 200)
        boss=class4(500, 200, 150)
        largeHazard=class6(100, 229)
        largeHazard1=class6(300, 229)
        largeHazard2=class6(500, 229)
        list2.add(mage)
        list4.add(boss)
        list5.add(mage, boss)
        list8.add(largeHazard, largeHazard1, largeHazard2)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==47:
        boss=class4(600, 200, 150)
        mage=class2(500, 200)
        knight=class3(400, 200)
        knight1=class3(300, 200)
        grunt=class1(200, 200)
        grunt1=class1(100, 200)
        largeHazard=class6(100, 229)
        largeHazard1=class6(300, 229)
        largeHazard2=class6(500, 229)
        list1.add(grunt, grunt1)
        list2.add(mage)
        list3.add(knight, knight1)
        list4.add(boss)
        list5.add(grunt, grunt1, mage, knight, knight1, boss)
        list8.add(largeHazard, largeHazard1, largeHazard2)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==48:
        boss=class4(600, 200, 150)
        boss1=class4(500, 200, 150)
        boss2=class4(400, 200, 150)
        mage=class2(500, 200)
        largeHazard=class6(100, 229)
        largeHazard1=class6(300, 229)
        largeHazard2=class6(500, 229)
        list2.add(mage)
        list4.add(boss, boss1, boss2)
        list5.add(mage, boss, boss1, boss2)
        list8.add(largeHazard, largeHazard1, largeHazard2)
        for sprite in list5:
          sprite.getImages()
      elif self.worldLevel==50:
        boss=class4(700, 200, 400)
        largeHazard=class6(100, 229)
        largeHazard1=class6(300, 229)
        largeHazard2=class6(500, 229)
        list4.add(boss)
        list5.add(boss)
        list8.add(largeHazard, largeHazard1, largeHazard2)
        for sprite in list5:
          sprite.getImages()

  def update(self, list, class1, class2, class3, list1, list2, list3, list4):
    if self.worldLevel%10==0: #Makes the door locked if it is a boss level
      for sprite in list:
        if sprite.shop==False: 
          self.open=False
        else:
          self.open=True #Unlocks the door if the boss has been defeated
    
    if self.spawnCooldown==0 and self.worldLevel==10: #Spawning enemies during boss levels
      for sprite in list:
        if sprite.shop==False:
          grunt=class1(600, 200)
          list1.add(grunt)
          list4.add(grunt)
          for sprite in list4:
            sprite.getImages()
          self.spawnCooldown=1000
    
    if self.spawnCooldown==0 and self.worldLevel==20:
      for sprite in list:
        if sprite.shop==False:
          mage=class2(500, 200)
          list2.add(mage)
          list4.add(mage)
          for sprite in list4:
            sprite.getImages()
          self.spawnCooldown=1000
    
    if self.spawnCooldown==0 and self.worldLevel==30:
      for sprite in list:
        if sprite.shop==False:
          knight=class3(600, 200)
          list3.add(knight)
          list4.add(knight)
          for sprite in list4:
            sprite.getImages()
          self.spawnCooldown=1000
    
    if self.spawnCooldown==0 and self.worldLevel==40:
      for sprite in list:
        if sprite.shop==False:
          grunt=class1(500, 200)
          mage=class2(500, 200)
          list1.add(grunt)
          list2.add(mage)
          list4.add(grunt, mage)
          for sprite in list4:
            sprite.getImages()
          self.spawnCooldown=1000

    if self.spawnCooldown==0 and self.worldLevel==50:
      for sprite in list:
        if sprite.shop==False:
          grunt=class1(500, 200)
          mage=class2(500, 200)
          knight=class3(500, 200)
          list1.add(grunt)
          list2.add(mage)
          list3.add(knight)
          list4.add(grunt, mage, knight)
          for sprite in list4:
            sprite.getImages()
          self.spawnCooldown=1000
    
    if self.spawnCooldown>0 and self.worldLevel%10==0:
      self.spawnCooldown-=1 #Slowly decreasing the cooldown for spawning enemies

  def gameComplete(self): #Checking if the game has been completed
    gameFinished=False
    if self.worldLevel==51:
      gameFinished=True
    return gameFinished     