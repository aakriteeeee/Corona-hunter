import pygame
import sys
import math
import random
from pygame import mixer

# Initialize Font
pygame.font.init()

#Load Audio Files
pygame.mixer.init(size=-16, channels=2)  # Initialize Sound Mixer
pygame.mixer.set_num_channels(16)  # Set channels to 16 from 8 to avoid sounds not playing
jump = pygame.mixer.Sound('jump.wav')
throw = pygame.mixer.Sound('throw.wav')
pygame.mixer.Sound.set_volume(jump, .2)  # Set Volume Lower
pygame.mixer.Sound.set_volume(throw, .2)  # Set Volume Lower
pygame.mixer.music.load('themesong.wav')  # Load in theme song


clock = pygame.time.Clock()

#title and icon
pygame.display.set_caption('Corona Hunter')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


# Screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png").convert_alpha()


class Player:
    def __init__(self):
        self.playerimg = pygame.image.load("doctor.png").convert_alpha()
        self.playerimg = pygame.transform.scale(self.playerimg, (150, 150))
        self.player_x = 50
        self.player_y = 400
        self.player_velocity = 3
        self.is_jump = False
        self.jump_count = 10
        self.score = 0  # Added score tracker to player object

    # Move player and limit boundary
    def move_player_in_screen(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.player_x < 720:
            self.player_x += 3
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.player_x -= 3

    # Jump
    def player_jump(self):
        keys = pygame.key.get_pressed()
        if not self.is_jump:
            if keys[pygame.K_SPACE]:
                self.is_jump = True
                jump.play()
        else:
            if self.jump_count >= -10:
                # jump formula
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.player_y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 10


class Corona_Virus():
    def __init__(self):
        self.index = 0
        self.coronaimg = []
        self.corona_pos_x = []
        self.corona_pos_y = []
        self.num_of_virus = 3
        self.corona_pos = 450
        self.corona_velocity = 1
        self.score = 0
        self.gameover = False

    def generate_corona(self, player):
        for i in range(self.num_of_virus):
            self.coronaimg.append(pygame.image.load("corona_virus.png").convert_alpha())
            self.corona_pos_x.append(random.randint(750, 900))
            self.corona_pos_y.append(self.corona_pos)
            self.corona_pos -= 90

        for i in range(corona.num_of_virus):
            corona.corona_pos_x[i] -= corona.corona_velocity
            screen.blit(corona.coronaimg[i], (corona.corona_pos_x[i], corona.corona_pos_y[i]))

        for i in range(corona.num_of_virus):
            # 2D distance formula --> square root ( (x2-x1)**2 + (y2-y1)**2 )
            distance = math.sqrt((corona.corona_pos_x[i] - vaccine.injection_x) ** 2 +
                                 (corona.corona_pos_y[i] - vaccine.injection_y) ** 2)
            player_distance = math.sqrt((corona.corona_pos_x[i] - player.player_x + 40) ** 2 +
                                        (corona.corona_pos_y[i] - player.player_y + 50) ** 2)

            # if player's position and vaccine position is lesser than 55
            if player_distance < 55:
                self.gameover = True

            # if machine throw is True than kill aliens
            if vaccine.throw is True:
                if distance < 40:
                    corona.corona_pos_y[i] = -500
                    screen.blit(corona.coronaimg[i], (corona.corona_pos_x[i], corona.corona_pos_y[i]))
                    self.score += 1
                    player.score += 1  # Increase player score by 1


    # if score hits 2 regenerate aliens at random position between 750-900
    def regenerate_corona(self):
        if corona.score // 3 == 1:
            self.score = 0
            self.corona_velocity += 0.4
            self.coronaimg = []
            self.corona_pos_x = []
            self.corona_pos_y = []
            self.corona_pos = 450
            for i in range(self.num_of_virus):
                self.coronaimg.append(pygame.image.load("corona_virus.png").convert_alpha())
                self.corona_pos_x.append(random.randint(750, 900))
                self.corona_pos_y.append(self.corona_pos)
                self.corona_pos -= 90

    # if corona's position is lesser than 20
    def corona_wins(self):
        for i in range(self.num_of_virus):
            if self.corona_pos_x[i] < 20:
                pygame.quit()
                sys.exit()


# Objects
player = Player()
corona = Corona_Virus()


class Vaccine:
    def __init__(self):
        self.injection = pygame.image.load("vaccine.png").convert_alpha()
        self.injection_x = player.player_x + 40
        self.injection_y = player.player_y + 50
        self.throw = False

    # throw vaccine
    def throw_vaccine(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.throw = True
            throw.play()

        # if vaccine is not thrown stick with the player
        if not self.throw:
            self.injection_x = player.player_x + 40
            self.injection_y = player.player_y + 50

        # if vaccine is thrown move the machine on x axis
        else:
            self.injection_x += 20
            if self.injection_x > 850:
                self.injection_x = player.player_x + 40
                self.injection_y = player.player_y + 50
                self.throw = False

# Death Screen
def death_screen(player):  # Pass in player object for access to final score

    #Death screen music start
    pygame.mixer.music.load('death_theme.wav')  # Load in death screen song
    pygame.mixer.music.play(-1)  # Start playing theme song
    pygame.mixer.music.set_volume(.2)

    # Fonts initialized
    death_font = pygame.font.SysFont('comicsans', 200)
    death_option_font = pygame.font.SysFont('comicsans', 65)
    death_label = death_font.render('You Lose...', True, (255, 0, 0))
    death_option = death_option_font.render('Press Q To Quit', True, (0, 0, 0))
    score_label = death_option_font.render(f'Final Score: {player.score}', True, (0, 0, 0))

    # Death Screen Loop
    running = True
    while running:
        clock.tick(80)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

        # Draw all text and background to screen
        screen.blit(background, (0, 0))
        screen.blit(death_label, (65, 200))
        screen.blit(death_option, (175, 350))
        screen.blit(score_label, (225, 75))
        pygame.display.update()


# Start Menu Loop
def start_menu():
    pygame.mixer.music.play(-1)  # Start playing theme song
    pygame.mixer.music.set_volume(.2)
    running = True
    title_font = pygame.font.SysFont('comicsans', 75)  # Create font object
    while running:
        screen.blit(background, (0, 0))  # Draw Background To Screen
        menu_label = title_font.render('Press Space To Start...', True, (255, 255, 255))  # Create Text Label
        screen.blit(menu_label, (130, 50))  # Draw Label To Screen
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # If space is pressed, start game
                    main_loop()  # Starts main_loop
                    pygame.mixer.music.stop()
                    death_screen(player)
                    running = False  # After main_loop (player loses), the game quits

vaccine = Vaccine()

def main_loop():
    # Main game loop
    while not corona.gameover:
        # Fps
        clock.tick(80)
        # Creating score tracker
        score_font = pygame.font.SysFont('comicsans', 75)
        score_tracker = score_font.render(f'Score: {player.score}', True, (255, 255, 255))
        # Handling Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        # screen blits
        screen.blit(background, (0, 0))
        screen.blit(vaccine.injection, (vaccine.injection_x, vaccine.injection_y))
        screen.blit(player.playerimg, (player.player_x, player.player_y))
        screen.blit(score_tracker, (15, 20))  # Draw score tracker to screen

        # Calling functions
        player.move_player_in_screen()
        player.player_jump()
        corona.generate_corona(player)
        vaccine.throw_vaccine()
        corona.regenerate_corona()
        corona.corona_wins()


        # refresh window
        pygame.display.update()


start_menu()  # Game starts from start menu, and the main_loop runs from within the start