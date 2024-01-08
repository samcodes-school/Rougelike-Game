import pygame

class spriteSheet():
  def __init__ (self, image):
    self.sheet=image

  def get_image(self, frame, width, height, scale, colour):
    image=pygame.Surface((width, height)) #Creates a surface the image can be added to
    image.blit(self.sheet, (0, 0), ((frame*width), 0, width, height)) #Gets a new frame at frame*height, so it constantly moves along the spritesheet and grabs each image, since width is the width of the image
    image=pygame.transform.scale(image, (width*scale, height*scale)) #Changing the size of the image so it fits the screen well
    image.set_colorkey(colour) #And getting rid of the black background
    return image #Returns the image, so it is added to tempList in player.py, where it is then added to the master animation list