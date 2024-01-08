import pygame
screen=pygame.display.set_mode((660, 500))

class button(pygame.sprite.Sprite):
  def __init__(self, x, y, image, image1):
    pygame.sprite.Sprite.__init__(self)
    self.image=pygame.transform.scale(image, (180, 75))
    self.image1=pygame.transform.scale(image1, (180, 75))
    self.rect=self.image.get_rect()
    self.rect.x=x
    self.rect.y=y
    self.clicked=False

  def draw(self):
    action=False
    pos=pygame.mouse.get_pos() #Gets the position of the mouse
    if self.rect.collidepoint(pos): #Checks if the mouse is touching the button
      if pygame.mouse.get_pressed()[0]==1 and self.clicked==False: #Checks if the button is pressed
        self.clicked=True
        action=True 

    if pygame.mouse.get_pressed()[0]==0:
      self.clicked=False

    if self.rect.collidepoint(pos): #Changes the image of the button based on whether or not the mouse is touching it
      screen.blit(self.image1, (self.rect.x, self.rect.y))
    else:
      screen.blit(self.image, (self.rect.x, self.rect.y))

    return action #Returns True if the button was pressed, which breaks the loop in main.py

def startGame(): #Checks if the space key was pressed while the story screen is open
  begin=False
  keys=pygame.key.get_pressed()
  if keys[pygame.K_SPACE]:
    begin=True
  return begin #Breaks the loop if the space key was pressed
    

    