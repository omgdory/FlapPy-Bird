# October 7, 2022
# first attempt at making flappy bird.
# not using any OOP at all except those imported.
# THIS FILE IS NOT THE FINAL FILE; SEE "flap2.py"

import pygame, random, time, os, json

os.chdir(os.path.dirname(__file__))
pygame.init()

# window size
window_width = 1300
window_height = 800

# setting up the window
window = pygame.display.set_mode((window_width, window_height))
windowCaptions = ["Flabby Bird", "Flapster"] # for the lols
randomCaptionIndex = random.randint(0, (len(windowCaptions)-1))
pygame.display.set_caption(windowCaptions[randomCaptionIndex])

# define pygame-specific variables
font = pygame.font.SysFont(None, 72)
bg = pygame.image.load(r"SamplePics\starwarsbg.jpg")
bg = pygame.transform.scale(bg, (window_width,window_height))
pipe = pygame.image.load(r"SamplePics\pipe.png")
pipeRect = pipe.get_rect()
topPipe = pygame.transform.flip(pipe, False, True)
topPipeRect = topPipe.get_rect()
player = pygame.image.load(r"SamplePics\flappyBird.png")
player = pygame.transform.scale(player, (100, 100))
playerRect = player.get_rect()
playRect = pygame.Rect(window_width//2-80, window_height//2, 160, 80)
playText = "Play"

# define variables
gameOver = True
clicked = False
pipeExist = False
score = 0
pipeVel = 5
playerVel = 7
accl = .5
playerRect.x = 215
playerRect.y = window_height//2
pipeRect.x = window_width-500

# define color rgb tuples
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


# getting save data
# read the file and parse the data into "playerData" variable
with open('flap.json', 'r') as file:
    encodedPlayerData = file.read()
    playerData = json.loads(encodedPlayerData)
    file.close()
    
# parse the player data
highScore = playerData['highScore']

# functions
# save function
def save():
    global highScore
    playerData['highScore'] = highScore
    with open('flap.json', 'w') as f:
        json.dump(playerData, f, indent=4)
        f.close()

# to draw home (game over) screen
def drawHome():
    pygame.draw.rect(window, green, playRect)
    renderedText = font.render(playText, True, blue)
    window.blit(renderedText, (window_width//2-50, window_height//2+10))

# to draw screen
def drawScreen():
    # draw bg and player
    window.blit(bg, (0,0))
    window.blit(player, playerRect)

    global highScore
    # change high score if needed
    if score > highScore:
        highScore = score

    # draw the score on the screen
    scoreRect = pygame.Rect(window_width-400,50,350,50)
    scoreString = "Score: " + str(score)
    renderedScore = font.render(scoreString, True, blue)

    # draw the high score on the screen
    highScoreRect = pygame.Rect(window_width-400,100,350,50)
    highScoreString = "High Score: " + str(highScore)
    renderedHighScore = font.render(highScoreString, True, blue)

    # drawing score and high score, and their respective rectangles
    pygame.draw.rect(window, green, scoreRect)
    pygame.draw.rect(window, green, highScoreRect)
    window.blit(renderedScore, (window_width-400, 50))
    window.blit(renderedHighScore, (window_width-400, 100))

# checking win conditions
def checkWin():
    global gameOver
    # check if gameOver
    if playerRect.y >= window_height or playerRect.y <= 0:
        gameOver = True
    # check player-pipe collision
    if playerRect.colliderect(pipeRect) or playerRect.colliderect(topPipeRect):
        gameOver = True


# game
run = True
while run:

    # checking the score
    if playerRect.x == pipeRect.x + 50:
        score += 1

    # if game over
    if gameOver:
        drawScreen()
        drawHome()
        pipeVel = 0
        accl = 0
        playerVel = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                pos = pygame.mouse.get_pos()
                if playRect.collidepoint(pos):
                    clicked = False
                    pipeExist = False
                    score = 0
                    pipeVel = 5
                    playerVel = 7
                    accl = .5
                    playerRect.x = 215
                    playerRect.y = window_height//2
                    pipeRect.x = window_width-500
                    gameOver = False
    # events for in-game
    else:
        drawScreen()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN: # and clicked == False:
            #     clicked = True
            # if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            #     clicked = False
                # make character jump (set velocity to point upwards)
                playerVel = 12.5
            if event.type == pygame.K_SPACE:
                playerVel = 12.5

    # move pipes and record score
    if pipeExist == False:
        pipeRect.y = window_height//random.uniform(1.1,3)
        topPipeRect.y = pipeRect.y-1170
        # print(pipeRect.y)
        pipeExist = True

    if pipeRect.x >= -370 and pipeExist:
        window.blit(pipe, pipeRect)
        topPipeRect.x = pipeRect.x
        window.blit(topPipe, topPipeRect)
    else:
        pipeRect.x = window_width
        topPipeRect.x = window_width
        pipeExist = False
    # move the pipe
    pipeRect.x -= pipeVel

    # make the player fall
    playerVel -= accl
    playerRect.y -= playerVel

    checkWin()

    # 60 fps means ~16ms per frame
    # made 10ms to account for python execution time
    time.sleep(.01)
    pygame.display.update()

save()

pygame.quit()
