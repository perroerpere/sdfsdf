import pygame
import sys
import random
import math



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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(black)
        self.rect = self.image.get_rect(center=(width / 2, height / 2))
        self.speed = 2
        self.gravity = 0.05
        self.vertical_speed = 0
        self.jump_strength = -7
        self.wall_jump_strength = 5  # Horisontal hoppstyrke fra veggen
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.grounded = False
        self.attached_to_wall = False  # Ny variabel for å sjekke om spilleren er festet til veggen
        self.horizontal_jump = 1

        # Flytt variablene inn i Player-klassen
        self.player_on_right = False
        self.player_on_left = False
        self.player_on_top = False
        self.player_on_bottom = False

    def update(self):
        # Bruker de nye attributtene i stedet for globale variabler
        if self.attached_to_wall:
            # Bevegelse opp/ned basert på hvilken vegg spilleren er festet til
            if self.player_on_right:
                if self.moving_up:
                    self.rect.y += self.speed
                elif self.moving_down:
                    self.rect.y -= self.speed
            elif self.player_on_left:
                if self.moving_up:
                    self.rect.y += self.speed
                elif self.moving_down:
                    self.rect.y -= self.speed
        else:
            # Standard horisontal bevegelse
            if self.moving_right:
                self.rect.x += self.speed
            if self.moving_left:
                self.rect.x -= self.speed



        # Gravitasjon hvis ikke festet til vegg
        if not self.grounded and not self.attached_to_wall:
            self.vertical_speed += self.gravity
            self.rect.y += self.vertical_speed


        # Gravitasjon høyere
        if not self.grounded and self.attached_to_wall and self.player_on_right:
            self.vertical_speed += self.gravity
            self.rect.x += self.vertical_speed

        # Gravitasjon venstere
        if not self.grounded and self.attached_to_wall and self.player_on_left:
            self.vertical_speed += self.gravity
            self.rect.x -= self.vertical_speed

        # Sjekk bunnkollisjon
        if self.rect.bottom >= height:
            self.rect.bottom = height
            self.vertical_speed = 0
            self.grounded = True
        else:
            self.grounded = False

    def movement(self, keys):
        self.moving_right = keys[pygame.K_d] and not self.attached_to_wall and self.rect.right < width
        self.moving_left = keys[pygame.K_a] and not self.attached_to_wall and self.rect.left > 0

        # Tillat vertikal bevegelse når festet til vegg
        if self.attached_to_wall:
            if self.player_on_left:  # Når spilleren er festet til venstre vegg
                self.moving_up = keys[pygame.K_d]  # Bruk d for opp
                self.moving_down = keys[pygame.K_a]  # Bruk a for ned
            elif self.player_on_right:  # Når spilleren er festet til høyre vegg
                self.moving_up = keys[pygame.K_a]  # Bruk a for opp
                self.moving_down = keys[pygame.K_d]  # Bruk d for ned
        else:
            self.moving_up = False
            self.moving_down = False

    def jump(self):
        if self.grounded:
            self.vertical_speed = self.jump_strength
            self.grounded = False
        elif self.attached_to_wall:
            #self.horizontal_jump = 10
            if self.player_on_right:
                self.vertical_speed = self.jump_strength
                self.rect.x -= self.wall_jump_strength
            elif self.player_on_left:
                self.vertical_speed = self.jump_strength
                self.rect.x += self.wall_jump_strength
            self.attached_to_wall = False  # Løsne fra veggen etter hopp



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(red)
        self.rect = self.image.get_rect(topleft=(x, y))

    def check_collision(self, player):
        # Bare tilbakestill sideflag når spilleren ikke er festet til veggen

        if abs(player.vertical_speed) > player.horizontal_jump :
            player.player_on_left = player.player_on_right = player.attached_to_wall = False
        if not player.attached_to_wall:
            player.player_on_left = player.player_on_right = False

        # Kollisjonslogikk for sidene
        if self.rect.colliderect(player.rect):
            if player.rect.right > self.rect.left and player.rect.left < self.rect.left:
                player.rect.right = self.rect.left
                player.grounded = False #TODO
                player.attached_to_wall = True  # Fest til vegg
                player.player_on_right = True
                player.vertical_speed = 0

            elif player.rect.left < self.rect.right and player.rect.right > self.rect.right:
                player.rect.left = self.rect.right
                player.grounded = False #TODO
                player.attached_to_wall = True  # Fest til vegg
                player.player_on_left = True
                player.vertical_speed = 0

            elif player.rect.bottom > self.rect.top and player.rect.top < self.rect.top:
                player.rect.bottom = self.rect.top
                player.vertical_speed = 0
                player.grounded = True
                player.attached_to_wall = False  # Ikke fest til vegg på toppen
                player.player_on_top = True

            elif player.rect.top < self.rect.bottom and player.rect.bottom > self.rect.bottom:
                player.rect.top = self.rect.bottom
                player.vertical_speed = 0
                player.attached_to_wall = False  # Ikke fest til vegg på bunnen
                player.player_on_bottom = True



def update_cycle(keys):
    player_sprite.update()
    player.movement(keys)
    for obstacle in obstacle_sprite:
        if isinstance(obstacle, Obstacle):  # Sikre at det er en Obstacle-instans
            obstacle.check_collision(player)

# Initialiser spiller og hindringer
player = Player()
player_sprite = pygame.sprite.GroupSingle(player)
obstacle_sprite = pygame.sprite.Group(
    Obstacle(500, 50, 600, 600),
    Obstacle(50, 500, 100, 200),
    Obstacle(50, 500, 400, 200)
)

# Hovedspilleløkken
def game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.jump()

        keys = pygame.key.get_pressed()
        update_cycle(keys)


        # Tegn alt
        screen.blit(background, (0, 0))
        player_sprite.draw(screen)
        obstacle_sprite.draw(screen)
        pygame.display.flip()

game()