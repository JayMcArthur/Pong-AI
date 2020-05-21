# Import the pygame library and initialise the game engine
import pygame
import time
import sys
import random
from random import randint
from AI import neuralNetwork

pygame.init()
pygame.font.init()

# Define some Var
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SILVER = (105, 105, 105)
WIN_X = 960
WIN_Y = 540
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 20
WIN_CON = 10
#Sets up AI
IN_NODES = 3
HID_HEI = 2
HID_LEN = 2
OUT_NODES = 3
LEARN = 0.3
AI = neuralNetwork(IN_NODES, HID_HEI, HID_LEN, OUT_NODES, LEARN)
TRAIN_TIME = 4


# Open a new window
screen = pygame.display.set_mode((WIN_X, WIN_Y))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()



class Paddle(pygame.sprite.Sprite):
    width = PADDLE_WIDTH
    height = PADDLE_HEIGHT
    
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()
        
    def moveUp(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
          self.rect.y = 0
          
    def moveDown(self, pixels):
        self.rect.y += pixels
        if self.rect.y > WIN_Y - PADDLE_HEIGHT:
          self.rect.y = WIN_Y - PADDLE_HEIGHT

    def draw(self, win):
        pass


class Ball(pygame.sprite.Sprite):
    width = BALL_SIZE
    height = BALL_SIZE
    color = RED

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, self.color, (5, 5), 5)
        self.velocity = [randint(-3, 3), randint(-10, 10)]
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = ((abs(self.velocity[0]) + 1) * -self.velocity[0]/abs(self.velocity[0]))
        self.velocity[1] += randint(-5, 5)

def trainAI(AI):
    for i in range(10000):
        y = random.randrange(1,101) / 100
        z = random.randrange(1,101) / 100
        if (z > y):
            AI.train([y,random.randrange(1,101)/100,z], [0.99,0.01,0.01])
            AI.train([z,random.randrange(1,101)/100,z], [0.01,0.99,0.01])
        elif (z == y):
            AI.train([y,random.randrange(1,101)/100,z], [0.01,0.99,0.01])
        elif (z < y):
            AI.train([z,random.randrange(1,101)/100,z], [0.01,0.99,0.01])
            AI.train([y,random.randrange(1,101)/100,z], [0.01,0.01,0.99])

# Setup Players
all_sprites_list = pygame.sprite.Group()

player = Paddle(WHITE)
player.rect.x = 0
player.rect.y = WIN_Y/2 - PADDLE_HEIGHT/2
all_sprites_list.add(player)
scoreP = 0

theAI = Paddle(BLUE)
theAI.rect.x = WIN_X - 10
theAI.rect.y = WIN_Y/2 - PADDLE_HEIGHT/2
all_sprites_list.add(theAI)
scoreA = 0
trainAI(AI)

ball = Ball()
ball.rect.x = WIN_X/2 - BALL_SIZE/2
ball.rect.y = WIN_Y/2 - BALL_SIZE/2
all_sprites_list.add(ball)

# -------- Main Program Loop -----------
while True:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            break
    if scoreP >= WIN_CON:
        screen.fill(BLACK)
        textSurface = END_FONT.render('PLAYER 1 WINS!', False, (255, 255, 255))
        screen.blit(textSurface, (58, 200))
        pygame.display.update()
        break
    elif scoreA >= WIN_CON:
        screen.fill(BLACK)
        textSurface = END_FONT.render('PLAYER 2 WINS!', False, (255, 255, 255))
        screen.blit(textSurface, (58, 200))
        pygame.display.update()
        break


    # Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.moveUp(5)
    if keys[pygame.K_s]:
        player.moveDown(5)

    theAIMove = AI.query([ (ball.rect.y + BALL_SIZE/2)/WIN_Y, (ball.rect.x + BALL_SIZE/2)/WIN_X, (theAI.rect.y + PADDLE_HEIGHT/2)/WIN_Y ])
    if theAIMove[0] > theAIMove[1] and theAIMove[0] > theAIMove[2]:
        theAI.moveUp(6.5)
    elif theAIMove[2] > theAIMove[1] and theAIMove[2] > theAIMove[0]:
        theAI.moveDown(6.5)
        
        # --- Game logic should go here
    all_sprites_list.update()

    if ball.velocity[0] == 0:
        ball.velocity[0] = -7

    # Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x >= WIN_X - PADDLE_WIDTH/2:
        scoreP += 1
        ball.velocity = [randint(-3, 3), randint(-10, 10)]
        ball.rect.x = WIN_X/2 - BALL_SIZE/2

    if ball.rect.x + PADDLE_WIDTH/2 <= 0:
        scoreA += 1
        ball.velocity = [randint(-3, 3), randint(-10, 10)]
        ball.rect.x = WIN_X/2 - BALL_SIZE/2

    if ball.rect.y > WIN_Y - BALL_SIZE:
        ball.rect.y = WIN_Y - BALL_SIZE
        ball.velocity[1] = -ball.velocity[1]

    if ball.rect.y < 0 :
        ball.rect.y = 0
        ball.velocity[1] = -ball.velocity[1]

        # Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, player) or pygame.sprite.collide_mask(ball, theAI):
        ball.bounce()
        ball.update()

    # --- Drawing code should go here
    # First, clear the screen to black.
    screen.fill(BLACK)
    # Draw the net
    pygame.draw.line(screen, WHITE, [WIN_X/2 - 3, 0], [WIN_X/2 - 3, WIN_Y], 6)

    # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen)

    # Display scores:
    text = STAT_FONT.render(str(scoreP), 1, WHITE)
    screen.blit(text, (0 + 240, 10))
    text = STAT_FONT.render(str(scoreA), 1, WHITE)
    screen.blit(text, (WIN_X - 240, 10))
    textSurface = STAT_FONT.render('P1', False, (255, 255, 255))
    screen.blit(textSurface, (85, 15))
    textSurface = STAT_FONT.render('P2', False, (255, 255, 255))
    screen.blit(textSurface, (WIN_X - 85, 15))

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(90)

pygame.quit()
