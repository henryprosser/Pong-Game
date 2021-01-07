# My Python Game

# import modules
import pygame
import random
from random import randint
import math

### DEFINE VARIABLES ###

# Define colors
WHITE = (255,255,255)
BLACK = (0,0,0)

# Define speed of paddles
speed = 12

# Initial Ball coordinates
color = WHITE

# Initialise pygame
pygame.init()

# Setting font
pygame.font.init()
myfont = pygame.font.SysFont("Helvetica", 120)

# Create constant FPS
clock = pygame.time.Clock()

# Define height and width of screen
width = 800
height = 600

# Create an 800x600 sized screen
screen = pygame.display.set_mode([width,height])

# Set title of the windows
pygame.display.set_caption('Pong!')

### CLASSES ###

# Class Paddle
class Paddle(pygame.sprite.Sprite):

    def __init__ (self,paddle_x,paddle_y,color):
        super().__init__()
        self.image = pygame.Surface([7,50])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = paddle_x
        self.rect.y = paddle_y

        self.paddle_x_speed = 0
        self.paddle_y_speed = 0

        self.score = 0

    def changespeed(self,paddle_x,paddle_y):
        self.paddle_x_speed += paddle_x
        self.paddle_y_speed += paddle_y

    def update(self):
        self.rect.x += self.paddle_x_speed
        self.rect.y += self.paddle_y_speed

# Class Ball
class Ball(pygame.sprite.Sprite):
        
    def __init__ (self,color):
        super().__init__()
        self.image = pygame.Surface([7,7])
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.reset()

    def reset(self): # Setting initial ball speed & position
        self.x = 400
        self.y = 300
        self.speed = 4
        
        WrongAngle = True # Defining angle of ball at start - only accepting a certain range 
        while WrongAngle:
                self.angle = random.random()*math.pi*2
                if self.angle <= math.pi/4 and self.angle >= 0 \
                   or self.angle <= math.pi*1 and self.angle >= 3*math.pi/4 \
                   or self.angle <= 5*math.pi/4 and self.angle >= math.pi*1 \
                   or self.angle <= 2*math.pi and self.angle >= 7*math.pi/4:
                        WrongAngle = False

        self.angle_x = math.cos(self.angle)
        self.angle_y = math.sin(self.angle)
        self.speed *= 1

    def update(self):
        self.x += self.speed*self.angle_x
        self.y -= self.speed*self.angle_y

        # Collision detection for edge of screen

        if self.y < 0: # If y coord of ball less than 0
            self.angle_y *= -1
            
        if self.y > 593: # If y coord of ball greater than 593
            self.angle_y *= -1
            
        if self.x < 0: # If x coord of ball less than 0
            Player2.score += 1
            self.reset()

        if self.x > 800: # If x coord of ball greater than 800
            Player1.score += 1
            self.reset()

        self.rect.x = self.x
        self.rect.y = self.y
       
 # Create instances of classes
Player1 = Paddle(75,275,WHITE)
Player2 = Paddle(718,275,WHITE)
ball = Ball(WHITE)

# Initialise sprites lists'
all_sprites_list = pygame.sprite.Group()
player1_list = pygame.sprite.Group()
player2_list = pygame.sprite.Group()
ball_list = pygame.sprite.Group()

# Add sprites to lists
all_sprites_list.add(Player1)
all_sprites_list.add(Player2)
all_sprites_list.add(ball)
player1_list.add(Player1)
player2_list.add(Player2)
ball_list.add(ball)
          
### MAIN LOOP ###

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_UP and Player2.rect.y > 0:
                Player2.paddle_y_speed = -speed
            elif event.key == pygame.K_DOWN and Player2.rect.y < 600:
                Player2.paddle_y_speed = speed
            elif event.key == pygame.K_a and Player1.rect.y > 0:
                Player1.paddle_y_speed = -speed
            elif event.key == pygame.K_z and Player1.rect.y < 600:
                Player1.paddle_y_speed = speed

        elif event.type == pygame.KEYUP:
            
            if event.key == pygame.K_UP:
                Player2.paddle_y_speed = 0
            elif event.key == pygame.K_DOWN:
                Player2.paddle_y_speed = 0
            elif event.key == pygame.K_a:
                Player1.paddle_y_speed = 0
            elif event.key == pygame.K_z:
                Player1.paddle_y_speed = 0
    
    # Collision detection between ball & paddles - increase the speed each turn by 1
    if pygame.sprite.spritecollide(ball,player1_list, False):
        ball.angle_x *= -1
        ball.speed += 0.5
        
    if pygame.sprite.spritecollide(ball,player2_list, False):
        ball.angle_x *= -1
        ball.speed += 0.5

    # Update sprites
    all_sprites_list.update()

    ### DRAWING STUFF ###

    # Clear screen
    screen.fill(BLACK)

    # Draw all sprites
    all_sprites_list.draw(screen)
    
    # Draw score
    Player1Score = myfont.render(str(Player1.score), 1, (WHITE))
    Player2Score = myfont.render(str(Player2.score), 1, (WHITE))
    screen.blit(Player1Score, (175, 10))
    screen.blit(Player2Score, (585, 10)) 

    # Flip screen
    pygame.display.flip()

    # Draw halfway line
    A=26
    n=-25
    for Num in range(A):
        n=n+25
        pygame.draw.rect(screen, WHITE,(400,n,3.25,20))
               
    # Update display
    pygame.display.update()

    # Check for Game Over
    if Player1.score == 10:
        player1_win = True
        print("Player 1 wins!")
        break
    elif Player2.score == 10:
        player2_win = True
        print("Player 2 wins!")
        break

    # Set FPS
    clock.tick(60)

# When main loop is finished, quit pygame
pygame.quit()
