#Rouge - A Rougelike Game

#Bugs: 
#While charging a power attack, the player can change which direction it is facing, but the attack will be targeted at the direction it was facing originally.
#Charging a power attack and then attempting to block will stop the player from being able to move. The player can move again after attacking or blocking. 

#Rouge - A Rougelike Game lets the user attempt to save Rougeland from a corruption that has infected its inhabitants. Run, jump and dash through the 50 levels while slaying enemies using your sword and fireballs. Upgrade your character through a skill and shop system, but be careful - one death will send you back to the start. 

#Most of the comments are located in main.py, player.py, levels.py, boss.py and enemyArrow.py, as most of the other .py files use the same code as one of the files mentioned above (i.e. the enemies use pretty much the same code)

import pygame

from button import button, startGame #Needed to create buttons

#Setup
pygame.init()
screen = pygame.display.set_mode((660, 500)) #Creating the screen
pygame.display.set_caption("Rouge") #And the title of the game
clock=pygame.time.Clock() #For FPS
font=pygame.font.SysFont("Comic Sans MS", 30) #Used to draw text on the screen

#Importing all of the images for the various menus and buttons
startRed=pygame.image.load("startRed.png")
startPurple=pygame.image.load("startPurple.png")

quitRed=pygame.image.load("quitRed.png")
quitPurple=pygame.image.load("quitPurple.png")

menuRed=pygame.image.load("menuRed.png")
menuPurple=pygame.image.load("menuPurple.png")

menu=pygame.image.load("Menu.png")
menu=pygame.transform.scale(menu, (660, 455)) #Resizing the images to fit the screen

story=pygame.image.load("Story.png")
story=pygame.transform.scale(story, (660, 455))

deathScreen=pygame.image.load("deathScreen.png")
deathScreen=pygame.transform.scale(deathScreen, (660, 455))

complete=pygame.image.load("Complete.png")
complete=pygame.transform.scale(complete, (660, 455))

#Creating the three buttons needed for the game
startButton=button(240, 225, startRed, startPurple) #The start button
quitButton=button(240, 325, quitRed, quitPurple) #The quit button
menuButton=button(240, 325, menuRed, menuPurple) #And the main menu button

#Creating the big game loop, necessary to let the user go back to the main menu after dying or completing the game
gaming=True
while gaming:
  
  mainMenu=True #Creating the main menu loop
  while mainMenu:
    for event in pygame.event.get(): #Necessary so the program stops if the user closes the tab
      if event.type==pygame.quit:
        pygame.quit()
    
    screen.fill((0, 0, 0)) #Filling the background
  
    screen.blit(menu, (0, 0)) #Drawing the main menu screen
    
    if startButton.draw(): #Using the start button
      mainMenu=False
  
    if quitButton.draw(): #Using the quit button
      pygame.quit()
    
    pygame.display.update() #Updating the display
    clock.tick(40) #Regulating the FPS to 40
  
  premise=True 
  while premise: #Creating the loop for the premise of the game
    for event in pygame.event.get():
      if event.type==pygame.quit:
        pygame.quit()
  
    screen.fill((0, 0, 0))
  
    screen.blit(story, (0, 0)) #Drawing the premise/backstory screen
  
    if startGame(): #Checking whether or not the space bar has been pressed
      premise=False
  
    pygame.display.update()
    clock.tick(40)

  #Getting all of the necessary classes for the main game 
  from player import Player
  from arrow import Arrow
  from basicEnemy import basicEnemy
  from archer import archerEnemy
  from enemyArrow import enemyArrow
  from knight import Knight
  from boss import Boss
  from hazards import smallHazard, largeHazard
  from levels import door

  #And creating lists for them to be able to access them easier
  enemyList=pygame.sprite.Group()
  arrowList=pygame.sprite.Group()
  enemyArrowList=pygame.sprite.Group()
  archerList=pygame.sprite.Group()
  playerGroup=pygame.sprite.Group()
  basicEnemyList=pygame.sprite.Group()
  knightList=pygame.sprite.Group()
  bossList=pygame.sprite.Group()
  hazardList=pygame.sprite.Group()

  ending=0 #Necessary for ensuring which ending is displayed (either the death screen or the game complete screen)
  
  player=Player(10, 200) #Instantiating the player
  playerGroup.add(player) #And adding it to a list for use later
  
  nextLevel=door(620, 198) #Instantiating the door to the next level, which also creates the enemies
  
  player.getImages() #For animation - this just gets all the images from the spritesheet for the player ("Player.png")
  
  running = True
  while running: #The actual game loop
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Calling all of the player methods (movement, attacking, etc.)
    player.keys() 
    player.dash(nextLevel)
    player.jump(nextLevel)
    player.weapons(nextLevel)
    player.attack(enemyList, Arrow, arrowList, nextLevel)
    player.epicMove(enemyList)
    player.skills(nextLevel)
    player.shop(nextLevel, bossList)
    player.animate()
    if player.death():
      ending=-1 #Sets the ending to the death screen
      running=False #Breaks the loop upon player death
    
    for sprite in enemyList: #Enemy movement
      sprite.movement(player)
    for sprite in arrowList: #Player arrow (fireball) movement
      sprite.movement(enemyList)
    for sprite in enemyArrowList: #Enemy arrow (fireball) movement
      sprite.movement(playerGroup)
    
    for sprite in basicEnemyList: #Basic enemy attacks
      sprite.attack(playerGroup)
    for sprite in knightList: #Knight Attacks
      sprite.attack(playerGroup)
    for sprite in archerList: #Enemy archer attacks
      sprite.attack(enemyArrow, enemyArrowList)
    for sprite in bossList: #Boss Attacks
      sprite.attack(enemyArrow, enemyArrowList, playerGroup)

    for sprite in hazardList: #Checking for collisions with hazards
      sprite.collision(player)
  
    for sprite in enemyList: #Enemy Animations
      sprite.animate()
      
    screen.fill((0,0,0))
    pygame.draw.rect(screen, ((70, 70, 70)), pygame.Rect(0, 228, 660, 271)) #Drawing the ground
    
    for sprite in enemyList: #Displaying the enemies
      sprite.draw()
    for sprite in arrowList: #Displaying player arrows (fireballs)
      sprite.draw()
    for sprite in enemyArrowList: #Displaying enemy arrows (fireballs)
      sprite.draw()

    for sprite in hazardList: #Displaying any hazards
      sprite.draw()
    
    nextLevel.draw() #Displaying the door to the next level

    player.draw(nextLevel) #Displaying the player - The player is drawn last so the skill and shop menus are drawn over anything else
  
    player.update(enemyList, arrowList, enemyArrowList, archerList, basicEnemyList, knightList, bossList, hazardList) #Updating the player (the lists are used on player death)
    player.updateAnimation() #Updating the image of the player

    #Update the image for each type of enemy (these have to be done separately since the boss class takes two parameters for its updateAnimation method)
    for sprite in basicEnemyList: 
      sprite.updateAnimation(player)
    for sprite in knightList:
      sprite.updateAnimation(player)
    for sprite in archerList:
      sprite.updateAnimation(player)
    for sprite in bossList:
      sprite.updateAnimation(player, nextLevel)
      
    #Generate the next level
    nextLevel.newLevel(player, basicEnemyList, archerList, knightList, bossList, enemyList, arrowList, enemyArrowList, hazardList, basicEnemy, archerEnemy, Knight, Boss, smallHazard, largeHazard)
    
    #Update the level if necessary (i.e. during boss fights)
    nextLevel.update(bossList, basicEnemy, archerEnemy, Knight, basicEnemyList, archerList, knightList, enemyList)

    if nextLevel.gameComplete(): #Checking if the player finished the game
      ending=1 #Sets the ending to the game complete screen
      running=False #And breaks the loop
      
    pygame.display.update()
    clock.tick(40)
  
  gameOver=True
  while gameOver: #The loop for once the player dies or completes the game
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
  
    screen.fill((0, 0, 0))

    if ending==-1: #The bad ending
      screen.blit(deathScreen, (0, 0)) #Drawing death screen
      level=str(nextLevel.worldLevel)
      levelFailed=font.render(level, False, (255, 0, 255))
      levelFailedText=font.render("You were Corrupted at level", False, (255, 0, 255)) #Making some text - the boolean argument is for whether or not text is antialised, which makes it smoother, but slows the game down
      levelFailedText1=font.render("of 50.", False, (255, 0, 255))
      screen.blit(levelFailedText, (200, 225)) #Drawing the text
      screen.blit(levelFailed, (280, 250))
      screen.blit(levelFailedText1, (308, 250))
      
    elif ending==1: #The good ending
      screen.blit(complete, (0, 0)) #Drawing the game complete screen
      goodJobText=font.render("You have destroyed the Corruption.", False, (255, 0, 0)) #Making some text
      goodJobText1=font.render("Congratulations!", False, (255, 0, 0))
      screen.blit(goodJobText, (170, 250)) #Drawing the text
      screen.blit(goodJobText1, (245, 275)) 
    else:
      pass

    if ending==-1 or ending==1: #Creating the button to go back to the menu
      if menuButton.draw():
        gameOver=False
  
    pygame.display.update()
    clock.tick(40)
  
  delay=True
  while delay: #Creating a loop that waits until the left mouse button has been lifted
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        pygame.quit()
      if event.type==pygame.MOUSEBUTTONUP: #This loop is necessary since the main menu button and the quit button overlap, and so this prevents the game from automatically quitting after the main menu button is pressed
        mouse=pygame.mouse.get_pressed()
        if mouse[0]==False: #Checking that the left mouse button is no longer being pressed
          delay=False