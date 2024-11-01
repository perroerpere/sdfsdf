import pygame
import sys
import random



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

window_width = 1500
window_height = 1000

world_width = 5000
world_height = 5000



weather_active = False
wind_strength = 0  # Holder styrke for vinden
ground_slippery = False  # Om bakken er glatt (pga regn)

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Byggeplassen")
pygame.key.set_repeat(True)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.crouching = False

        self.image = pygame.Surface((25, 25))
        self.image.fill(black)
        self.rect = self.image.get_rect(center=(window_width / 2, window_height / 2))
        self.speed = 2
        self.gravity = 0.05
        self.vertical_speed = 0
        self.horizontal_jump_speed_right = 0
        self.horizontal_jump_speed_left = 0
        self.jump_strength = -6
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.grounded = False
        self.attached_to_wall = False  # Ny variabel for å sjekke om spilleren er festet til veggen
        self.using_parachute = False
        self.can_jump = True

        # Flytt variablene inn i Player-klassen
        self.player_on_right = False
        self.player_on_left = False
        self.player_on_top = False
        self.player_on_bottom = False

    def update(self):
        if self.grounded and self.attached_to_wall:
            if self.player_on_right:
                self.rect.x -= 1
                self.rect.y -= 1
                self.attached_to_wall = False
                self.player_on_right = False
            if self.player_on_left:
                self.rect.x += 1
                self.rect.y -= 1
                self.attached_to_wall = False
                self.player_on_left = False

        # Bruker de nye attributtene i stedet for globale variabler
        if wind_strength != 0 and not (self.grounded or self.attached_to_wall):
            self.rect.x += wind_strength

        if ground_slippery and (self.grounded or self.attached_to_wall):
            if self.moving_left:
                self.rect.x -= self.speed * 1.5  # Sklir litt ekstra til venstre
            elif self.moving_right:
                self.rect.x += self.speed * 1.5

        # om spilleren er intill en vegg
        if self.attached_to_wall:
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
            self.horizontal_jump_speed_right = 0
            self.horizontal_jump_speed_left = 0


        else:
            # Standard horisontal bevegelse
            if self.moving_right:
                self.rect.x += self.speed
            if self.moving_left:
                self.rect.x -= self.speed



        # Gravitasjon hvis ikke festet til vegg
        if not self.grounded and not self.attached_to_wall:
            # Sjekker om spilleren bruker paraplyen
            if self.using_parachute:
                self.vertical_speed = 1 # Senk farten med paraply
            else:
                self.vertical_speed += self.gravity
            self.rect.y += self.vertical_speed


        if self.horizontal_jump_speed_left or self.horizontal_jump_speed_right:

            # Momentum hvis Jump From Right Wall
            if self.horizontal_jump_speed_right and not self.horizontal_jump_speed_left:
                self.horizontal_jump_speed_right += self.gravity
                if self.horizontal_jump_speed_right <= 0:
                    #print(f"rightspeed: {self.horizontal_jump_speed_right}| attached: {self.attached_to_wall}| on right: {self.player_on_right}| on left: {self.player_on_left}")
                    self.rect.x += self.horizontal_jump_speed_right

            # Momentum hvis Jump From left Wall
            if self.horizontal_jump_speed_left and not self.horizontal_jump_speed_right:
                self.horizontal_jump_speed_left -= self.gravity
                if self.horizontal_jump_speed_left >= 0:
                    #print(f"leftspeed: {self.horizontal_jump_speed_left}| attached: {self.attached_to_wall}| on left: {self.player_on_left}| on right: {self.player_on_right}")
                    self.rect.x += self.horizontal_jump_speed_left
            else:
                pass


        # Gravitasjon høyere
        if not self.grounded and self.attached_to_wall and self.player_on_right:
            self.vertical_speed += self.gravity
            self.rect.x += self.vertical_speed

        # Gravitasjon venstere
        if not self.grounded and self.attached_to_wall and self.player_on_left:
            self.vertical_speed += self.gravity
            self.rect.x -= self.vertical_speed

        # Sjekk bunnkollisjon
        if self.rect.bottom >= window_height:
            self.rect.bottom = window_height
            self.vertical_speed = 0
            self.horizontal_jump_speed_right = 0
            self.horizontal_jump_speed_left = 0
            self.grounded = True
        else:
            self.grounded = False

    def movement(self, keys):
        self.moving_right = keys[pygame.K_d] and not self.attached_to_wall and self.rect.right < window_width
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

        if self.grounded or self.attached_to_wall:
            self.using_parachute = False

    def jump(self):
        if self.grounded:
            self.vertical_speed = self.jump_strength
            self.grounded = False
        elif self.attached_to_wall and self.can_jump:
            if self.player_on_right:
                self.horizontal_jump_speed_right = (self.jump_strength / 1)
            elif self.player_on_left:
                self.horizontal_jump_speed_left = -(self.jump_strength / 1)
            self.attached_to_wall = False  # Løsne fra veggen etter hopp

    def activate_parachute(self):
        if not self.grounded and not self.attached_to_wall:
            self.using_parachute = True



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, move_range=(0, 0), move_speed=0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((color))  # Fyll fargen rød (bruker RGB i stedet for variabelen red her)
        self.rect = self.image.get_rect(topleft=(x, y))

        # Bevegelsesrelaterte variabler
        self.move_range = move_range
        self.move_speed = move_speed
        self.direction = 1  # 1 = høyre, -1 = venstre
        self.start_x = x
        self.move_counter = 0

    def update(self):
        # Oppdater bevegelse
        if self.move_speed > 0 and self.move_counter > 5:
            # Sjekker om objektet er utenfor bevegelsesområdet
            if (self.rect.x > self.start_x + self.move_range[1] and self.direction > 0) or \
               (self.rect.x < self.start_x + self.move_range[0] and self.direction < 0):
                self.direction *= -1  # Bytt retning

            # Oppdater posisjon basert på hastighet og retning
            self.rect.x += self.move_speed * self.direction
            self.move_counter = 0
        elif self.move_speed > 0:
            self.move_counter += 1

    def check_collision(self, player):
        # Tilbakestill sideflag når spilleren ikke er festet til veggen
        if abs(player.vertical_speed) > 1:
            player.player_on_left = player.player_on_right = player.attached_to_wall = False
        if not player.attached_to_wall:
            player.player_on_left = player.player_on_right = False

        # Kollisjonslogikk for sidene
        if self.rect.colliderect(player.rect):
            player.using_parachute = False
            if player.rect.right > self.rect.left and player.rect.left < self.rect.left:
                player.rect.right = self.rect.left
                player.grounded = False
                player.attached_to_wall = True
                player.player_on_right = True
                player.vertical_speed = 0

            elif player.rect.left < self.rect.right and player.rect.right > self.rect.right:
                player.rect.left = self.rect.right
                player.grounded = False
                player.attached_to_wall = True
                player.player_on_left = True
                player.vertical_speed = 0

            elif player.rect.bottom > self.rect.top and player.rect.top < self.rect.top:
                player.rect.bottom = self.rect.top
                player.vertical_speed = 0
                player.grounded = True
                player.attached_to_wall = False
                player.player_on_top = True

            elif player.rect.top < self.rect.bottom and player.rect.bottom > self.rect.bottom:
                player.rect.top = self.rect.bottom
                player.vertical_speed = 0
                player.attached_to_wall = False
                player.player_on_bottom = True





def update_cycle(keys):
    player_sprite.update()
    player.movement(keys)
    for obstacle in obstacle_sprite:
        if isinstance(obstacle, Obstacle):  # Sikre at det er en Obstacle-instans
            obstacle.check_collision(player)
            obstacle.update()


def handle_weather():
    global wind_strength, ground_slippery, weather_active
    # Aktiver vær tilfeldig
    if not weather_active and random.randint(1, 2000) == 3001:  # TODO
        weather_active = True
        if random.choice(["wind", "rain"]) == "wind":
            wind_strength = random.choice([-1, 1]) * random.uniform(0.5, 2.0)
            print(f"Wind active! Strength: {wind_strength}")
        else:
            ground_slippery = True
            print("Rain active! Ground is slippery.")
    elif weather_active:
        # Fjern vær-effekt etter noen sekunder
        if random.randint(1, 5000) == 1:
            wind_strength = 0
            ground_slippery = False
            weather_active = False
            print("Weather cleared.")


# Initialiser spiller og hindringer
player = Player()
player_sprite = pygame.sprite.GroupSingle(player)

level1 = (
    Obstacle(color=red, width=500, height=50, x=700, y=700, move_range=(-500, 50), move_speed=1),
    Obstacle(color=maroon, width=50, height=900, x=100, y=200),
    Obstacle(color=blue, width=50, height=500, x=700, y=100),
    Obstacle(color=cyan, width=100, height=500, x=1000, y=100),
    Obstacle(color=lime, width=50, height=500, x=400, y=200),
    Obstacle(color=green, width=500, height=50, x=800, y=600),
    Obstacle(color=navy, width=50, height=50, x=1300, y=10),
    Obstacle(color=fuchsia, width=250, height=50, x=1000, y=800, move_range=(-500, 50), move_speed=2),
)
level2 = (
    Obstacle(color=blue, width=50, height=50, x=100, y=900),
    Obstacle(color=blue, width=50, height=50, x=666, y=806),
    Obstacle(color=blue, width=50, height=250, x=0, y=300),
    Obstacle(color=blue, width=250, height=50, x=258, y=171),
    Obstacle(color=blue, width=50, height=500, x=740, y=0),
    Obstacle(color=blue, width=150, height=50, x=970, y=330),
    Obstacle(color=blue, width=150, height=50, x=1200, y=180),
    Obstacle(color=blue, width=125, height=50, x=300, y=900, move_range=(-100, 100), move_speed=1),
    Obstacle(color=blue, width=125, height=50, x=300, y=600, move_range=(-100, 100), move_speed=1),
    Obstacle(color=blue, width=125, height=50, x=840, y=575, move_range=(-100, 100), move_speed=1),

)
level3 = (
    Obstacle(color=blue, width=50, height=350, x=100, y=100),
    Obstacle(color=blue, width=50, height=350, x=100, y=650),
    Obstacle(color=blue, width=50, height=350, x=400, y=100),
    Obstacle(color=blue, width=50, height=350, x=400, y=650),
    Obstacle(color=blue, width=50, height=350, x=700, y=100),
    Obstacle(color=blue, width=50, height=350, x=700, y=650),
    Obstacle(color=blue, width=50, height=350, x=1000, y=100),
    Obstacle(color=blue, width=50, height=350, x=1000, y=650),
    Obstacle(color=blue, width=50, height=350, x=1300, y=100),
    Obstacle(color=blue, width=50, height=350, x=1300, y=650),
)


obstacle_sprite = pygame.sprite.Group(level1)


# Hovedspilleløkken
def game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("space")
                player.jump()
                player.can_jump = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                print("spacedog")
                player.can_jump = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # Ny knapp for å aktivere paraplyen
                player.activate_parachute()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                print(mx, my)

        keys = pygame.key.get_pressed()
        update_cycle(keys)

        handle_weather()


        # Tegn alt
        screen.blit(background, (0, 0))
        player_sprite.draw(screen)
        obstacle_sprite.draw(screen)
        pygame.display.flip()

game()