# ballGame
from typing import Union

import pygame                                      # so that we can use any object or method etc. that can be pygame.XXX
import sys                                         # so that we can use any object or methods etc. that can sys.XXX like sys.exit()
from pygame.locals import *

# initialize pygame
from pygame.surface import Surface, SurfaceType

pygame.init()                                      # initialize all objects of pygame before we use it

# define colors                                    # (red, green, blue)
BLACK = (0, 0, 0)

# create window
pygame.display.set_caption("My First Game")        # set our caption at the top of display
WIDTH = 650                                        # Declare that WIDTH is the width of our window
HEIGHT = 630                                       # Declare that HEIGHT is the height of our window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))     # Use WIDTH and HEIGHT above to set our window size
BG = pygame.image.load('img/BG.jpg').convert()     # load our background into our game

# define ball
BALL = pygame.image.load('img/pokemon_ball.png').convert()      # load our ball into our game
BALL.set_colorkey(BLACK)                           # ignore the yellow on the ball
BallRrect = BALL.get_rect()                        # get the rectangle of the ball let us control and determine the ball
Move = [3, 6]                                      # define where and how the ball moves ([x,y])
Speed = pygame.time.Clock()                        # Declare speed that to keep our game looping correctly

# define bat
PADDLE = pygame.Surface([100, 20])                 # define the surface of our paddle
PADDLE.fill([255, 255, 0])                         # fill the paddle with full color of yellow
PADDLE_position = PADDLE.get_rect(x=200, y=570)    # initialize the position of our paddle

# define a wall
WALL = pygame.Surface([200, 20])
WALL.fill([70, 200, 100])
WALL_position = WALL.get_rect(center=WIN.get_rect().center)

Count = 0                                          # count is to count the number of times the ball hits the paddle and initialize it before our game loop
status = "Playing"
# Game loop
Run = True                                         # if Run = False then the game will end
while Run:
    # keep loop running at the right speed
    Speed.tick(60)
    # Process input (events)
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    font = pygame.font.SysFont("arial", 30, bold = True)       # declare font is fond arial font that size is 30 and not bold
    text = font.render(f"Level: {Count}", True, (255, 255, 255))# declare text is (font.render(): calculating what pattern of pixels is needed (True means Anti-aliasing))

    Keys = pygame.key.get_pressed()                             # the Keys is to get any pressed key from board keys

    if status == 'Playing':

        if Keys[pygame.K_LEFT] and PADDLE_position.left > 0:        # when we press the left key and the paddle is in the window
            PADDLE_position.x -= 10                                 # then the paddle will move -10 pixel

        if Keys[pygame.K_RIGHT] and PADDLE_position.right < WIDTH:  # when we press the right key and the paddle is in the window
            PADDLE_position.x += 10                                 # then the paddle will move 10 pixel

        if PADDLE_position.colliderect(BallRrect):                  # if the paddle hits the ball (check their rectangle)
            Move[1] *= -1                                           # the ball will bounce
            Count +=1                                               # and the count that is the paddle hits the ball will plus one

        BallRrect = BallRrect.move(Move)                            # the ball rect follows the movement of ball rect to move, which is based on the movement of the ball

        if BallRrect.left < 0 or BallRrect.right > WIDTH:           # if the rect of our ball exceeds the width of our window
            Move[0] = -Move[0]                                      # the X axis of ball will bounce

        if BallRrect.top < 0: # 更改為球的頂部(top)碰撞到Y軸的時候         # if the rect of ball exceeds the height of our window
            Move[1] = -Move[1]                                      # the Y axis of ball will bounce

        if BallRrect.bottom > HEIGHT:# 球的底部碰到HEIGHT的時候
            status = "Lose"# 判定遊戲結束

    # draw / render
    WIN.blit(BG, (0, 0))       # 畫出背景,位置 X=0 Y=0            # set our background onto the window copied from X=0, Y=0
    WIN.blit(BALL, BallRrect)  # 畫出球,畫球的長方形               # set our ball onto the window copied from the rect of the ball
    WIN.blit(PADDLE, PADDLE_position) # 畫出球拍、位置            # set our paddle onto the window copied from the rect of the paddle
    WIN.blit(text, text.get_rect(x=10, y=10))                   # set the text from the rect of the text onto our WIN
    WIN.blit(WALL, WALL_position)
    if status == "Lose":
        text = font.render(("GAME OVER"), True, (255, 255, 255))
        WIN.blit(text, text.get_rect(center=WIN.get_rect().center))
    # 視窗.blit(字, 字的方形(中心位置=視窗.get().center))
    # *after* drawing everything, flip the display
    pygame.display.update()    # =flip() 更新畫面(重複畫圖)，直到主動結束