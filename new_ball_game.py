import sys

import pygame

RED = (255, 0, 0)

WIDTH, HEIGHT = (550, 600)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG_img = pygame.image.load('img/BG.jpg').convert_alpha()
BG = pygame.transform.scale(BG_img, (550, 600))

pygame.init()

# define color
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)


class Ball(pygame.sprite.Sprite):  # sprite module
    def __init__(self, pos_x, pos_y, move_x, move_y, paddles,
                 hit_player):  # the position x and y of Ball, image path of ball
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('img/1.png').convert_alpha())
        self.sprites.append(pygame.image.load('img/2.png').convert_alpha())
        self.sprites.append(pygame.image.load('img/3.png').convert_alpha())
        self.sprites.append(pygame.image.load('img/4.png').convert_alpha())
        self.sprites.append(pygame.image.load('img/5.png').convert_alpha())
        self.sprites.append(pygame.image.load('img/6.png').convert_alpha())
        self.sprites.append(pygame.image.load('img/7.png').convert_alpha())
        self.sprites.append(pygame.image.load('img/8.png').convert_alpha())
        self.sprites.append(pygame.image.load('img/9.png').convert_alpha())
        self.sprites.append(pygame.image.load('img/10.png').convert_alpha())
        self.sprites.append(pygame.image.load('img/11.png').convert_alpha())
        self.sprites.append(pygame.image.load('img/12.png').convert_alpha())
        self.present_sprite = 0
        self.image = self.sprites[self.present_sprite]  # the image = self.sprite(present_sprite initial value is zero]
        for x in self.sprites:
            x.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # rect is to get to the rectangle of image
        self.rect.center = [pos_x, pos_y]  # rect.center  = x, y
        self.move_x = move_x
        self.move_y = move_y
        self.paddles = paddles
        self.hit_player = hit_player
        self.score_count = 0

    def update(self):
        self.present_sprite += 0.4
        if self.present_sprite >= len(self.sprites):
            self.present_sprite = 0
        self.image = self.sprites[int(self.present_sprite)]

        self.rect.x += self.move_x
        self.rect.y += self.move_y
        self.collision()

    def collision(self):
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.move_y *= -1
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.move_x *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            paddle_colli = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.right - paddle_colli.left) < 30 and self.move_x > 0:
                self.move_x *= -1
            if abs(self.rect.left - paddle_colli.right) < 30 and self.move_x < 0:
                self.move_x *= -1
            if abs(self.rect.top - paddle_colli.bottom) < 30 and self.move_y < 0:
                self.move_y *= -1
            if abs(self.rect.bottom - paddle_colli.top) < 30 and self.move_y > 0:
                self.move_y *= -1

        if pygame.sprite.spritecollide(self, self.hit_player, False):
            if self.score_count == 3 and self.score_count <= 5:
                self.move_x *= 2
                self.move_y *= 2
            paddle_colli = pygame.sprite.spritecollide(self, self.hit_player, False)[0].rect
            pygame.mixer.Sound.play(hit_player_sound)
            if abs(self.rect.right - paddle_colli.left) < 30 and self.move_x > 0:
                self.move_x *= -1
            if abs(self.rect.left - paddle_colli.right) < 30 and self.move_x < 0:
                self.move_x *= -1
            if abs(self.rect.top - paddle_colli.bottom) < 30 and self.move_y < 0:
                self.move_y *= -1
                self.score_count += 1
            if abs(self.rect.bottom - paddle_colli.top) < 30 and self.move_y > 0:
                self.move_y *= -1


class Brick(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('img/paddle.png').convert_alpha()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))


class Paddle(Brick):
    def __init__(self, pos_x, pos_y, x_move):
        super().__init__(pos_x, pos_y)
        self.x_move = x_move

    def update(self):
        self.rect.x += self.x_move
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.x_move *= -1


class Player(Brick):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.score_count = 0
        self.level_count = 0

    def update(self):
        self.level()
        self.draw_score()

    def level(self):
        if pygame.sprite.spritecollide(self, ball_group, False):
            self.score_count += 1
            self.level_count += 1
            if self.level_count == 2 and self.level_count <= 6:
                self.image = pygame.transform.scale(pygame.image.load('img/paddle.png').convert_alpha(), (90, 40))
                self.image.set_colorkey(WHITE)
                self.rect = self.image.get_rect(center=(WIDTH / 2, HEIGHT - 10))

    def draw_score(self):
        score_font = pygame.font.SysFont("Arial.ttf", 40, bold=False)
        font_text = score_font.render(f"Score:{self.score_count}", True, WHITE)
        WIN.blit(font_text, font_text.get_rect(x=10, y=10))


pygame.mixer.init()
hit_player_sound = pygame.mixer.Sound("img/BounceYoFrankie.flac")
hit_player_sound.set_volume(0.1)

player = Player(200, HEIGHT - 10)
player_group = pygame.sprite.Group()
player_group.add(player)

paddle_1 = Paddle(WIDTH / 2, 300, 3)
paddle_2 = Paddle(WIDTH / 2, 100, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(paddle_1, paddle_2)

ball_group = pygame.sprite.Group()  # add to sprite group of pygame
ball = Ball(300, 200, 4, 4, paddle_group, player_group)  # x = the image path
ball_group.add(ball)  # add ball in the group

clock = pygame.time.Clock()

Run = True
while Run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    Keys = pygame.key.get_pressed()
    if Keys[pygame.K_LEFT] and player.rect.left > 0:
        player.rect.x -= 10
    if Keys[pygame.K_RIGHT] and player.rect.right < WIDTH:
        player.rect.x += 10

    WIN.blit(BG, (0, 0))
    ball_group.draw(WIN)
    ball_group.update()
    paddle_group.draw(WIN)
    paddle_group.update()
    player_group.draw(WIN)
    player_group.update()
    clock.tick(60)
    pygame.display.update()
