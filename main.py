import random # for generating random numbers
import sys #we will use sys.exit to exit the program
import pygame
from pygame.locals import* #Basic pygame imports
# global variables for game
FPS=32 # frame per second
SCREENWIDTH=289
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))# for initialzing game window
GROUNDY=SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='Gallery/sprites/bird.png'
BACKGROUND='Gallery/sprites/background.png'
PIPE='Gallery/sprites/pipe.png'
# main method start
def welcomescreen():
    playerx=int(SCREENWIDTH*0.1)
    playery=int(SCREENHEIGHT*0.46)
    messagex=int(SCREENWIDTH*0.000005)
    messagey=int(SCREENHEIGHT*0.00005)
    basex=0
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.type==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def maingame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENHEIGHT*0.45)
    basex=0
    # create two pipes for blitting on the screen
    newpipe1=getRandompipe()
    newpipe2=getRandompipe()
    # my List of upper pipes
    upperpipes = [
        {'x': SCREENWIDTH+200, 'y':newpipe1[0]['y']},
        {'x':  SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newpipe2[0]['y']}
    ]
    # my List of lower pipes
    lowerpipes = [
        {'x': SCREENWIDTH+200, 'y':newpipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newpipe2[1]['y']}
    ]
    
    pipevelx= -4
    playervely = -9
    playermaxvel = 10
    playerminvel= -8
    playeraccY=1
    playerFlaAccv= -8
    playerFlapped=False
    # playerFlapped=False  true only when bird is flapped
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playervely=playerFlaAccv
                    playerFlapped=True
                    GAME_SOUNDS['wing'].play()
        chrashtest=iscollide(playerx,playery,upperpipes,lowerpipes)
        if chrashtest:
            return
        playermidpos = playerx + GAME_SPRITES['player'].get_width()/2
        # to increase score
        for pipe in upperpipes:
            pipemidpos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipemidpos<= playermidpos < pipemidpos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()
        if playervely<playermaxvel and not playerFlapped:
            playervely+=playeraccY
        if playerFlapped:
            playerFlapped=False
        playerheight=GAME_SPRITES['player'].get_height()
        playery=playery+min(playervely,GROUNDY-playery-playerheight)
        # move pipes to left
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x']+=pipevelx
            lowerpipe['x']+=pipevelx
        # add new pipe when first about  to the cross
        if 0<upperpipes[0]['x']<5:
           newpipe=getRandompipe()
           upperpipes.append(newpipe[0])
           lowerpipes.append(newpipe[1]) 
        # if pipe out of screen
        if upperpipes[0]['x']<-GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
        # lets blit our sprites
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperpipe['x'],upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        # print(myDigits)
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def iscollide(playerx,playery,upperpipes,lowerpipes):
    if playery > GROUNDY-25 or playery<0:
        GAME_SOUNDS['die'].play()
        return True
    for pipe in upperpipes:
        pipeheight=GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeheight+pipe['y'] and abs(playerx-pipe['x'])<GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerpipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False

# to get random pipes
def getRandompipe():
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    offset=SCREENHEIGHT/3
    y2=offset + random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex=SCREENWIDTH + 1
    y1=pipeHeight-y2+offset
    pipe=[{'x':pipex,'y':-y1},{'x':pipex,'y':y2}]        
    # print(pipe)
    return pipe
if __name__=='__main__':
    pygame.init()
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption('FlappyBird By Rayyan')
    GAME_SPRITES["numbers"]=(
    pygame.image.load('gallery/sprites/0.png').convert_alpha(),
    pygame.image.load('gallery/sprites/1.png').convert_alpha(),
    pygame.image.load('gallery/sprites/2.png').convert_alpha(),
    pygame.image.load('gallery/sprites/3.png').convert_alpha(),
    pygame.image.load('gallery/sprites/4.png').convert_alpha(),
    pygame.image.load('gallery/sprites/5.png').convert_alpha(),
    pygame.image.load('gallery/sprites/6.png').convert_alpha(),
    pygame.image.load('gallery/sprites/7.png').convert_alpha(),
    pygame.image.load('gallery/sprites/8.png').convert_alpha(),
    pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )
    GAME_SPRITES['message']=(pygame.image.load('gallery/sprites/message.png').convert_alpha())
    GAME_SPRITES['base']=(pygame.image.load('gallery/sprites/base.png').convert_alpha())
    GAME_SPRITES['background']=(pygame.image.load(BACKGROUND).convert())
    GAME_SPRITES['pipe']=(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha())
    GAME_SPRITES['player']=(pygame.image.load(PLAYER).convert_alpha())
    pygame.mixer.init()
    GAME_SOUNDS['die']=(pygame.mixer.Sound('gallery/Audios/die.mp3'))
    GAME_SOUNDS['hit']=(pygame.mixer.Sound('gallery/Audios/hit.wav'))
    GAME_SOUNDS['swoosh']=(pygame.mixer.Sound('gallery/Audios/swoosh.wav'))
    GAME_SOUNDS['point']=(pygame.mixer.Sound('gallery/Audios/point.wav'))
    GAME_SOUNDS['wing']=(pygame.mixer.Sound('gallery/Audios/wing.mp3'))
while True:
    welcomescreen()# shows welcome screen to user
    maingame()# this is the main game function