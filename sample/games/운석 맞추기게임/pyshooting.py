import pygame
import random
from time import sleep

# https://wikidocs.net/65638
BLACK = (0, 0, 0)
padWidth = 480
padHeight = 640

pygame.init()
gamePad = pygame.display.set_mode((padWidth, padHeight))
pygame.display.set_caption('PyShooting')
background = pygame.image.load('assets/background.png')
fighter =  pygame.image.load('assets/fighter.png')
missile = pygame.image.load('assets/missile.png')
explosion = pygame.image.load('assets/explosion.png')
pygame.mixer.music.load('assets/music.wav')
pygame.mixer.music.play(-1)
missileSound = pygame.mixer.Sound('assets/missile.wav')
gameOverSound = pygame.mixer.Sound('assets/gameover.wav')
clock = pygame.time.Clock()

rockImage = ['assets/rock01.png', 'assets/rock02.png', 'assets/rock03.png', 'assets/rock04.png', 'assets/rock05.png',
             'assets/rock06.png', 'assets/rock07.png', 'assets/rock08.png', 'assets/rock09.png', 'assets/rock10.png',
             'assets/rock11.png', 'assets/rock12.png', 'assets/rock13.png', 'assets/rock14.png', 'assets/rock15.png',
             'assets/rock16.png', 'assets/rock17.png', 'assets/rock18.png', 'assets/rock19.png', 'assets/rock20.png',
             'assets/rock21.png', 'assets/rock22.png', 'assets/rock23.png', 'assets/rock24.png', 'assets/rock25.png',
             'assets/rock26.png', 'assets/rock27.png', 'assets/rock28.png', 'assets/rock29.png', 'assets/rock30.png']
explosionSound = ['assets/explosion01.wav', 'assets/explosion02.wav', 'assets/explosion03.wav', 'assets/explosion04.wav']

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def writeScore(count):
    global gamePad
    font = pygame.font.Font('assets/NanumGothic.ttf', 20)
    text = font.render('파괴한 운석 수: ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font('assets/NanumGothic.ttf', 20)
    text = font.render('놓친 운석 수: ' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (360, 0))

def writeMessage(text):
    textfont = pygame.font.Font('assets/NanumGothic.ttf', 80)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)

def crash():
    global gamePad
    writeMessage('전투기 파괴!')

def gameOver():
    global gamePad
    writeMessage('게임 오버!')

fighterSize = fighter.get_rect().size
fighterWidth = fighterSize[0]
fighterHeight = fighterSize[1]

x = padWidth *0.45
y = padHeight * 0.9
fighterX = 0

missileXY = []

rock = pygame.image.load(random.choice(rockImage))
rockSize = rock.get_rect().size
rockWidth = rockSize[0]
rockHeight = rockSize[1]
destroySound = pygame.mixer.Sound(random.choice(explosionSound))

rockX = random.randrange(0, padWidth - rockWidth)
rockY = 0
rockSpeed = 2

isShot = False
shotCount = 0
rockPassed = 0

while True:
    #gamePad.fill(BLACK)
    drawObject(background, 0, 0)

    event = pygame.event.poll()
    if event.type in [pygame.QUIT]:
        break

    if event.type in [pygame.KEYDOWN]:
        if event.key == pygame.K_LEFT:
            fighterX -= 5
        elif event.key == pygame.K_RIGHT:
            fighterX += 5
        elif event.key == pygame.K_SPACE:
            missileSound.play()
            missileX = x + fighterWidth/2
            missileY = y - fighterHeight
            missileXY.append([missileX, missileY])

    if event.type in [pygame.KEYUP]:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            fighterX = 0

    x += fighterX
    if x < 0:
        x = 0
    elif x > padWidth - fighterWidth:
        x = padWidth - fighterWidth

    if y < rockY + rockHeight:
        if (rockX > x and rockX < x + fighterWidth) or \
        (rockX + rockWidth > x  and rockX + rockWidth < x + fighterWidth):
            crash()

    drawObject(fighter, x, y)

    if len(missileXY) != 0:
        for i, bxy in enumerate(missileXY):
            bxy[1] -= 10
            missileXY[i][1] = bxy[1]

            if bxy[1] < rockY:
                if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                    missileXY.remove(bxy)
                    isShot = True
                    shotCount += 1

            if bxy[1] <= 0:
                try:
                    missileXY.remove(bxy)
                except:
                    pass

    if len(missileXY) != 0:
        for bx, by in missileXY:
            drawObject(missile, bx, by)

    writeScore(shotCount)

    rockY += rockSpeed

    if rockY > padHeight:
        rock = pygame.image.load(random.choice(rockImage))
        rockSize = rock.get_rect().size
        rockWidth = rockSize[0]
        rockHeight = rockSize[1]
        rockX = random.randrange(0, padWidth - rockWidth)
        rockY = 0
        rockPassed += 1

    if rockPassed == 3:
        gameOver()

    writePassed(rockPassed)

    if isShot:
        drawObject(explosion, rockX, rockY)
        destroySound.play()

        rock = pygame.image.load(random.choice(rockImage))
        rockSize = rock.get_rect().size
        rockWidth = rockSize[0]
        rockHeight = rockSize[1]
        rockX = random.randrange(0, padWidth, rockWidth)
        rockY = 0
        destroySound = pygame.mixer.Sound(random.choice(explosionSound))
        isShot = False

        rockSpeed += 0.02
        if rockSpeed >= 10:
            rockSpeed = 10

    drawObject(rock, rockX, rockY)

    pygame.display.update()

    clock.tick(60)

pygame.quit()