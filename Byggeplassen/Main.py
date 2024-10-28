import pygame
import sys
import random
import math

from pygame.examples.sprite_texture import sprite

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
lime = (0, 255, 0)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
fuchsia = (255, 0, 255)
silver = (192, 192, 192)
gray = (128, 128, 128)
maroon = (128, 0, 0)
olive = (128, 128, 0)
purple = (128, 0, 128)
teal = (0, 128, 128)
navy = (0, 0, 128)

background = pygame.image.load("GameBackground.jpg")

width = 1500
height = 1000

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Byggeplassen")
pygame.key.set_repeat(True)

player_on_ass = 0
player_on_head = 0
player_on_right = 0
player_on_left = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25,25))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.speed = 2

        self.gravity = 0.05
        self.vertical_speed = 0
        self.jump_strenght = -7

        self.moving_right = False
        self.moving_left = False
        self.is_on_ground = False


    def update(self):
        if not player_on_left or player_on_right:
            if self.moving_right:
                self.rect.x += self.speed
            if self.moving_left:
                self.rect.x -= self.speed



        if player_on_right:
            if self.moving_right:
                self.rect.y -= self.speed
            if self.moving_left:
                self.rect.y += self.speed


        if player_on_left:
            if self.moving_right:
                self.rect.y += self.speed
            if self.moving_left:
                self.rect.y -= self.speed

        if not self.is_on_ground:
            self.vertical_speed += self.gravity
            self.rect.y += self.vertical_speed
        if self.rect.bottom >= height:
            self.rect.bottom = height
            self.vertical_speed = 0
            self.is_on_ground = True


        else:
            self.is_on_ground = False

        if pygame.sprite.spritecollide(self, obstacle_sprite,False):
            self.is_on_ground = True



    def movement(self,keys):
        if keys[pygame.K_d] and self.rect.right < width:
            player.moving_right = True
        else:
            player.moving_right = False

        if keys[pygame.K_a] and self.rect.x > -10:
            player.moving_left = True
        else:
            player.moving_left = False

        if keys[pygame.K_w] and self.rect.y > -10:
            player.moving_up = True
        else:
            player.moving_up = False

        if keys[pygame.K_s] and self.rect.y < height -10:
            player.moving_down = True
        else:
            player.moving_down = False

    def jump(self):
        if self.is_on_ground:
            self.vertical_speed = self.jump_strenght
            self.is_on_ground = False


    def get_pos(self):
        return self.rect.x, self.rect.y


player_sprite = pygame.sprite.Group()
player = Player()
player_sprite.add(player)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, width, height, screen_width, screen_height):
        super().__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = screen_height
        self.rect.y = screen_width

    def update(self):
        if pygame.sprite.spritecollide(self, player_sprite, False):
            if player.rect.bottom > self.rect.top and player.rect.top < self.rect.top:
                print("hei")
            if player.rect.left == self.rect.right:
                global player_on_left
                player_on_left = True





def updatescycle(keys):
    player_sprite.update()
    player.update()
    player.movement(keys)
    obstacle_sprite.update()



obstacle_sprite = pygame.sprite.Group()
obstacle_1 = Obstacle(500,50,600,600)
obstacle_2 = Obstacle(50,500, 100,200)
obstacle_sprite.add(obstacle_1)
obstacle_sprite.add(obstacle_2)

def game():
    game = True
    while game:
        player_x, player_y = player.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        keys = pygame.key.get_pressed()




        updatescycle(keys)
        screen.blit(background, (0, 0))
        player_sprite.draw(screen)
        obstacle_sprite.draw(screen)
        pygame.display.flip()



game()