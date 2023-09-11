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
screenCaptions = ["FlapPy Bird", "Flabby Birb", "Also Try Minecraft", "Also Try Terraria"]
randomCaptionIndex = random.randint(0, (len(screenCaptions)-1))
pygame.display.set_caption(screenCaptions[randomCaptionIndex])

# Setting up the clock
FPS = 60
clock = pygame.time.Clock()

# Reference Images
PIPE_IMG = r"SamplePics\pipe.png"
PLAYER_IMG = r"SamplePics\babyyoda.jpg"

# Presentational variables (non-pygame)
font = pygame.font.SysFont(None, 72)
black = (0,0,0)
skyBlue = (51,153,255)
darkGreen = (0,153,0)

# Unpack save data
# Read the file and parse the data into "playerData" variable
with open('flap.json', 'r') as file:
    readPlayerData = file.read()
    playerData = json.loads(readPlayerData)
    file.close()
# Parse the player data
highScore = playerData['highScore']

# Player class
class Player():
    velocity = 7
    acceleration = 0.5

    def __init__(self, x: int, y: int, width: int, height: int, src: str) -> None: # void
        image = pygame.image.load(src)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def Update(self) -> None:
        Player.velocity -= Player.acceleration
        self.rect.y -= Player.velocity

# Pipe class for pipe object
class Pipe():
    VELOCITY = 5
    GAP_SIZE = 1170
    SEPARATION = 650

    def __init__(self, x: int, y: int, src: str):
        # initialize the bottom pipe
        # initialize the top pipe relative to the bottom pipe
        self.botImage = pygame.image.load(src)
        
        self.topImage = pygame.transform.flip(self.botImage, False, True)

        self.botRect = self.botImage.get_rect()
        self.topRect = self.topImage.get_rect()

        self.botRect.x = x
        self.botRect.y = y
        self.topRect.x = self.botRect.x
        self.topRect.y = self.botRect.y-self.GAP_SIZE

    # To update after each game loop
    def Update(self):
        if self.endReached():
            # reset the pipe
            self.botRect.x = SCREEN_WIDTH
            self.botRect.y = random.randint(SCREEN_HEIGHT//3, SCREEN_HEIGHT*0.8)
            # reset the top pipe, too
            self.topRect.x = self.botRect.x
            self.topRect.y = self.botRect.y-self.GAP_SIZE
        else:
            self.topRect.x -= Pipe.VELOCITY
            self.botRect.x -= Pipe.VELOCITY
            screen.blit(self.botImage, self.botRect)
            screen.blit(self.topImage, self.topRect)
    
    def endReached(self) -> bool:
        if self.topRect.x <= -self.SEPARATION:
            return True
        return False


# Button/GUI class
class Element():
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y

    # Method to draw button to the screen with given text
    # Automatically centers the text
    def Draw(self, text: str) -> None:
        pygame.draw.rect(screen, skyBlue, self.rect)
        renderedText = font.render(text, True, black)
        screen.blit(renderedText, (self.x+(self.width//6), self.y+(self.height//6)))

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
        pipes = []
        sep = Pipe.SEPARATION
        for _ in range(3):
            pipes.append(Pipe(SCREEN_WIDTH-sep, random.randint(SCREEN_HEIGHT//3, SCREEN_HEIGHT*0.8), PIPE_IMG))
            sep -= Pipe.SEPARATION
        player = Player(SCREEN_WIDTH//7, SCREEN_HEIGHT//2, 100, 100, PLAYER_IMG)

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
                GameOverElement.Draw("Game Over")
                # halt 
                Player.acceleration = 0
                Player.velocity = 0
                Pipe.velocity = 0
                PlayButton.Draw("Play")
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
                            player.rect.x = SCREEN_WIDTH//7
                            player.rect.y = SCREEN_HEIGHT//2
                            Player.velocity = 7
                            Player.acceleration = 0.5

                            sep = Pipe.SEPARATION
                            for obj in pipes:
                                obj.botRect.x, obj.topRect.x = SCREEN_WIDTH-sep, SCREEN_WIDTH-sep
                                obj.botRect.y = random.randint(SCREEN_HEIGHT//3, SCREEN_HEIGHT*0.8)
                                obj.topRect.y = obj.botRect.y-Pipe.GAP_SIZE
                                sep -= Pipe.SEPARATION
                            Pipe.velocity = 5
                            
                            score = 0
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
                player.Update()
                for obj in pipes:
                    obj.Update()

                # If player leaves the screen
                if player.rect.y < 0 or player.rect.y > SCREEN_HEIGHT:
                    gameOver = True

                # Checking pipe collisions
                for obj in pipes:
                    if player.rect.colliderect(obj.botRect) or player.rect.colliderect(obj.topRect):
                        gameOver = True
                    elif player.rect.x == obj.botRect.x + (obj.botRect.width):
                        score += 1

                # Updating score as necessary
                if score > highScore:
                    highScore = score

            ScoreElement.Draw(f"Score: {score}")
            HighScoreElement.Draw(f"Highscore: {highScore}")

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
