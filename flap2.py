# October 2022 ish
# second attempt at flappy bird
# incorporating OOP

import pygame, random, os, json

# Ensure that the working directory is the file's folder directory
os.chdir(os.path.dirname(__file__))
pygame.init()

# Setting up the screen
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setting up the caption (random, for the lols)
screenCaptions = ["Class Flap", "Flabby Birb", "Also Try Minecraft", "Also Try Terraria"]
randomCaptionIndex = random.randint(0, (len(screenCaptions)-1))
pygame.display.set_caption(screenCaptions[randomCaptionIndex])

# Setting up the clock
FPS = 60
clock = pygame.time.Clock()

# Presentational variables (non-pygame)
font = pygame.font.SysFont(None, 72)
black = (0,0,0)
skyBlue = (51,153,255)
darkGreen = (0,153,0)

# Unpack save data
# Read the file and parse the data into "playerData" variable
with open('flap.json', 'r') as file:
    encodedPlayerData = file.read()
    playerData = json.loads(encodedPlayerData)
    file.close()
# Parse the player data
highScore = playerData['highScore']

# Player class
class Player():
    velocity = 7
    acceleration = .5

    def __init__(self, x, y, width, height, src): # void
        image = pygame.image.load(src)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        Player.velocity -= Player.acceleration
        self.rect.y -= Player.velocity

# Pipe class for pipe object
class Pipe():
    velocity = 5

    def __init__(self, x, y, src): # void
        # initialize the bottom pipe
        self.botImage = pygame.image.load(src)
        self.botRect = self.botImage.get_rect()
        self.botRect.x = x
        self.botRect.y = y
        # initialize the top pipe
        self.topImage = pygame.transform.flip(self.botImage, False, True)
        self.topRect = self.topImage.get_rect()
        self.topRect.x = self.botRect.x
        self.topRect.y = self.botRect.y-1170

    # To update after each game loop
    def update(self):
        if self.topRect.x <= -650:
            # reset the pipe
            self.botRect.x = SCREEN_WIDTH
            self.botRect.y = random.randint(350, 700)
            # reset the top pipe, too
            self.topRect.x = self.botRect.x
            self.topRect.y = self.botRect.y-1170
        else:
            self.topRect.x -= Pipe.velocity
            self.botRect.x -= Pipe.velocity
            screen.blit(self.botImage, self.botRect)
            screen.blit(self.topImage, self.topRect)

# Button/GUI class
class Element():
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y

    # Method to draw button to the screen with given text
    # Automatically centers the text
    def draw(self, text):
        pygame.draw.rect(screen, skyBlue, self.rect)
        renderedText = font.render(text, True, black)
        screen.blit(renderedText, (self.x+self.width//6, self.y+self.height//6))

# Game class
class Flap():
    # Initializing will simply run main
    def __init__(self):
        self.Main()
        
    def Main(self):
        global highScore

        # Game variables
        score = 0
        gameOver = False

        # Surface variables
        bg = pygame.image.load(r"SamplePics\starwarsbg.jpg")
        pipe1 = Pipe(SCREEN_WIDTH-650, random.randint(350, 700), r"SamplePics\pipe.png")
        pipe2 = Pipe(SCREEN_WIDTH, random.randint(350, 700), r"SamplePics\pipe.png")
        pipe3 = Pipe(SCREEN_WIDTH+650, random.randint(350, 700), r"SamplePics\pipe.png")
        player = Player(215, SCREEN_HEIGHT//2, 100, 100, r"SamplePics\babyyoda.jpg")

        # Game elements
        PlayButton = Element(SCREEN_WIDTH//2-80, SCREEN_HEIGHT//2, 160, 80)
        GameOverElement = Element(SCREEN_WIDTH//2-250, SCREEN_HEIGHT//2-80, 500, 80)
        ScoreElement = Element(SCREEN_WIDTH-400, 50, 400, 50)
        HighScoreElement = Element(SCREEN_WIDTH-400, 100, 400, 50)

        # Transforming (fitting into screen)
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Main game loop
        clicked = False
        run = True
        while run:
            screen.blit(bg, (0,0))
            screen.blit(player.image, player.rect)

            if gameOver:
                GameOverElement.draw("Game Over")
                # halt 
                Player.acceleration = 0
                Player.velocity = 0
                Pipe.velocity = 0
                PlayButton.draw("Play")
                # game-over event handler
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    # "clicked" variable to allow for holding down mouse button
                    if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                        clicked = True
                    if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                        clicked = False
                        pos = pygame.mouse.get_pos()
                        if PlayButton.rect.collidepoint(pos):
                            # Reset player position
                            player.rect.x = 215
                            player.rect.y = SCREEN_HEIGHT//2

                            # (REVISE IF AND WHEN POSSIBLE)
                            # Reset pipe 1 position 
                            pipe1.botRect.x, pipe1.topRect.x = SCREEN_WIDTH-650, SCREEN_WIDTH-650
                            pipe1.botRect.y = random.randint(350, 700)
                            pipe1.topRect.y = pipe1.botRect.y-1170
                            # Reset pipe 2 position
                            pipe2.botRect.x, pipe2.topRect.x = SCREEN_WIDTH, SCREEN_WIDTH
                            pipe2.botRect.y = random.randint(350, 700)
                            pipe2.topRect.y = pipe2.botRect.y-1170
                            # Reset pipe 3 position
                            pipe3.botRect.x, pipe3.topRect.x = SCREEN_WIDTH+650, SCREEN_WIDTH+650
                            pipe3.botRect.y = random.randint(350, 700)
                            pipe3.topRect.y = pipe3.botRect.y-1170
                            # Reinstantiate player (just to be safe)
                            player = Player(215, SCREEN_HEIGHT//2, 100, 100, r"SamplePics\babyyoda.jpg")
                            score = 0
                            # Reset variables
                            Player.acceleration = .5
                            Player.velocity = 7
                            Pipe.velocity = 5
                            gameOver = False
            else: # For in-game (not game over)
                # in-game event handler
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # make character jump (set velocity to point upwards)
                        Player.velocity = 12.5

                # Update game objects
                player.update()
                pipe1.update()
                pipe2.update()
                pipe3.update()

                # If player leaves the screen
                if player.rect.y < 0 or player.rect.y > 800:
                    gameOver = True

                # Checking pipe collisions (REVISE IF AND WHEN POSSIBLE)
                if player.rect.colliderect(pipe1.botRect) or player.rect.colliderect(pipe1.topRect):
                    gameOver = True
                if player.rect.colliderect(pipe2.botRect) or player.rect.colliderect(pipe2.topRect):
                    gameOver = True
                if player.rect.colliderect(pipe3.botRect) or player.rect.colliderect(pipe3.topRect):
                    gameOver = True
                
                # Check the score as necessary
                if player.rect.x == pipe1.botRect.x + 100:
                    score += 1
                elif player.rect.x == pipe2.botRect.x + 100:
                    score += 1
                elif player.rect.x == pipe3.botRect.x + 100:
                    score += 1

                # Updating score as necessary
                if score > highScore:
                    highScore = score

            ScoreElement.draw(f"Score: {score}")
            HighScoreElement.draw(f"Highscore: {highScore}")

            # Updating clock and display
            pygame.display.update()
            clock.tick(FPS)

if __name__ == "__main__":
    # Run main
    Flap()

    # Save
    playerData['highScore'] = highScore
    with open('flap.json', 'w') as f:
        json.dump(playerData, f, indent=4)
        f.close()
