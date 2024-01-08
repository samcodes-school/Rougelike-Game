import pygame
import animation #The animation file is needed to animate the player
screen=pygame.display.set_mode((660, 500)) #A screen is needed to blit things onto
black=(0, 0, 0)

class Player(pygame.sprite.Sprite): #Making our player class
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self) #Necessary for the class to be a sprite

    #Keeping track of the position of the player
    self.x = x 
    self.y = y

    #Attributes needed for animation
    self.frames=pygame.image.load("Player.png") #Loading the player spritesheet
    self.images=animation.spriteSheet(self.frames) #Turns the spritesheet into one image
    self.animation_list=[] #The master animation list
    self.animation_steps=[3, 3, 4, 4, 4, 4, 1, 1, 8, 8] #The other animation lists, the length is based on the amount of frames per action, for example, the walking left and walking right animations are both 3 frames long
    self.action=0 #Dictates what the player is doing
    self.last_update=pygame.time.get_ticks() #Regulates the speed of animation of the player
    self.animation_cooldown=75 #The speed of animation
    self.frame=0 #The frame of the current action
    self.counter=0 #Used to add the images to self.animation_list

    #Attributes needed for collision
    self.surf = pygame.Surface((30, 30)) #Creating a surface
    self.rect = self.surf.get_rect() #Getting a rectangle from the surface, which can then be used to detect collision
    
    #Stats for moving
    self.vel = 5 #The speed of the player
    self.direction=1 #The direction of the player
    self.moving=False

    #Stats for player dashing
    self.dashCooldown=0
    self.maxDashCooldown=250
    self.dashDistance=100
    self.dashCost=10

    #Stats for combat
    self.attackCooldown=250
    self.maxAttackCooldown=250
    self.damage=10
    self.rangedDamage=10
    self.activeWeapon="Sword"
    self.melee=False
    self.ranged=False
    self.blocking=False
    self.invincibility=0
    self.attackCost=10
    self.powerAttack=0
    self.potionCooldown=0

    #Stats for jumping
    self.isJump = False
    self.jumpCount = 7

    #Health, Stamina and Magicka
    self.health=150
    self.maxHealth=150
    self.stamina=100
    self.maxStamina=100
    self.magicka=100
    self.maxMagicka=100
    
    #Stats for the super
    self.super=0
    self.maxSuper=250
    self.superDamage=25

    #Images and stats for the skill tree
    self.skillTree=False
    self.skillImage=pygame.image.load("Skills.png")
    self.skillImage=pygame.transform.scale(self.skillImage, (660, 455))
    self.TImage=pygame.image.load("SkillT.png")
    self.TImage=pygame.transform.scale(self.TImage, (24, 24))
    self.skillCooldown=0
    self.skillUpgradeCooldown=0
    self.skillPoints=0
    self.XP=0
    self.level=0

    #Shopping images and stats
    self.shopCooldown=0
    self.shopping=False
    self.shopImage=pygame.image.load("Shop.png")
    self.shopImage=pygame.transform.scale(self.shopImage, (660, 455))
    self.buyCooldown=0
    self.money=0

    #Keeping track of shop increases
    self.armour=0
    self.healthPotions=0
    self.staminaPotions=0
    self.magickaPotions=0
    self.shopDamageCount=0
    self.shopRangedCount=0

    #Keeping track of skill increases
    self.skillDamageCount=0
    self.skillRangedCount=0
    self.attackCostCount=0
    self.attackCooldownCount=0
    self.dashCount=0
    self.movementCount=0
    self.potionPotency=50
    self.potionCount=0
    self.superCount=0
    
    self.corrupted=False #Whether or not the player has died

    #Loading images for the active weapon and potions
    self.swordActiveImage=pygame.image.load("swordActive.png").convert_alpha()
    self.swordActiveImage=pygame.transform.scale(self.swordActiveImage, (60, 80))
    self.swordInactiveImage=pygame.image.load("swordInactive.png").convert_alpha()
    self.swordInactiveImage=pygame.transform.scale(self.swordInactiveImage, (60, 80))
    self.fireActiveImage=pygame.image.load("fireActive.png").convert_alpha()
    self.fireActiveImage=pygame.transform.scale(self.fireActiveImage, (60, 80))
    self.fireInactiveImage=pygame.image.load("fireInactive.png").convert_alpha()
    self.fireInactiveImage=pygame.transform.scale(self.fireInactiveImage, (60, 80))
    self.healthPotionImage=pygame.image.load("healthPotions.png").convert_alpha()
    self.healthPotionImage=pygame.transform.scale(self.healthPotionImage, (60, 80))
    self.staminaPotionImage=pygame.image.load("staminaPotions.png").convert_alpha()
    self.staminaPotionImage=pygame.transform.scale(self.staminaPotionImage, (60, 80))
    self.magickaPotionImage=pygame.image.load("magickaPotions.png").convert_alpha()
    self.magickaPotionImage=pygame.transform.scale(self.magickaPotionImage, (60, 80))
  
  #Getting all of the images from the spritesheet 
  def getImages(self):
    for i in self.animation_steps:
      tempList=[] #Creating a temporary list
      for _ in range(i):
        tempList.append(self.images.get_image(self.counter, 32, 32, 2, black)) #And adding each image in the spritesheet to it, with the proper formatting
        self.counter+=1 #Keeps moving through the spritesheet
      self.animation_list.append(tempList) #Adds the list to the master list, essentialy creating a 2D list, where each sublist is an action of the player

  def updateAnimation(self): 
    current_time=pygame.time.get_ticks() #Gets the time
    if current_time-self.last_update>=self.animation_cooldown: #Checks to see if enough time has gone by to update the animation
      self.frame+=1 
      self.last_update=current_time #Resetting self.last_update
      if self.frame>=len(self.animation_list[self.action]): #Checking whether or not the frame is greater than the length of the list, which would cause an index out of range error
        self.frame=0 #If so, it sends it back to the start of the list

    #Makes the player stop animating if they are not moving
    if self.action==0 and self.moving==False: 
      self.frame=0
    if self.action==1 and self.moving==False:
      self.frame=0

    #Stopping the attack animation from going on forever
    if self.action==2 or self.action==3:
      if self.frame==3:
        self.melee=False
        if self.action==2:
          self.frame=0
          self.action=0
        else:
          self.frame=0
          self.action=1

    #Stopping the ranged attack animation from going on forever
    if self.action==4 or self.action==5:
      if self.frame==3:
        self.ranged=False
        if self.action==4:
          self.frame=0
          self.action=0
        else:
          self.frame=0
          self.action=1

    #Resetting the block animation
    if self.action==6 or self.action==7:
      if self.blocking==False:
        if self.action==6:
          self.action=0
        else:
          self.action=1

    #Checking for player death after it has gone through the death animation
    if self.action==8 or self.action==9:
      if self.frame==7:
        self.corrupted=True

  def death(self): 
    endGame=False
    if self.corrupted==True:
      endGame=True
    return endGame #Breaks the running loop and goes to the game over screen

  #Animation
  def animate(self):
    keys=pygame.key.get_pressed()
    if keys[pygame.K_d] and self.health>0: #The health check prevents the player from spamming d and a to prevent their character from dying
      self.action=0 #Move right
      if self.frame>=len(self.animation_list[self.action]): #Prevents any index out of range error from switching between actions
        self.frame=0
    if keys[pygame.K_a] and self.health>0:
      self.action=1 #Move left
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0

    if self.melee==True and self.blocking==False and self.direction==1:
      self.action=2 #Attack right
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0
    if self.melee==True and self.blocking==False and self.direction==-1:
      self.action=3 #Attack left
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0

    if self.ranged==True and self.blocking==False and self.direction==1:
      self.action=4 #Ranged attack right
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0
    if self.ranged==True and self.blocking==False and self.direction==-1:
      self.action=5 #Ranged attack left
      if self.frame>=len(self.animation_list[self.action]):
        self.frame=0
    
    if self.blocking==True and self.melee==False and self.direction==1:
      self.action=6 #Block right
      self.frame=0 #There is only one frame for this action
    if self.blocking==True and self.melee==False and self.direction==-1:
      self.action=7 #Block left
      self.frame=0

    if self.health<=0 and self.direction==1:
      self.action=8 #Death animation facing right
      self.animation_cooldown=500 #Slows down the animation 
    if self.health<=0 and self.direction==-1:
      self.action=9 #Death animation facing left
      self.animation_cooldown=500

  #Moving left and right
  def keys(self):
    if self.health>0 and self.skillTree==False and self.shopping==False and self.powerAttack==0: #Preventing the player from moving while charging an attack
      keys=pygame.key.get_pressed()
      if keys[pygame.K_d] and self.x<640: #Check for boundaries
        self.x+=self.vel #Move right
        self.direction=1 #Update player direction
        self.moving=True
      elif keys[pygame.K_a] and self.x>5: #Check for boundaries
        self.x-=self.vel #Move left
        self.direction=-1
        self.moving=True
      else:
        self.moving=False

  #Dashing
  def dash(self, sprite):
    if self.health>0 and self.skillTree==False and self.shopping==False and self.powerAttack==0 and sprite.worldLevel>=3: #The player cannot dash before level three, where the prompt for dashing is displayed
      keys=pygame.key.get_pressed()
      if keys[pygame.K_s] and self.dashCooldown<=0 and self.magicka>self.dashCost: #Checking that the player has enough magicka to dash
        if self.x<self.dashDistance and self.direction==-1:
          self.x+=(self.x*self.direction) #Some math to determine boundaries for the left side of the screen
        elif self.x>(640-self.dashDistance) and self.direction==1:
          self.x+=((640-self.x)*self.direction) #Same thing here, just for the right
        else:
          self.x+=(self.dashDistance*self.direction)
        self.dashCooldown=self.maxDashCooldown #Setting a cooldown for dashing
        self.magicka-=self.dashCost #And using some of the player's magicka

  #Jumping
  def jump(self, sprite): 
    if self.health>0 and self.skillTree==False and self.shopping==False and self.powerAttack==0 and sprite.worldLevel>=2: #No jumping before level 2
      keys=pygame.key.get_pressed()
      if self.isJump==False and self.y==200: #The player can only jump if it is touching the ground, which prevents infinite jumping
        if keys[pygame.K_w]:
          self.isJump=True
      else:
        if self.jumpCount >= -7:
            self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5 #Simulates a parabola, where jumpCount are the x coordinates and self.y is the y coordinate, and the x intercepts are at -7 and 7 
            self.jumpCount -= 1
        else: 
            self.jumpCount = 7 #At jumpCount=7 the player is back on the ground
            self.isJump = False

  #Shopping
  def shop(self, sprite1, list):
    if self.health>0 and self.skillTree==False and sprite1.worldLevel%10==0: #The player can only shop on boss levels
      for sprite in list:
        if sprite.shop==True: #And only after the boss has been defeated
          keys=pygame.key.get_pressed()
          if keys[pygame.K_e] and self.shopCooldown==0: #shopCooldown prevents the shop menu from opening and closing instantaneously, since [e] is used to both open and close the shop
            if self.shopping==False:
              self.shopping=True #Opening the shop menu
              self.shopCooldown=10
            else:
              self.shopping=False #Closing the shop menu
              self.shopCooldown=10
          else:
            pass
          if self.shopping==True and self.buyCooldown==0:
            if keys[pygame.K_1] and self.money>50 and self.shopDamageCount<5: #Keeps track of how many upgrades you have in a category and caps it at 5, and checks that you have enough money to buy the upgrade
              self.damage+=2 #Upgrade sword damage
              self.buyCooldown=10 #Add a cooldown so it doesn't upgrade the sword multiple times at once
              self.money-=50 #Subtracts the amount of money necessary for the upgrade
              self.shopDamageCount+=1 #Increases the upgrade count by 1 for this category
            if keys[pygame.K_2] and self.money>50 and self.shopRangedCount<5:
              self.rangedDamage+=1 #Upgrade ranged damage
              self.buyCooldown=10
              self.money-=50
              self.shopRangedCount+=1
            if keys[pygame.K_3] and self.money>50 and self.armour<5:
              self.armour+=1 #Upgrade armour
              self.buyCooldown=10
              self.money-=50
            if keys[pygame.K_4] and self.money>25 and self.healthPotions<5:
              self.healthPotions+=1 #Add health potions
              self.buyCooldown=10
              self.money-=25
            if keys[pygame.K_5] and self.money>25 and self.staminaPotions<5:
              self.staminaPotions+=1 #Add stamina potions
              self.buyCooldown=10
              self.money-=25
            if keys[pygame.K_6] and self.money>25 and self.magickaPotions<5:
              self.magickaPotions+=1 #Add magicka potions
              self.buyCooldown=10
              self.money-=25

  #The skill tree
  def skills(self, sprite):
    if self.health>0 and self.shopping==False and sprite.worldLevel>=9: #The player can't open the skill menu until the prompt is displayed on the screen
      keys=pygame.key.get_pressed()
      if keys[pygame.K_t] and self.skillCooldown==0: #The same type of thing as the shopping code above
        if self.skillTree==False:
          self.skillCooldown=10
          self.skillTree=True
        else:
          self.skillCooldown=10
          self.skillTree=False
      else:
        pass
      if self.skillTree==True and self.skillUpgradeCooldown==0 and self.skillPoints>0:
        if keys[pygame.K_1] and self.skillDamageCount<5:
          self.damage+=2 #Upgrade sword damage
          self.skillUpgradeCooldown=10
          self.skillPoints-=1
          self.skillDamageCount+=1
        if keys[pygame.K_2] and self.skillRangedCount<5:
          self.rangedDamage+=1 #Upgrade ranged damage
          self.skillUpgradeCooldown=10
          self.skillPoints-=1
          self.skillRangedCount+=1
        if keys[pygame.K_3] and self.attackCostCount<5:
          self.attackCost-=1 #Upgrade attack cost
          self.skillUpgradeCooldown=10
          self.skillPoints-=1
          self.attackCostCount+=1
        if keys[pygame.K_4] and self.attackCooldownCount<5:
          self.maxAttackCooldown-=25 #Upgrade attack cooldown
          self.skillUpgradeCooldown=10
          self.skillPoints-=1
          self.attackCooldownCount+=1
        if keys[pygame.K_5] and self.dashCount<5:
          self.maxDashCooldown-=25 #Upgrade dashing in a few ways
          self.dashDistance+=20
          self.dashCost-=1
          self.skillUpgradeCooldown=10
          self.skillPoints-=1
          self.dashCount+=1
        if keys[pygame.K_6] and self.movementCount<5:
          self.vel+=1 #Upgrade the player's speed
          self.skillUpgradeCooldown=10
          self.skillPoints-=1
          self.movementCount+=1
        if keys[pygame.K_7] and self.potionCount<5:
          self.potionPotency+=20 #Upgrade the effectiveness of potions
          self.skillUpgradeCooldown=10
          self.skillPoints-=1
          self.potionCount+=1
        if keys[pygame.K_8] and self.superCount<5:
          self.maxSuper-=25 #Upgrade the super of the player
          self.superDamage+=25
          self.skillUpgradeCooldown=10
          self.skillPoints-=1
          self.superCount+=1
      if self.XP>=100 and self.level<10: #Check for level up, to a max of level 10
        self.level+=1 #The player gains a level
        self.skillPoints+=1 #A skill point (for the skill menu)
        self.maxHealth+=25 #And their health, stamina, and magicka are improved, as well as brought back to max
        self.health=self.maxHealth
        self.maxStamina+=25
        self.stamina=self.maxStamina
        self.maxMagicka+=25
        self.magicka=self.maxMagicka
        self.XP-=100 #Subtracts the necessary XP from the level up

  #Swapping weapons and using potions
  def weapons(self, sprite):
    if self.health>0 and self.skillTree==False and self.shopping==False and sprite.worldLevel>=4:
      keys=pygame.key.get_pressed()
      if keys[pygame.K_1]:
        self.activeWeapon="Sword" #Switches the active weapon to sword
      if keys[pygame.K_2]:
        self.activeWeapon="Bow" #Switches the active weapon to bow
      if keys[pygame.K_3] and self.healthPotions>0 and self.health<self.maxHealth and self.potionCooldown==0: #Using health potions
        if self.health+self.potionPotency>self.maxHealth:
          self.health+=(self.maxHealth-self.health) #Some math to not give the player more health than his max health
        else:
          self.health+=self.potionPotency
        self.healthPotions-=1 #Gets rid of the potion
        self.potionCooldown=10 #And adds a cooldown to prevent multiple potions from being used at once
      if keys[pygame.K_4] and self.staminaPotions>0 and self.stamina<self.maxStamina and self.potionCooldown==0: #Using stamina potions
        if self.stamina+self.potionPotency>self.maxStamina:
          self.stamina+=(self.maxStamina-self.stamina)
        else:
          self.stamina+=self.potionPotency
        self.staminaPotions-=1
        self.potionCooldown=10
      if keys[pygame.K_5] and self.magickaPotions>0 and self.magicka<self.maxMagicka and self.potionCooldown==0: #Using magicka potions
        if self.magicka+self.potionPotency>self.maxMagicka:
          self.magicka+=(self.maxMagicka-self.magicka)
        else:
          self.magicka+=self.potionPotency
        self.magickaPotions-=1
        self.potionCooldown=10

  #Attacking
  def attack(self, group, ranged, list, sprite):
    if self.health>0 and self.skillTree==False and self.shopping==False and self.y==200:
      left, middle, right=pygame.mouse.get_pressed()
      if left and self.attackCooldown<=0 and self.blocking==False and self.stamina>self.attackCost and sprite.worldLevel>=4: #No attacking before level 4
        if self.powerAttack<100:
          self.powerAttack+=10 #Pressing left mouse adds to the power attack bar above the player
      elif not left and self.powerAttack>0: 
        if self.activeWeapon=="Sword":
          if self.powerAttack<100: #Checks to see whether or not the attack is a power attack or a regular attack
            self.melee=True
            attackRect=pygame.Rect(self.x+(20*self.direction), self.y, 20, 30) #Creates a rectangle for collision with other sprites
            for sprite in group: 
              if attackRect.colliderect(sprite.rect): #If there is a collision
                sprite.health-=self.damage #The sprites take damage based on the sword damage of the player
                if self.super<self.maxSuper and (sprite.health+self.damage)>0:
                  self.super+=self.damage #And this charges the player's super
            self.attackCooldown=self.maxAttackCooldown #Sets a cooldown
            self.stamina-=self.attackCost #Uses some stamina
            self.powerAttack=0 #And resets power attack
          else:
            self.melee=True
            attackRect=pygame.Rect(self.x+(20*self.direction), self.y, 20, 30)
            for sprite in group: 
              if attackRect.colliderect(sprite.rect):
                sprite.health-=self.damage*2 #Does double damage since it is a power attack
                if self.super<self.maxSuper and (sprite.health+(self.damage*2))>0:
                  self.super+=self.damage*2 #And so charges the super twice as much
            self.attackCooldown=self.maxAttackCooldown
            self.stamina-=self.attackCost
            self.powerAttack=0
        elif self.activeWeapon=="Bow": #Pretty much the same thing
          if self.powerAttack<100:
            self.ranged=True
            arrow=ranged(self.x, self.y, self.direction, self.rangedDamage) #Except it creates a fireball instead
            list.add(arrow) #Which is added to the player fireball list
            self.attackCooldown=self.maxAttackCooldown
            self.stamina-=self.attackCost
            self.powerAttack=0
          else:
            self.ranged=True
            arrow=ranged(self.x, self.y, self.direction, self.rangedDamage*2) #Power attack so twice the damage
            list.add(arrow)
            self.attackCooldown=self.maxAttackCooldown
            self.stamina-=self.attackCost
            self.powerAttack=0
      elif right and self.magicka>1 and self.melee==False and self.ranged==False and sprite.worldLevel>=5: #Blocking is only possible after the prompt on level 5
        self.blocking=True
        self.magicka-=0.5 #Keeps using magicka as long as the player is blocking
      else:
        self.blocking=False

  def epicMove(self, list):
    if self.health>0 and self.skillTree==False and self.shopping==False:
      keys=pygame.key.get_pressed()
      if keys[pygame.K_q] and self.super==self.maxSuper: #Checks to see if it is charged completely
        for sprite in list: #Damages all enemies (uses enemyList, which contains all the enemies currently on the screen)
          sprite.health-=self.superDamage #Deals damage based on the relevant stat
        self.super=0 #And resets it

  #Drawing the player and all the relevant stats and prompts
  def draw(self, sprite): 
    font=pygame.font.SysFont("Comic Sans MS", 30) #Used for for the prompts

    if sprite.worldLevel==1:
      movement=font.render("Press A and D to move.", False, (255, 0, 0)) #Making text for the prompt on level 1
      screen.blit(movement, (0, 50)) #And drawing it to the screen

    elif sprite.worldLevel==2:
      jump=font.render("Press W to jump.", False, (255, 0, 0))
      screen.blit(jump, (0, 50))

    elif sprite.worldLevel==3:
      dash=font.render("Press S to dash in the direction you are moving.", False, (255, 0, 0))
      dash1=font.render("Dashing uses magic power.", False, (255, 0, 0))
      screen.blit(dash, (0, 50))
      screen.blit(dash1, (0, 75))

    elif sprite.worldLevel==4:
      attack=font.render("Press the Left Mouse button to attack. Attacking uses stamina.", False, (255, 0, 0))
      attack1=font.render("Hold the Left Mouse button to charge your attack.", False, (255, 0, 0))
      attack2=font.render("Use 1 - 5 to switch weapons and use potions.", False, (255, 0, 0))
      screen.blit(attack, (0, 50))
      screen.blit(attack1, (0, 75))
      screen.blit(attack2, (0, 100))

    elif sprite.worldLevel==5:
      block=font.render("Press the Right Mouse button to block.", False, (255, 0, 0))
      block1=font.render("Blocking uses magic power.", False, (255, 0, 0))
      super=font.render("Charge your super by damaging enemies with your sword.", False, (255, 0, 0))
      screen.blit(block, (0, 50))
      screen.blit(block1, (0, 75))
      screen.blit(super, (0, 100))

    elif sprite.worldLevel==6:
      grunt=font.render("Grunts are the weakest members of the Corrupted,", False, (255, 0, 0))
      grunt1=font.render("but can be dangerous in groups.", False, (255, 0, 0))
      screen.blit(grunt, (0, 50))
      screen.blit(grunt1, (0, 75))

    elif sprite.worldLevel==7:
      mage=font.render("Casters are the second weakest members of the Corrupted,", False, (255, 0, 0))
      mage1=font.render("but possess ranged abilities.", False, (255, 0, 0))
      screen.blit(mage, (0, 50))
      screen.blit(mage1, (0, 75))

    elif sprite.worldLevel==8:
      knight=font.render("Knights are one of the more powerful members of the Corrupted.", False, (255, 0, 0))
      knight1=font.render("Be careful when fighting them.", False, (255, 0, 0))
      screen.blit(knight, (0, 50))
      screen.blit(knight1, (0, 75))

    elif sprite.worldLevel==9:
      boss=font.render("Upgrade your gear by slaying enemies and bosses.", False, (255, 0, 0))
      boss1=font.render("Upgrade your skills in the same way.", False, (255, 0, 0))
      screen.blit(boss, (0, 50))
      screen.blit(boss1, (0, 75))

    elif sprite.worldLevel==11:
      goodLuck=font.render("That's all for now. Good luck.", False, (255, 0, 0))
      screen.blit(goodLuck, (0, 50))

    elif sprite.worldLevel==31:
      hazards=font.render("The Corruption is spreading. Avoid Corruption pools.", False, (255, 0, 0))
      hazards1=font.render("Corruption pools will not damage the Corrupted.", False, (255, 0, 0))
      screen.blit(hazards, (0, 50))
      screen.blit(hazards1, (0, 75))

    #Drawing the player, at its current animation state
    screen.blit(self.animation_list[self.action][self.frame], (self.x-16, self.y-14)) #The x-16 and y-14 are used to reposition the player so its hitbox makes sense. A better way to do it would've been to use .convert_alpha() on the player spritesheet, but I didn't find out about that until much later

    if sprite.worldLevel>=6: #The health bar of the player
      pygame.draw.rect(screen, ((128, 0, 0)), pygame.Rect(300, 300, 100, 10))
      pygame.draw.rect(screen, ((255, 0, 0)), pygame.Rect(300, 300, 100*(self.health/self.maxHealth), 10))
      health=font.render("Health", False, (255, 0, 0))
      screen.blit(health, (315, 275))

    if sprite.worldLevel>=4: #Stamina bar
      pygame.draw.rect(screen, ((0, 128, 0)), pygame.Rect(150, 300, 100, 10))
      pygame.draw.rect(screen, ((0, 255, 0)), pygame.Rect(150, 300, 100*(self.stamina/self.maxStamina), 10))
      stamina=font.render("Stamina", False, (0, 255, 0))
      screen.blit(stamina, (158, 275))
    
    if sprite.worldLevel>=3: #Magicka bar
      pygame.draw.rect(screen, ((0, 0, 128)), pygame.Rect(450, 300, 100, 10))
      pygame.draw.rect(screen, ((0, 0, 255)), pygame.Rect(450, 300, 100*(self.magicka/self.maxMagicka), 10))
      magicka=font.render("Magic", False, (0, 0, 255))
      screen.blit(magicka, (470, 275))

    if sprite.worldLevel>=5: #Bar for the super
      pygame.draw.rect(screen, ((128, 128, 0)), pygame.Rect(150, 350, 100, 10))
      pygame.draw.rect(screen, ((255, 255, 0)), pygame.Rect(150, 350, 100*(self.super/self.maxSuper), 10))
      if self.super==self.maxSuper: #Only displays [Q] when the super is charged, which makes it easier for the user to know when to use the super
        superKey=font.render("[Q]", False, (255, 255, 0))
        screen.blit(superKey, (115, 340))

    if sprite.worldLevel>=9: #The XP bar
      pygame.draw.rect(screen, ((128, 0, 128)), pygame.Rect(300, 350, 100, 10))
      pygame.draw.rect(screen, ((255, 0, 255)), pygame.Rect(300, 350, self.XP, 10))
      if self.skillPoints>0: #Only displays [T] when the user has unspent skill points, which makes it easier for the user to know when they've leveled up
        levelKey=font.render("[T]", False, (255, 0, 255))
        screen.blit(levelKey, (265, 340))

    if sprite.worldLevel>=6: #The money the player currently has
      money=str(self.money)
      moneyAmount=font.render(money, False, (255, 255, 0))
      moneyWord=font.render("Coins:", False, (255, 255, 0))
      screen.blit(moneyAmount, (520, 345))
      screen.blit(moneyWord, (450, 345))
  
    pygame.draw.rect(screen, ((255, 0, 0)), pygame.Rect(self.x, self.y-15, 30*(self.powerAttack/100), 10)) #The charge of the attack if there is any

    if sprite.worldLevel>=4: #Displaying the active weapon and potion icons
      if self.activeWeapon=="Sword": #Displays sword as the active weapon
        screen.blit(self.swordActiveImage, (50, 375))
        screen.blit(self.fireInactiveImage, (175, 375))
        screen.blit(self.healthPotionImage, (300, 375))
        healthPotions=str(self.healthPotions) #To display text the text has to be a string, so it is important to convert the stat for whatever is going to be displayed to a string before using font.render
        healthPotionsNum=font.render(healthPotions, False, (255, 0, 0))
        screen.blit(healthPotionsNum, (360, 390))
        screen.blit(self.staminaPotionImage, (425, 375))
        staminaPotions=str(self.staminaPotions)
        staminaPotionsNum=font.render(staminaPotions, False, (255, 0, 0))
        screen.blit(staminaPotionsNum, (485, 390))
        screen.blit(self.magickaPotionImage, (550, 375))
        magickaPotions=str(self.magickaPotions)
        magickaPotionsNum=font.render(magickaPotions, False, (255, 0, 0))
        screen.blit(magickaPotionsNum, (610, 390))
      else: #Displays fireball as the active weapon
        screen.blit(self.swordInactiveImage, (50, 375))
        screen.blit(self.fireActiveImage, (175, 375))
        screen.blit(self.healthPotionImage, (300, 375))
        healthPotions=str(self.healthPotions)
        healthPotionsNum=font.render(healthPotions, False, (255, 0, 0))
        screen.blit(healthPotionsNum, (360, 390))
        screen.blit(self.staminaPotionImage, (425, 375))
        staminaPotions=str(self.staminaPotions)
        staminaPotionsNum=font.render(staminaPotions, False, (255, 0, 0))
        screen.blit(staminaPotionsNum, (485, 390))
        screen.blit(self.magickaPotionImage, (550, 375))
        magickaPotions=str(self.magickaPotions)
        magickaPotionsNum=font.render(magickaPotions, False, (255, 0, 0))
        screen.blit(magickaPotionsNum, (610, 390))

    if self.skillTree==True and self.health>0: #Displaying the skill menu
      screen.blit(self.skillImage, (0, 0))
      screen.blit(self.TImage, (457, 418)) #Fixing a mistake I made when creating the skill menu - I put press E to close instead of press T to close 
      skillPoints=str(self.skillPoints) 
      skillPointText1=font.render("You have", False, (255, 0, 0))
      if self.skillPoints!=1: #It's important to have good grammar 
        skillPointText2=font.render("unspent skill points.", False, (255, 0, 0))
      else:
        skillPointText2=font.render("unspent skill point.", False, (255, 0, 0))
      skillPointNum=font.render(skillPoints, False, (255, 0, 0))
      screen.blit(skillPointText1, (0, 420))
      screen.blit(skillPointNum, (95, 420))
      screen.blit(skillPointText2, (115, 420))
      
      attackPoints=str(self.skillDamageCount) #Showing how many upgrades the player has put into each skill
      attackPointsNum=font.render(attackPoints, False, (255, 0, 0))
      screen.blit(attackPointsNum, (100, 150))
      
      rangedPoints=str(self.skillRangedCount)
      rangedPointsNum=font.render(rangedPoints, False, (255, 0, 0))
      screen.blit(rangedPointsNum, (280, 150))
      
      costPoints=str(self.attackCostCount)
      costPointsNum=font.render(costPoints, False, (255, 0, 0))
      screen.blit(costPointsNum, (465, 150))
      
      cooldownPoints=str(self.attackCooldownCount)
      cooldownPointsNum=font.render(cooldownPoints, False, (255, 0, 0))
      screen.blit(cooldownPointsNum, (630, 150))
      
      dashPoints=str(self.dashCount)
      dashPointsNum=font.render(dashPoints, False, (255, 0, 0))
      screen.blit(dashPointsNum, (100, 290))
      
      movementPoints=str(self.movementCount)
      movementPointsNum=font.render(movementPoints, False, (255, 0, 0))
      screen.blit(movementPointsNum, (285, 290))
      
      potionPoints=str(self.potionCount)
      potionPointsNum=font.render(potionPoints, False, (255, 0, 0))
      screen.blit(potionPointsNum, (470, 290))
      
      superPoints=str(self.superCount)
      superPointsNum=font.render(superPoints, False, (255, 0, 0))
      screen.blit(superPointsNum, (640, 290))

    if self.shopping==True and self.health>0: #Pretty much the same code as the skill menu above
      screen.blit(self.shopImage, (0, 0))
      money=str(self.money)
      moneyAmount=font.render(money, False, (255, 0, 0))
      moneyWord=font.render("Coins:", False, (255, 0, 0))
      screen.blit(moneyAmount, (170, 420))
      screen.blit(moneyWord, (100, 420))

      shopAttack=str(self.shopDamageCount)
      shopAttackNum=font.render(shopAttack, False, (255, 0, 0))
      screen.blit(shopAttackNum, (170, 150))
      
      shopRanged=str(self.shopRangedCount)
      shopRangedNum=font.render(shopRanged, False, (255, 0, 0))
      screen.blit(shopRangedNum, (355, 150))
      
      shopArmour=str(self.armour)
      shopArmourNum=font.render(shopArmour, False, (255, 0, 0))
      screen.blit(shopArmourNum, (540, 150))

      healthPotions=str(self.healthPotions)
      healthPotionsNum=font.render(healthPotions, False, (255, 0, 0))
      screen.blit(healthPotionsNum, (170, 290))
      
      staminaPotions=str(self.staminaPotions)
      staminaPotionsNum=font.render(staminaPotions, False, (255, 0, 0))
      screen.blit(staminaPotionsNum, (355, 290))
  
      magickaPotions=str(self.magickaPotions)
      magickaPotionsNum=font.render(magickaPotions, False, (255, 0, 0))
      screen.blit(magickaPotionsNum, (540, 290))
      
  def update(self, list1, list2, list3, list4, list5, list6, list7, list8): #Updates the cooldowns for everything
    if self.health>0:
      if self.dashCooldown>0: #Dash cooldown
        self.dashCooldown-=10
      if self.attackCooldown>0: #Attack cooldown
        self.attackCooldown-=10
      if self.invincibility>0: #Inivincibility from enemy attacks
        self.invincibility-=10
      self.rect.x=self.x #Updates the player's hitbox position
      self.rect.y=self.y
      if self.health<self.maxHealth/2: #Slow health regen up to 50% of max health
        self.health+=0.05
      if self.stamina<self.maxStamina: #Stamina regeneration
        self.stamina+=0.1
      if self.magicka<self.maxMagicka: #Magicka regeneration
        self.magicka+=0.1
      if self.super>self.maxSuper: #Keeps the super at no more than max capacity
        self.super=self.maxSuper
      if self.skillCooldown>0: #Skill menu cooldown
        self.skillCooldown-=1
      if self.skillUpgradeCooldown>0: #Skill upgrade cooldown
        self.skillUpgradeCooldown-=1
      if self.shopCooldown>0: #Shop menu cooldown
        self.shopCooldown-=1
      if self.buyCooldown>0: #Shop upgrade cooldown
        self.buyCooldown-=1
      if self.potionCooldown>0: #Potion usage cooldown
        self.potionCooldown-=1
    else: #Deletes all other sprites when the player dies
      pygame.sprite.Group.empty(list1)
      pygame.sprite.Group.empty(list2)
      pygame.sprite.Group.empty(list3)
      pygame.sprite.Group.empty(list4)
      pygame.sprite.Group.empty(list5)
      pygame.sprite.Group.empty(list6)
      pygame.sprite.Group.empty(list7)
      pygame.sprite.Group.empty(list8)
      self.blocking=False #Stops the player from doing any other action than the death animation
      self.moving=False
      self.melee=False
      self.ranged=False