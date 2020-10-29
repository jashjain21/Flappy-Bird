import random  # for generating random numbers (for flappy bird pipes)
import sys  # if user wants to exit the game use sys.exit
import pygame
from pygame.locals import *  # basic pygame imports

# Global variables for the game
FPS = 32  # frames per seconf if less than lag feeling we get
SCREENWIDTH = 289
SCREENHEIGHT = 511
# above 2 numbers made by taking in consideration phone size(average like)
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8  # taking 80 percent of the screen height
GAME_SPRITES = {}  # to display the image
GAME_SOUNDS = {}  # to play the sound
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'


def welcomeScreen():
    """
    Shows welcome images on the screen
    """
    playerx = int(SCREENWIDTH / 5)  # players x position should be 1/5th thewidth from the left
    # basically denotes x position of bird.Typecasted to integer for easier rendering rather than float
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0  # so that it starts from the start of the screen
    while True:
        for event in pygame.event.get():  # ges all the keystrokes pressed by the user
            # if user clicks on cross button close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # keydown means keypressed
                # QUIT IS pygame's event for quitting
                pygame.quit()
                sys.exit()
                # if user presses space or up key start the game for him
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # means now we gotta go to main game na hence now return
                return
            else:  # else start blitting images
                # coordinates are from top left corner always in pygame
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()  # unless and until this function is run ur screen wouldnt change
                FPSCLOCK.tick(FPS)


def mainGame():
    # print("In maingame")
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENHEIGHT / 2)
    basex = 0
    # get pipe 's list liek eg [{'x':,'y':},{'x':,'y':}] for upper and lower pipe coordinates
    # create 2 pipes for blitting on screen
    # took 2 such set of pipes coz on one screen 2 such pairs would be better
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    # mylist of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]
    # my list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]
    # thus due to SCREENWIDTH +200 AND SCREENWIDTH+200+SCREENWIDHT/2 U
    # get a sequencde of pipes

    pipeVelX = -4  # vel of pipe moving pipe moving backward gives illusion bird moving forward

    playerVelY = -9  # player falls down bt gets an acceleration of 1 hence min will still remai 8
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity due to acceleration while flapping
    playerFlapped = False  # True when bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:  # means he is in screen
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)  # function returns true if u crash
        if crashTest:
            return

        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        # so that we get to the middle of the player and if he crosses the pipe increase his score by 1
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False  # like he did it once na hence so
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0][
            'x'] < 5:  # just abt to exit add a new pipe when the first pipe is abt to cross the leftmost part of the screen
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
        # if pipe out of screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # lets now blit our screen

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        # SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        myDigits = [int(x) for x in list(str(score))]
        # so that if score is 21 u get myDigits as [2,1]

        width = 0  # total wdth which my nubmers would take
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()  # so that next number ki height we get
        pygame.display.update()  # unless and until this function is run ur screen wouldnt change
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    # if player y is greater than GROUNDY - 25 or playery< 0
    if playery > GROUNDY - 25 or playery < 0:  # 24 is height of bird hence took this
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        print(f"Pipe height variable is {pipeHeight} and playery is {playery}")
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) <
                GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    return False


def getRandomPipe():
    '''
    generate position of 2 pipes for blitting on screen
    one bottom normal and top inverted
    '''
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()  # heihgt remains same no matter inverted or not
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(
        SCREENHEIGHT - GAME_SPRITES['base'].get_height() - offset * 1.2))  # Syntax. random.randrange(start, stop, step)
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper pipe
        {'x': pipeX, 'y': y2}  # lower pipe
    ]
    return pipe


if __name__ == "__main__":
    # this is the main function from where it starts like our game
    pygame.init()  # initialsies pygame's all modules
    FPSCLOCK = pygame.time.Clock()  # will get me a clock which i can tick used to control game's fps so that above upper
    # limit not more frames would be rendered
    pygame.display.set_caption("Flappy bird by MJK")
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        # The new surface will be in a format suited for quick
        # blitting to the given format with per pixel alpha. If no surface is given, the new surface will be optimized for
        # blitting to the current display.
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),  # rotating pipe to show it upwards
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SOUNDS['die'] = pygame.mixer.Sound(
        'gallery/audio/die.wav')  # due to this object being created can play song using .play() method
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
    # thus created a key value dictionary pair

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()  # the initial screen when user presses any button go to mainGame
        mainGame()  # main game function
