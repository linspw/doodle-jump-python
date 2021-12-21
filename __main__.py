import OpenGL.GL as Gl
import OpenGL.GLU as Glu
import OpenGL.GLUT as Glut
import sys
import random

class Character:
  def __init__(self, positionX = 0, positionY = 0):
    self.positionX = positionX
    self.positionY = positionY
    self.sizeX = 35.0
    self.sizeY = 50.0
  
  def render(self):
    Gl.glBegin(Gl.GL_POLYGON)
    Gl.glColor3f(0.0, 255.0, 0.0)
    Gl.glVertex2f(self.positionX, self.positionY)
    Gl.glVertex2f(self.positionX, self.positionY + self.sizeY)
    Gl.glVertex2f(self.positionX + self.sizeX, self.positionY + self.sizeY)
    Gl.glVertex2f(self.positionX + self.sizeX, self.positionY)
    Gl.glEnd()

  def move_left(self, screenWidthSize, pixels = 10):
    self.positionX = self.positionX - pixels
    if (self.positionX < 0 ):
      self.positionX = 0
  
  def move_right(self, screenWidthSize, pixels = 10):
    self.positionX = self.positionX + pixels
    if ((self.positionX + self.sizeX) > screenWidthSize):
      self.positionX = screenWidthSize - self.sizeX

class Blocks:
  def __init__(self):
    self.items = [[400, 100]]
    self.sizeX = 50.0
    self.sizeY = 10
    self.maxOfBlocks = 10

  def render(self):
    for block in self.items:
      Gl.glBegin(Gl.GL_POLYGON)
      Gl.glColor3f(255.0, 0.0, 0.0)
      positionX = block[0]
      positionY = block[1]
      Gl.glVertex2f(positionX, positionY)
      Gl.glVertex2f(positionX, positionY + self.sizeY)
      Gl.glVertex2f(positionX + self.sizeX, positionY + self.sizeY)
      Gl.glVertex2f(positionX + self.sizeX, positionY)
      Gl.glEnd()

  def count_of_blocks(self):
    return len(self.items)

  def remove_block(self, index = 0):
    self.items.pop(index)

  def add_new_block(self, viewWidth, jumpSize, safeAreaX = 300, safeAreaY = 100):
    # print(viewWidth, jumpSize, safeArea)
    lastBlock = self.items[-1]
    lastBlockX = lastBlock[0]
    lastBlockY = lastBlock[1]
    if((lastBlockX + safeAreaX) >= viewWidth):
      diffX = -random.randint(0, safeAreaX)
    else:
      diffX = random.randint(0, safeAreaX)

    newBlockX = lastBlockX + diffX
    newBlockY = random.randint(int(lastBlockY + self.sizeY), int(lastBlockY + jumpSize - safeAreaY))
    self.items.append([newBlockX, newBlockY])

  def check_if_collide(self, positionX, positionY, sizeX, sizeY):
    for block in self.items:
      blockPositionX = block[0]
      blockPositionY = block[1]
      blockSizeX = self.sizeX
      blockSizeY = self.sizeY

      blockIntervalX = [blockPositionX, blockPositionX + blockSizeX]
      blockIntervalY = [blockPositionY, blockPositionY + blockSizeY]

      if(
        (positionX >= blockIntervalX[0] and positionX <= blockIntervalX[1]) 
        and
        (positionY >= blockIntervalY[0] and positionY <= blockIntervalY[1])    
      ):
        return True
      elif(
        (positionX + sizeX >= blockIntervalX[0] and positionX + sizeX <= blockIntervalX[1]) 
        and
        (positionY >= blockIntervalY[0] and positionY <= blockIntervalY[1])    
      ):
        return True
    return False

  def climb(self, pixels):
    itemsUpdated = []
    for block in self.items:
      blockPositionX = block[0]
      blockPositionY = block[1]
      itemsUpdated.append([blockPositionX, blockPositionY - pixels])
    self.items = itemsUpdated

class Utils:
  def render_text(self, positionX, positionY, font, text, centered = False):
    Gl.glColor3i(255, 255, 255)
    len = 0
    for character in text:
      len += Glut.glutBitmapWidth(font, ord(character))
    if(centered):
      Gl.glRasterPos2f(positionX - len/2, positionY)
    else:
      Gl.glRasterPos2f(positionX, positionY)
    for character in text:
      Glut.glutBitmapCharacter(font, ord(character))
class Game:
  def __init__(self):
    self.windowPositionX = 50
    self.windowPositionY = 10
    self.viewWidth = 800
    self.viewHeight = 800
    self.utils = Utils()
    self.gravityPixelJump = 0.25
    self.jumpSizeDefault = 350
    self.walkPixelDefault = 10
    self.walkToLeft = 0
    self.walkToRight = 0
    self.climbHeight = self.viewHeight/2
    self.characterMaxHeight = 0
    self.gameStatus = "to_start"

  def initialize(self):
    self.jumpPixelCount = 0
    self.jumping = self.jumpPixelCount > 0
    self.character = Character(400 - 25, 200 - 25)
    self.blocks = Blocks()
    self.score = 0.0

  def display(self):
    Gl.glClear(Gl.GL_COLOR_BUFFER_BIT)
    if(self.gameStatus == "to_start"):
      text = str("Use Menu to Start")
      self.utils.render_text(self.viewWidth/2, self.viewHeight/2, Glut.GLUT_BITMAP_HELVETICA_18, text, True)

    if(self.gameStatus == "started" or self.gameStatus == "paused"):
      text = str('%.2f' % self.score)
      self.character.render()
      self.blocks.render()
      self.utils.render_text(20, self.viewHeight - 40, Glut.GLUT_BITMAP_HELVETICA_18, text)

    if(self.gameStatus == "loose"):
      text = str('You loose! - %.2f meters' % self.score)
      self.utils.render_text(self.viewWidth/2, self.viewHeight/2, Glut.GLUT_BITMAP_HELVETICA_18, text, True)

    Gl.glFlush()
 
  def setup_window(self):
    Glut.glutInit(sys.argv)
    Glut.glutInitDisplayMode(Glut.GLUT_SINGLE | Glut.GLUT_RGB)
    Glut.glutInitWindowSize(self.viewWidth, self.viewHeight)
    Glut.glutInitWindowPosition(self.windowPositionX, self.windowPositionY)
    Glut.glutCreateWindow(b"Doodle Jump")
    Glut.glutReshapeFunc(self.screen_resize)
    Glut.glutSpecialFunc(self.character_commands)
    Glut.glutIdleFunc(self.character_gravity)
  
  def setup_screen(self):
    Gl.glClearColor(239.0, 232.0, 226.0, 1.0) # Color white

  def setup_display(self):
    Glut.glutDisplayFunc(self.display)

  def screen_resize(self, w, h):
    # Especifica as dimensões da Viewport
    Gl.glViewport(0, 0, w, h)
    self.viewWidth = w
    self.viewHeight = h
    # Inicializa o sistema de coordenadas
    Gl.glMatrixMode(Gl.GL_PROJECTION)
    Gl.glLoadIdentity()
    Glu.gluOrtho2D (0, self.viewWidth, 0, self.viewHeight)
  
  def setup_menu(self):
    Glut.glutCreateMenu(self.process_menu_events)  
    Glut.glutAddMenuEntry("Start", 0)  
    Glut.glutAddMenuEntry("Pause", 1)
    Glut.glutAddMenuEntry("Exit", 2)
    Glut.glutAttachMenu(Glut.GLUT_RIGHT_BUTTON)

  def process_menu_events(self, option):
    if(option == 0):
      self.initialize()
      self.gameStatus = "started"
    elif(option == 1):
      if not(self.gameStatus == "paused"):
        self.gameStatus = "paused"
      else:
        self.gameStatus = "started"
    elif(option == 2):
      Glut.glutLeaveMainLoop()
    
    return 0
  
  def character_commands(self, key, x, y):
    if(key == Glut.GLUT_KEY_LEFT):
      self.walkToLeft += 1
           
    if(key == Glut.GLUT_KEY_RIGHT):
      self.walkToRight += 1

    Glut.glutPostRedisplay()

  def character_gravity(self):
    if not(self.gameStatus == "started"):
      return

    if(self.jumpPixelCount > 0):
      self.jumpPixelCount -= 1
      if not(self.character.positionY >= self.climbHeight):
        self.character.positionY += self.gravityPixelJump
      else:
        self.score += self.gravityPixelJump
      self.jumping = True

    else:
      self.character.positionY += -self.gravityPixelJump
      self.jumping = False

    if(self.walkToLeft > 0):
      self.walkToLeft -= 1
      self.character.move_left(self.viewWidth, self.walkPixelDefault)

    if(self.walkToRight > 0):
      self.walkToRight -= 1
      self.character.move_right(self.viewWidth, self.walkPixelDefault)

    hasCollided = self.blocks.check_if_collide(self.character.positionX, self.character.positionY, self.character.sizeX, self.character.sizeY)
    if(hasCollided and not self.jumping):
      # print(self.jumpPixelCount)
      self.jumpPixelCount += self.jumpSizeDefault/self.gravityPixelJump

    if(self.character.positionY >= self.climbHeight):
      self.blocks.climb(self.gravityPixelJump)
      if(self.is_inside_vertical_screen(self.blocks.items[-1][1])):
        self.blocks.add_new_block(self.viewHeight, self.jumpSizeDefault)
      if not(self.is_inside_vertical_screen(self.blocks.items[0][1])):
        self.blocks.remove_block(0)
      

    if not(self.is_inside_vertical_screen(self.character.positionY)):
      self.gameStatus = "loose"

    Glut.glutPostRedisplay()

  def is_inside_vertical_screen(self, positionY):
    if(positionY > 0 and positionY < self.viewHeight):
      return True
    else:
      return False


  def render(self):
    self.setup_window()
    self.setup_screen()
    self.setup_menu()
    self.setup_display()
    Glut.glutMainLoop()

def main():
  app = Game()

  app.render()

main()
