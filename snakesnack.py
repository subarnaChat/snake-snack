#importing pygame module,random function,sys
import random, pygame, sys
#the following line is optional since we have already imported the pygame module.
from pygame.locals import*
FPS=5
#specifying the size of screen
WINDOWWIDTH=1000
WINDOWHEIGHT=600
CELLSIZE=20
assert WINDOWWIDTH % CELLSIZE==0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT%CELLSIZE==0, "Window height must be a multiple of cell size."
#specifying cell size
CELLWIDTH=int(WINDOWWIDTH/CELLSIZE)
CELLHEIGHT=int(WINDOWHEIGHT/CELLSIZE)
#      R    G   B
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
DARKGREEN=(0,140,0)
DARKGRAY=(40,40,40)
CREAM=(255,192,103)
BGCOLOR=CREAM
BLUE=(0,0,255)
PINK=(255,50,180)
DARKRED=(150,0,0)

UP='up'
DOWN='down'
LEFT='left'
RIGHT='right'
#index of snake's head
HEAD=0 
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    #clock of the game
    FPSCLOCK=pygame.time.Clock()
    #set_mode sets the the size of screen according to the given specifications
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT=pygame.font.Font('freesansbold.ttf',20)
    pygame.display.set_caption('SNAKE SNACK')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    #a random start point is set
    startx=random.randint(5,CELLWIDTH-5)
    starty=random.randint(5,CELLHEIGHT-5)
    #apple appears at a random location
    apple=getRandomLocation()
    snakeCoords=[{'x':startx,'y':starty}, {'x':startx-1,'y':starty-1}, {'x':startx-2,'y':starty-2}]
    direction=RIGHT


   

    while True: #main game loop
        for event in pygame.event.get():#event handling loop
            if event.type==QUIT:
                terminate()
            elif event.type==KEYDOWN:
                if(event.key==K_LEFT or event.key==K_a) and direction!=RIGHT:
                    direction=LEFT
                elif (event.key==K_RIGHT or event.key==K_d) and direction!=LEFT:
                    direction=RIGHT
                elif (event.key==K_UP or event.key==K_w) and direction!=DOWN:
                    direction=UP
                elif (event.key==K_DOWN or event.key==K_s) and direction!=UP:
                    direction=DOWN
                elif event.key == K_ESCAPE:
                    terminate()
        #check if the snake has hit itself or the edge 
        if snakeCoords[HEAD]['x']==-1 or snakeCoords[HEAD]['x']==CELLWIDTH or snakeCoords[HEAD]['y']==-1 or snakeCoords[HEAD]['y']==CELLHEIGHT:
            return #game over

        for snakeBody in snakeCoords[1:]:
            if snakeBody['x']==snakeCoords[HEAD]['x'] and snakeBody['y']==snakeCoords[HEAD]['y']:
                return #game over
        if snakeCoords[HEAD]['x']==apple['x'] and snakeCoords[HEAD]['y']==apple['y']:
            #set a new apple somewhere at a random location
            apple=getRandomLocation()
        else:
            #remove snake's tail segment
            del snakeCoords[-1]
        #move the snake by adding a segment in the direction it is moving
        if direction==UP:
            newHead={'x':snakeCoords[HEAD]['x'],'y':snakeCoords[HEAD]['y']-1}
        elif direction==DOWN:
            newHead={'x':snakeCoords[HEAD]['x'],'y':snakeCoords[HEAD]['y']+1}
        elif direction==LEFT:
            newHead={'x':snakeCoords[HEAD]['x']-1,'y':snakeCoords[HEAD]['y']}
        elif direction==RIGHT:
            newHead={'x':snakeCoords[HEAD]['x']+1,'y':snakeCoords[HEAD]['y']}
        snakeCoords.insert(0,newHead)
        DISPLAYSURF.fill(BGCOLOR)#filling the background colour
        drawGrid()#draw gridlines in the screen
        drawSnake(snakeCoords)#drawing snake according to its coordinates
        scor=(len(snakeCoords))-3#specify the condition of score
        drawApple(apple)
        drawScore(scor)
        x= levels(scor)
        pygame.display.update()
        #specifying the speed of snake
        m=FPS+(x*2)
        if(m>18):#limit the speed of snake
            m=18
        FPSCLOCK.tick(m)
#getting highscore from the file
def get_highscore(score):
    high_score=score
    high_score_file=open("high_score.txt",'r+')
    high_score=high_score_file.read()
    high_score_file.close()
    return high_score
#saving new score
def save_new_score(score):
    high_score=score
    high_score_file=open("high_score.txt",'r+')
    high_score_file.write(str(score))
    high_score_file.close()
    return high_score
    
def drawPressKeyMsg():
    #render is used to used to write any string in a window in python
    pressKeySurf=BASICFONT.render('press a key to play',True,DARKGRAY)
    pressKeyEsc=BASICFONT.render('press escape key to exit',True,DARKGRAY)
    #get_rect() is used to reserve a rectangle to write in pygame window
    pressKeyRect=pressKeySurf.get_rect()
    pressKeyRec=pressKeyEsc.get_rect()
    pressKeyRect.topright=(WINDOWWIDTH-200,WINDOWHEIGHT-30)
    pressKeyRec.topright=(WINDOWWIDTH-200,WINDOWHEIGHT-50)
    #blit is used to merge a rectangle or figure with a image
    DISPLAYSURF.blit(pressKeySurf,pressKeyRect)
    DISPLAYSURF.blit(pressKeyEsc,pressKeyRec)
#check if any key being pressed
def checkForKeyPress():
    if len(pygame.event.get(QUIT))>0:
        terminate()
    keyUpEvents=pygame.event.get(KEYUP)
    if len(keyUpEvents)==0:
       return None
    if keyUpEvents[0].key==K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def showStartScreen():
    titleFont=pygame.font.Font('freesansbold.ttf',50)
    bodyFont=pygame.font.Font('freesansbold.ttf',80)
    titleSurf1=titleFont.render('Snake Snack',True,WHITE)
    titleSurf2=bodyFont.render('Snake Snack',True,PINK)
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        #reserving a space for titleSurf1
        Rect1=titleSurf1.get_rect()
        Rect1.center=(WINDOWWIDTH/2,WINDOWHEIGHT/2)
        DISPLAYSURF.blit(titleSurf1,Rect1)
        #reserving a space for titleSurf2
        Rect2=titleSurf2.get_rect()
        Rect2.center=(WINDOWWIDTH/2,(WINDOWHEIGHT/2)-50)
        DISPLAYSURF.blit(titleSurf2,Rect2)
        drawPressKeyMsg()
        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def terminate():#to terminate the game
    pygame.quit()
    sys.exit()
def getRandomLocation():
    return{'x':random.randint(0,CELLWIDTH-1),'y':random.randint(0,CELLHEIGHT-1)}
def showGameOverScreen():
    gameOverFont=pygame.font.Font('freesansbold.ttf',100)
    gameSurf=gameOverFont.render('Game',True,DARKRED)
    overSurf=gameOverFont.render('Over',True,DARKRED)
    gameRect=gameSurf.get_rect()
    overRect=overSurf.get_rect()
    gameRect.midtop=(WINDOWWIDTH/2,10)
    overRect.midtop=(WINDOWWIDTH/2,gameRect.height+35)
    DISPLAYSURF.blit(gameSurf,gameRect)
    DISPLAYSURF.blit(overSurf,overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(5)
    checkForKeyPress()
    while True:
        if checkForKeyPress():
            pygame.event.get()
            return
def drawScore(score):#this function displays the score and the high score
    scoreSurf=BASICFONT.render('Score:%s'%(score),True,WHITE)
    scoreRect=scoreSurf.get_rect()
    scoreRect.topleft=(WINDOWWIDTH-120,10)
    DISPLAYSURF.blit(scoreSurf,scoreRect)
    high_score=get_highscore(score)
    if int(high_score)< score:
        save_new_score(score)
        high_score=get_highscore(score)
    hscoreSurf=BASICFONT.render('High Score:%s'%(high_score),True,WHITE)
    hscoreRect=hscoreSurf.get_rect()
    hscoreRect.topright=(WINDOWWIDTH-850,10)
    DISPLAYSURF.blit(hscoreSurf,hscoreRect)

                              
def drawSnake(snakeCoords):
    m=0
    for coord in snakeCoords:
        x=coord['x']*CELLSIZE
        y=coord['y']*CELLSIZE
        snakeSegmentRect=pygame.Rect(x,y,CELLSIZE,CELLSIZE)
        pygame.draw.rect(DISPLAYSURF,DARKGREEN,snakeSegmentRect)
        snakeInnerSegmentRect=pygame.Rect(x+4,y+4,CELLSIZE-8,CELLSIZE-8)
        pygame.draw.rect(DISPLAYSURF,GREEN,snakeInnerSegmentRect)
        if (m>0):
            continue
        for u in range(1):
          snakeEyeRect=pygame.Rect(x+7,y+7,CELLSIZE-15,CELLSIZE-15)
          pygame.draw.rect(DISPLAYSURF,BLUE,snakeEyeRect)
          m=1
def drawApple(coord):
     x=coord['x']*CELLSIZE
     y=coord['y']*CELLSIZE
     appleRect=pygame.Rect(x,y,CELLSIZE,CELLSIZE)
     pygame.draw.rect(DISPLAYSURF,RED,appleRect)
def drawGrid():
    for x in range(0,WINDOWWIDTH,CELLSIZE):
        pygame.draw.line(DISPLAYSURF,BLACK,(x,0),(x,WINDOWHEIGHT))
    for y in range(0,WINDOWHEIGHT,CELLSIZE):
        pygame.draw.line(DISPLAYSURF,BLACK,(0,y),(WINDOWWIDTH,y))

def levels(score):
            if(score==0 or score<5):
              levelSurf=BASICFONT.render('level: %d'%1,True,WHITE)
              m=1
            else:
                  level=score/5
                  levelSurf=BASICFONT.render('level: %d'%(level+1),True,WHITE)
                  m=level+1
            levelRect=levelSurf.get_rect()
            levelRect.topleft=(WINDOWWIDTH-200,10)
            DISPLAYSURF.blit(levelSurf,levelRect)
            return m
if __name__=='__main__':
    #calling main function
    main()
    
  
                            
        
