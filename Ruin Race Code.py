##########INFO##########
#####BACKSTORY#####
#Ruin Race is a platformer-style vertical scrolling game where the main objective
#is to avoid the liquid at the bottom of the screen. The liquid, along with
#projectiles that make the game suprisingly difficult. The end goal
#is to stay alive, and rescue your friend at the top of the volcano.
#######GUIDE#######
#Use W, A, and D to move up, left and right, respectively, for player 1.
#Use the up arrow, the left arrow and the right arrow, to move up, left and right, respectively, for player 2.
#Hit escape to exit the game or to go back.
#Jump on obstacles above you to keep from drowning.
#Powerups give you a temporary boost of some sort.
#####POWERUPS######
#Bullet/Fireball Invincibility [Common] - No bullets or fireballs can hurt you for 10 seconds.
#Player Speed Up [Uncommon] - Increases the player’s walk speed by 50% for 10 seconds.
#Health Restore [Uncommon] - Sets the player’s health back to 100%
#Ghost Platform [Rare] - This makes it possible for players to jump under the platform and appear on top, like Doodle Jump for 6 seconds.
#Lava Freeze [Rare] - Freezes the scrolling down motion of the game for 4 seconds.
#Orb of the Volcano Master [Legendary] - Teleports you to a mini-game where you try to rescue your lost friend from the evil lava monster.
########################

# IMPORTING AND INITIALIZING
import pygame, sys, random, pickle, threading, time
from pygame.locals import *
pygame.init()
pygame.mixer.init()
print("Booted pygame at: " + str(pygame.time.get_ticks()) + "ms")
# BONUS FEATURES (HACKS)
## WARNING: Changing any of these features will disable high-scores
cap_fps = True # Set this to false to uncap the FPS (otherwise capped at 30) - Default: True
spawn_platforms = True # Set this to false to stop spawning platforms - Default: True
spawn_more_powerups = False # Set this to true to spawn powerups at 10x the normal rate - Default: False
disable_liquids = False # Set this to true to become invincible to all liquids - Default: False
disable_projectiles = False # Set this to true to stop spawning projectiles on the screen - Default: False
increase_speed = False # Set this to true to give both players a 2x speed bonus - Default: False
instant_boss = False # Set this to true to go to the boss fight directly - Default: False
# VARIABLES NEEDED TO MAKE LOADING SCREEN
SCREEN = pygame.display.set_mode((640, 480))
CLOCK = pygame.time.Clock()
ULTRATINYFONT = pygame.font.Font("freesansbold.ttf", 16)
TINYFONT = pygame.font.Font("freesansbold.ttf", 24)
SMALLFONT = pygame.font.Font("freesansbold.ttf", 32)
MEDIUMFONT = pygame.font.Font("freesansbold.ttf", 48)
LARGEFONT = pygame.font.Font("freesansbold.ttf", 64)
print("Booted pre-loading screen variables at: " + str(pygame.time.get_ticks()) + "ms")
# MAKING A LOADING SCREEN
start_time = CLOCK.tick()
DUMMY_LOAD = pygame.mixer.Sound("ElectricTricks.mp3")
DUMMY_LOAD = pygame.image.load("boss0.png")
DUMMY_LOAD = pygame.image.load("volcanobg.png")
end_time = CLOCK.tick()
LOADING_QUOTIENT = 13
current_load = "Loading Screen"
load_amount = 0
time_taken = (end_time - start_time)
BOOT_TIME = round(pygame.time.get_ticks())
estimated_time = round((time_taken * LOADING_QUOTIENT)/1000 + BOOT_TIME/1000, 3)
print("Booted loading screen at " + str(BOOT_TIME) + "ms")
def loading(current_load, load_amount):
    SCREEN.blit(DUMMY_LOAD, (0, 0))
    if estimated_time == 1:
        text = SMALLFONT.render("Estimated load time: 1 second", False, (255, 55, 55))
        SCREEN.blit(text, (20, 20))
    else:
        text = SMALLFONT.render("Estimated load time: " + str(estimated_time) + " seconds", False, (255, 55, 55))
        SCREEN.blit(text, (20, 20))
    text2 = ULTRATINYFONT.render("Currently Loading: " + current_load, False, (255, 55, 55))
    SCREEN.blit(text2, (20, 60))
    text3 = SMALLFONT.render("Loading: " + str(round(load_amount/13 * 100)) + "%", False, (255, 55, 55))
    SCREEN.blit(text3, (390, 430))
    BAR_WIDTH = int(180 * load_amount / 13)
    pygame.draw.rect(SCREEN, (255, 55, 55), pygame.Rect(395, 400, BAR_WIDTH, 20))
    load_string = ""
    for i in range(load_amount):
        load_string += "-"
    for i in range(13 - load_amount):
        load_string += " "
    print(str(load_amount) + "/13 - " + str(round(load_amount/13 * 100)) + "% " + "[" + load_string + "] at " + str(pygame.time.get_ticks()) + "ms: " + current_load)
    pygame.display.update()
# CONSTANT VARIABLES
current_load = "Variables"
load_amount += 1
threading.Thread(target = loading(current_load, load_amount)).start()
FPS = 30
GRAVITY = 20
EASY_SCROLL_SPEED = 2
NORMAL_SCROLL_SPEED = 2.75
HARD_SCROLL_SPEED = 3.5
CREDITS_SCROLL_SPEED = 1
WALK_SPEED = 6
JUMP_POWER = 48
ARCADE_MODE = False
WATER_DAMAGE = 1
ACID_DAMAGE = 1.5
LAVA_DAMAGE = 2.5
BULLET_DAMAGE = 15
FIREBALL_DAMAGE = 35
EASY_PLATFORM_GAP = 6
NORMAL_PLATFORM_GAP = 5
HARD_PLATFORM_GAP = 4
NORMAL_PROJECTILE_RARITY = 240
HARD_PROJECTILE_RARITY = 160
BOSS_FIREBALL_RARITY = 12
ARCADE_CURSOR_SPEED = 5
if spawn_more_powerups == False:
    speed_rarity = 900
    health_rarity = 1500
    orb_rarity = 15000
    ghost_rarity = 2700
    projectile_proof_rarity = 600
    freeze_rarity = 2400
else:
    speed_rarity = 90
    health_rarity = 150
    orb_rarity = 1500
    ghost_rarity = 270
    projectile_proof_rarity = 60
    freeze_rarity = 240
EASY_SAVE_FILE = "easysave.txt"
NORMAL_SAVE_FILE = "normalsave.txt"
HARD_SAVE_FILE = "hardsave.txt"
NUMBER_OF_WINS_SAVE_FILE = "winssave.txt"
VERSION = "4.0"
# CHANGING VARIABLES
mouse_x = 0
mouse_y = 0
player_health = 100
rescue_health = 100
rescue_y = 200
boss_health = 10000
boss_y = 150
points = 0
game_mode = "pregame"
if instant_boss == True:
    game_mode = "rescue"
difficulty = ""
credits_y = 0
info_y = 0
liquid_y = 360
liquid_cycle = 1
frame_index = 0
points_active = False
can_play_drowning = True
one_has_died = False
initial_blit = False
speed_index = 0
ghost_index = 0
projectile_proof_index = 0
platforms_scrolling_index = 0
speed_up = False
ghost_on = False
projectile_proof = False
platforms_scrolling = True
left_click = False
cursor_mode = False
arcade_hit = False
game_over = False
if cap_fps == True and spawn_platforms == True and spawn_more_powerups == False and disable_liquids == False and disable_projectiles == False and increase_speed == False and instant_boss == False:
    high_scores = True
else:
    high_scores = False
last_platform_y = 100
hit_cooldown = 0
pregame_stage = 0
number_of_wins = 0
frame_rate = 30
start_time = time.time()
frame_rate_delay = 0.5
counter = 0
easy_score_list = []
normal_score_list = []
hard_score_list = []
platform_list = []
projectile_list = []
powerup_list = []
# SOUNDTRACK LOADS
current_load = "Soundtracks"
load_amount += 1
threading.Thread(target = loading(current_load, load_amount)).start()
MAIN_MUSIC = pygame.mixer.Sound("ElectricTricks.mp3")
GRASSLAND_MUSIC = pygame.mixer.Sound("MayMeadows.mp3")
FACILITY_MUSIC = pygame.mixer.Sound("GlitchWave.mp3")
VOLCANO_MUSIC = pygame.mixer.Sound("Takedown.mp3")
PREGAME_MUSIC = pygame.mixer.Sound("RoadToJustice.mp3")
ENDING_MUSIC = pygame.mixer.Sound("Endzone.mp3")
CREDITS_MUSIC = pygame.mixer.Sound("TheFinalFrontier.mp3")
# SOUND EFFECT LOADS
current_load = "Sound Effects"
load_amount += 1
threading.Thread(target = loading(current_load, load_amount)).start()
BUTTON_CLICKED = pygame.mixer.Sound("button_click.wav")
DROWNING = pygame.mixer.Sound("drowning.wav")
POWERUP = pygame.mixer.Sound("powerup.wav")
YOU_WIN = pygame.mixer.Sound("you_win.wav")
PROJECTILE_FIRE = pygame.mixer.Sound("projectile_fire.wav")
PROJECTILE_HIT = pygame.mixer.Sound("projectile_hit.wav")
# SPRITE LOADS
current_load = "Sprites"
load_amount += 1
threading.Thread(target = loading(current_load, load_amount)).start()
freeze0 = pygame.image.load("freeze0.png")
freeze1 = pygame.image.load("freeze1.png")
freeze2 = pygame.image.load("freeze2.png")
freeze3 = pygame.image.load("freeze3.png")
ghost0 = pygame.image.load("ghost0.png")
ghost1 = pygame.image.load("ghost1.png")
ghost2 = pygame.image.load("ghost2.png")
ghost3 = pygame.image.load("ghost3.png")
orb0 = pygame.image.load("orb0.png")
orb1 = pygame.image.load("orb1.png")
orb2 = pygame.image.load("orb2.png")
orb3 = pygame.image.load("orb3.png")
projectileproof0 = pygame.image.load("projectileproof0.png")
projectileproof1 = pygame.image.load("projectileproof1.png")
projectileproof2 = pygame.image.load("projectileproof2.png")
projectileproof3 = pygame.image.load("projectileproof3.png")
speed0 = pygame.image.load("speed0.png")
speed1 = pygame.image.load("speed1.png")
speed2 = pygame.image.load("speed2.png")
speed3 = pygame.image.load("speed3.png")
health0 = pygame.image.load("health0.png")
health1 = pygame.image.load("health1.png")
health2 = pygame.image.load("health2.png")
health3 = pygame.image.load("health3.png")
playerone0 = pygame.image.load("playerone0.png")
playerone1 = pygame.image.load("playerone1.png")
playerone2 = pygame.image.load("playerone2.png")
playertwo0 = pygame.image.load("playertwo0.png")
playertwo1 = pygame.image.load("playertwo1.png")
playertwo2 = pygame.image.load("playertwo2.png")
boss0 = pygame.image.load("boss0.png")
boss1 = pygame.image.load("boss1.png")
deadboss = pygame.image.load("bossdead.png")
bulletleft = pygame.image.load("bulletleft.png")
bulletright = pygame.image.load("bulletright.png")
fireballleft0 = pygame.image.load("fireballleft0.png")
fireballleft1 = pygame.image.load("fireballleft1.png")
fireballleft2 = pygame.image.load("fireballleft2.png")
fireballright0 = pygame.image.load("fireballright0.png")
fireballright1 = pygame.image.load("fireballright1.png")
fireballright2 = pygame.image.load("fireballright2.png")
water_image = pygame.image.load("water.png")
acid_image = pygame.image.load("acid.png")
lava_image = pygame.image.load("lava.png")
grasslandplatform = pygame.image.load("grasslandplatform.png")
facilityplatform = pygame.image.load("facilityplatform.png")
volcanoplatform = pygame.image.load("volcanoplatform.png")
# BACKGROUND LOADS
current_load = "Backgrounds"
load_amount += 1
threading.Thread(target = loading(current_load, load_amount)).start()
game_over_screen = pygame.image.load("game_over.png")
player_won_screen = pygame.image.load("player_won.png")
grasslandbg = pygame.image.load("grasslandbg.png")
facilitybg = pygame.image.load("facilitybg.png")
volcanobg = pygame.image.load("volcanobg.png")
volcanohit0 = pygame.image.load("volcanohit0.png")
volcanohit1 = pygame.image.load("volcanohit1.png")
infocard = pygame.image.load("infocard.png")
credits_image = pygame.image.load("credits.png")
menuscreen = pygame.image.load("menuscreen.png")
menuscreenplay1 = pygame.image.load("menuscreenplay1.png")
menuscreenplay2 = pygame.image.load("menuscreenplay2.png")
menuscreencredits = pygame.image.load("menuscreencredits.png")
menuscreeninfo = pygame.image.load("menuscreeninfo.png")
diffscreen = pygame.image.load("diffscreen.png")
diffscreeneasy = pygame.image.load("diffscreeneasy.png")
diffscreennormal = pygame.image.load("diffscreennormal.png")
diffscreenhard = pygame.image.load("diffscreenhard.png")
# CHANGING SOME SETTINGS
current_load = "System Settings"
load_amount += 1
threading.Thread(target = loading(current_load, load_amount)).start()
pygame.display.set_caption("Ruin Race V" + str(VERSION))
pygame.display.set_icon(playerone0)
if ARCADE_MODE == True:
    pygame.mouse.set_visible(False)
# LOADING SAVE FILES
current_load = "Saved Data"
load_amount += 1
threading.Thread(target = loading(current_load, load_amount)).start()
try:
    with open(EASY_SAVE_FILE, "rb") as file:
        loaded_content = pickle.load(file)
    for score in loaded_content:
        easy_score_list.append(score)
except:
    easy_score_list.append(0)
    with open(EASY_SAVE_FILE, "wb"):
        pass
try:    
    with open(NORMAL_SAVE_FILE, "rb") as file:
        loaded_content = pickle.load(file)
    for score in loaded_content:
        normal_score_list.append(score)
except:
    normal_score_list.append(0)
    with open(NORMAL_SAVE_FILE, "wb"):
        pass
try:
    with open(HARD_SAVE_FILE, "rb") as file:
        loaded_content = pickle.load(file)
    for score in loaded_content:
        hard_score_list.append(score)
except:
    hard_score_list.append(0)
    with open(HARD_SAVE_FILE, "wb"):
        pass
try:
    with open(NUMBER_OF_WINS_SAVE_FILE, "rb") as file:
        loaded_content = pickle.load(file)
    number_of_wins = int(loaded_content)
except:
    number_of_wins = 0
    with open(NUMBER_OF_WINS_SAVE_FILE, "wb")as file:
        pickle.dump(number_of_wins, file)

# DEFINING CLASSES
current_load = "Players"
load_amount += 1
threading.Thread(target = loading(current_load, load_amount)).start()
class Player:
    global GRAVITY, speed_up
    def __init__(self):
        self.x_pos = 320
        self.y_pos = 120
        self.y_vel = 0
        self.falling = True
        self.jumping = False
        self.active = True
        self.accel_index = 0
        self.can_jump = True
        self.health = 100

    def update(self):
        global JUMP_POWER
        if self.jumping and self.can_jump:
            self.can_jump = False
            self.accel_index = 0
            self.falling = True
            self.jumping = False
            self.y_pos -= JUMP_POWER
                    
        elif self.falling:
            self.y_pos += self.accel_index
            self.accel_index += GRAVITY/100

    def move_left(self):
        if speed_up == True:
            if increase_speed == True:
                self.x_pos -= WALK_SPEED * 3
            else:
                self.x_pos -= WALK_SPEED * 1.5
        else:
            if increase_speed == True:
                self.x_pos -= WALK_SPEED * 2
            else:
                self.x_pos -= WALK_SPEED

    def move_right(self):
        if speed_up == True:
            if increase_speed == True:
                self.x_pos += WALK_SPEED * 3
            else:
                self.x_pos += WALK_SPEED * 1.5
        else:
            if increase_speed == True:
                self.x_pos += WALK_SPEED * 2
            else:
                self.x_pos += WALK_SPEED

    def jump(self):
        self.jumping = True

current_load = "Platforms"
load_amount += 1
threading.Thread(target = loading(current_load, load_amount)).start()
class Platform:
    global platforms_scrolling
    def __init__(self, start_x, studs):
        self.x_pos = start_x
        self.y_pos = 0
        self.studs = studs
        self.height = 20

    def draw(self, surface, image, scroll):
        if platforms_scrolling == True:
            self.y_pos += scroll
        for i in range(self.studs):
            surface.blit(image, ((self.x_pos + 40 * i), self.y_pos))

current_load = "Projectiles"
load_amount += 1
threading.Thread(target = loading(current_load, load_amount)).start()
class Projectile:
    def __init__(self, x_pos, y_pos, velocity):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = velocity
        if self.x_vel < 0:
            self.direction = "left"
        else:
            self.direction = "right"

    def update(self):
        self.x_pos += self.x_vel
    
    def draw(self, surface, image):
        self.update()
        surface.blit(image, (self.x_pos, self.y_pos))

current_load = "Powerups"
load_amount += 1
threading.Thread(target = loading(current_load, load_amount)).start()
class Powerup:
    global freeze0, freeze1, freeze2, freeze3
    global ghost0, ghost1, ghost2, ghost3
    global orb0, orb1, orb2, orb3
    global projectileproof0, projectileproof1, projectileproof2, projectileproof3
    global speed0, speed1, speed2, speed3
    global health0, health1, health2, health3
    def __init__(self, powerup, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_frame = 1
        self.disabling = False
        self.powerup = powerup
        if powerup == "speed":
            self.frame1 = speed0
            self.frame2 = speed1
            self.frame3 = speed2
            self.frame4 = speed3
        elif powerup == "orb":
            self.frame1 = orb0
            self.frame2 = orb1
            self.frame3 = orb2
            self.frame4 = orb3
        elif powerup == "ghost":
            self.frame1 = ghost0
            self.frame2 = ghost1
            self.frame3 = ghost2
            self.frame4 = ghost3
        elif powerup == "projectileproof":
            self.frame1 = projectileproof0
            self.frame2 = projectileproof1
            self.frame3 = projectileproof2
            self.frame4 = projectileproof3
        elif powerup == "freeze":
            self.frame1 = freeze0
            self.frame2 = freeze1
            self.frame3 = freeze2
            self.frame4 = freeze3
        elif powerup == "health":
            self.frame1 = health0
            self.frame2 = health1
            self.frame3 = health2
            self.frame4 = health3 
      
    def draw(self, surface, scroll):
        if platforms_scrolling == True:
            self.y_pos += scroll
        if self.disabling == True:
            self.current_frame += 1
        if self.current_frame > 0 and self.current_frame <= 3:
            surface.blit(self.frame1, (self.x_pos, self.y_pos))
        elif self.current_frame > 3 and self.current_frame <= 6:
            surface.blit(self.frame2, (self.x_pos, self.y_pos))
        elif self.current_frame > 6 and self.current_frame <= 9:
            surface.blit(self.frame3, (self.x_pos, self.y_pos))
        elif self.current_frame > 9 and self.current_frame <= 12:
            surface.blit(self.frame4, (self.x_pos, self.y_pos))

current_load = "Cursor"
load_amount += 1
threading.Thread(target = loading(current_load, load_amount)).start()
class Cursor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.clicked = False
        self.cursor = pygame.Surface((7, 12), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(self.x, self.y, 7, 12)
        
    def update(self):
        self.rect = pygame.Rect(self.x, self.y, 7, 12)
        
    def draw(self, surface):
        self.update()
        pygame.draw.polygon(self.cursor, (255, 255, 255), [(0, 0), (7, 7), (5, 9), (7, 11), (5, 12), (3, 9), (0, 11)])
        pygame.draw.polygon(self.cursor, (0, 0, 0), [(0, 0), (7, 7), (5, 9), (7, 11), (5, 12), (3, 9), (0, 11)], 1)
        surface.blit(self.cursor, (self.x, self.y))

# MAKING SOME OBJECTS
current_load = "Finishing Up"
load_amount += 1
threading.Thread(target = loading(current_load, load_amount)).start()
PLAYER_ONE = Player()
PLAYER_TWO = Player()
CURSOR = Cursor(320, 240)
PLAY1_RECT = pygame.Rect(70, 200, 220, 60)
PLAY2_RECT = pygame.Rect(340, 200, 220, 60)
C_RECT = pygame.Rect(570, 420, 70, 50)
I_RECT = pygame.Rect(10, 410, 60, 50)
EASY_RECT = pygame.Rect(30, 190, 580, 70)
NORMAL_RECT = pygame.Rect(30, 280, 580, 90)
HARD_RECT = pygame.Rect(30, 380, 580, 80)
HIT_RECT = pygame.Rect(220, 360, 200, 70)

# FOR LOADING SCREEN DEBUGGING
debug_end_time = round(pygame.time.get_ticks())
print("Estimated load time " + str(estimated_time * 1000) + "ms")
print("Actual load time: " + str(debug_end_time) + "ms")
print("Difference between actual loading time and predicted loading time: " + str(estimated_time * 1000 - debug_end_time) + "ms")

# MAIN GAME LOOP
while True:
    left_click = False
    CURSOR.clicked = False
    if pygame.mixer.get_busy() == False and game_mode == "menu":
        MAIN_MUSIC.play()
        
    # EVENT HANDLER
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        # Exiting game
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Keydown inputs
        if event.type == KEYDOWN:
            if event.key == K_SPACE and ARCADE_MODE == True and (difficulty == "" or game_over == True) and game_mode != "rescue":
                CURSOR.clicked = True
            if event.key == K_RIGHT and ARCADE_MODE == True and game_mode == "rescue":
                arcade_hit = True
            if event.key == K_ESCAPE:
                # If in menu, quit the game
                if game_mode == "menu":
                    # Appending current score to previous scores file
                    if difficulty == "easy" and high_scores == True:
                        easy_score_list.append(points)
                        with open(EASY_SAVE_FILE, "wb") as file:
                            pickle.dump(easy_score_list, file)
                    if difficulty == "normal" and high_scores == True:
                        normal_score_list.append(points)
                        with open(NORMAL_SAVE_FILE, "wb") as file:
                            pickle.dump(normal_score_list, file)
                    if difficulty == "hard" and high_scores == True:
                        hard_score_list.append(points)
                        with open(HARD_SAVE_FILE, "wb") as file:
                            pickle.dump(hard_score_list, file)
                    # Ending game session properly
                    pygame.quit()
                    sys.exit()
                # If in-game, go to menu
                if game_mode != "menu":
                    BUTTON_CLICKED.play()
                    # Appending current score to previous scores file
                    if difficulty == "easy" and high_scores == True:
                        easy_score_list.append(points)
                        with open(EASY_SAVE_FILE, "wb") as file:
                            pickle.dump(easy_score_list, file)
                    if difficulty == "normal" and high_scores == True:
                        normal_score_list.append(points)
                        with open(NORMAL_SAVE_FILE, "wb") as file:
                            pickle.dump(normal_score_list, file)
                    if difficulty == "hard" and high_scores == True:
                        hard_score_list.append(points)
                        with open(HARD_SAVE_FILE, "wb") as file:
                            pickle.dump(hard_score_list, file)
                    # Resetting values
                    PLAYER_ONE.x_pos = 320
                    PLAYER_ONE.y_pos = 120
                    PLAYER_ONE.accel_index = 0
                    PLAYER_ONE.jumping = False
                    PLAYER_ONE.health = 100
                    PLAYER_TWO.x_pos = 320
                    PLAYER_TWO.y_pos = 120
                    PLAYER_TWO.accel_index = 0
                    PLAYER_TWO.jumping = False
                    PLAYER_TWO.health = 100
                    speed_index = 0
                    ghost_index = 0
                    projectile_proof_index = 0
                    platforms_scrolling_index = 0
                    speed_up = False
                    ghost_on = False
                    projectile_proof = False
                    platforms_scrolling = True
                    game_mode = "menu"
                    difficulty = ""
                    CURSOR.x = 320
                    CURSOR.y = 240
                    initial_blit = False
                    credits_y = 0
                    info_y = 0
                    points = 0
                    EASY_SCROLL_SPEED = 2
                    NORMAL_SCROLL_SPEED = 2.75
                    HARD_SCROLL_SPEED = 3.5
                    can_play_drowning = True
                    one_has_died = False
                    game_over = False
                    rescue_health = 100
                    rescue_y = 200
                    boss_health = 10000
                    boss_y = 150
                    # Stopping music and clearing lists
                    GRASSLAND_MUSIC.stop()
                    FACILITY_MUSIC.stop()
                    VOLCANO_MUSIC.stop()
                    CREDITS_MUSIC.stop()
                    PREGAME_MUSIC.stop()
                    ENDING_MUSIC.stop()
                    projectile_list.clear()
                    platform_list.clear()
                    powerup_list.clear()
                        
        # Mouse events
        if event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                left_click = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                left_click = False
    
    # Normal keybinds
    if ARCADE_MODE == False:
        if pressed[K_d]:
            PLAYER_ONE.move_right()
        if pressed[K_a]:
            PLAYER_ONE.move_left()
        if pressed[K_w]:
            PLAYER_ONE.jump()
            if PLAYER_ONE.accel_index > 2:
                PLAYER_ONE.can_jump = True
            if game_mode == "rescue" and rescue_y >= 100:
                rescue_y -= 3
        if pressed[K_s] and game_mode == "rescue" and rescue_y <= 330:
            rescue_y += 3
        if pressed[K_UP]:
            PLAYER_TWO.jump()
            if PLAYER_TWO.accel_index > 2:
                PLAYER_TWO.can_jump = True
        if pressed[K_LEFT]:
            PLAYER_TWO.move_left()
        if pressed[K_RIGHT]:
            PLAYER_TWO.move_right()
            
    # Arcade cabinet keybinds
    elif ARCADE_MODE == True:
        if pressed[K_RIGHT]:
            PLAYER_ONE.move_right()
        if pressed[K_LEFT]:
            PLAYER_ONE.move_left()
        if pressed[K_UP]:
            PLAYER_ONE.jump()
            if PLAYER_ONE.accel_index > 2:
                PLAYER_ONE.can_jump = True
            if game_mode == "rescue" and rescue_y >= 100:
                rescue_y -= 3
        if pressed[K_DOWN] and game_mode == "rescue" and rescue_y <= 330:
            rescue_y += 3
        if pressed[K_r]:
            PLAYER_TWO.jump()
            if PLAYER_TWO.accel_index > 2:
                PLAYER_TWO.can_jump = True
        if pressed[K_d]:
            PLAYER_TWO.move_left()
        if pressed[K_g]:
            PLAYER_TWO.move_right()
    if ARCADE_MODE == True and difficulty == "" and game_mode != "pregame" and game_mode != "rescue":
        cursor_mode = True
        if pressed[K_UP] and CURSOR.y >= 0:
            CURSOR.y -= ARCADE_CURSOR_SPEED
        if pressed[K_DOWN] and CURSOR.y <= 480:
            CURSOR.y += ARCADE_CURSOR_SPEED
        if pressed[K_LEFT] and CURSOR.x >= 0 :
            CURSOR.x -= ARCADE_CURSOR_SPEED
        if pressed[K_RIGHT] and CURSOR.x <= 640:
            CURSOR.x += ARCADE_CURSOR_SPEED

    # MAIN MENU MODE
    if game_mode == "menu":
        # Checking if the mouse is over button location using normal keybinds
        if ARCADE_MODE == False:
            if PLAY1_RECT.collidepoint(mouse_x, mouse_y) == True:
                SCREEN.blit(menuscreenplay1, (0, 0))
                if left_click == True:
                    left_click = False
                    BUTTON_CLICKED.play()
                    game_mode = "diff1"
            elif PLAY2_RECT.collidepoint(mouse_x, mouse_y) == True:
                SCREEN.blit(menuscreenplay2, (0, 0))
                if left_click == True:
                    left_click = False
                    BUTTON_CLICKED.play()
                    game_mode = "diff2"
            elif I_RECT.collidepoint(mouse_x, mouse_y) == True:
                SCREEN.blit(menuscreeninfo, (0, 0))
                if left_click == True:
                    left_click = False
                    BUTTON_CLICKED.play()
                    MAIN_MUSIC.stop()
                    CREDITS_MUSIC.play()
                    game_mode = "info"
            elif C_RECT.collidepoint(mouse_x, mouse_y) == True:
                SCREEN.blit(menuscreencredits, (0, 0))
                if left_click == True:
                    left_click = False
                    BUTTON_CLICKED.play()
                    MAIN_MUSIC.stop()
                    CREDITS_MUSIC.play()
                    game_mode = "credits"
            else:
                SCREEN.blit(menuscreen, (0, 0))
        # Checking if the mouse is over button location using arcade cabinet keybinds
        elif ARCADE_MODE == True: 
            if PLAY1_RECT.collidepoint(CURSOR.x, CURSOR.y) == True:
                SCREEN.blit(menuscreenplay1, (0, 0))
                if CURSOR.clicked == True:
                    CURSOR.clicked = False
                    BUTTON_CLICKED.play()
                    game_mode = "diff1"
            elif PLAY2_RECT.collidepoint(CURSOR.x, CURSOR.y) == True:
                SCREEN.blit(menuscreenplay2, (0, 0))
                if CURSOR.clicked == True:
                    CURSOR.clicked = False
                    BUTTON_CLICKED.play()
                    game_mode = "diff2"
            elif I_RECT.collidepoint(CURSOR.x, CURSOR.y) == True:
                SCREEN.blit(menuscreeninfo, (0, 0))
                if CURSOR.clicked == True:
                    CURSOR.clicked = False
                    BUTTON_CLICKED.play()
                    MAIN_MUSIC.stop()
                    CREDITS_MUSIC.play()
                    game_mode = "info"
            elif C_RECT.collidepoint(CURSOR.x, CURSOR.y) == True:
                SCREEN.blit(menuscreencredits, (0, 0))
                if CURSOR.clicked == True:
                    CURSOR.clicked = False
                    BUTTON_CLICKED.play()
                    MAIN_MUSIC.stop()
                    CREDITS_MUSIC.play()
                    game_mode = "credits"
            else:
                SCREEN.blit(menuscreen, (0, 0))
        # Blitting high-scores to the screen
        text = SMALLFONT.render("High Scores: ", False, (0, 0, 0))
        SCREEN.blit(text, (100, 430))
        easy_high_score = max(easy_score_list)
        text2 = SMALLFONT.render(str(easy_high_score), False, (0, 255, 0))
        SCREEN.blit(text2, (310, 430))
        normal_high_score = max(normal_score_list)
        text3 = SMALLFONT.render(str(normal_high_score), False, (255, 255, 0))
        SCREEN.blit(text3, (395, 430))
        hard_high_score = max(hard_score_list)
        text4 = SMALLFONT.render(str(hard_high_score), False, (255, 0, 0))
        SCREEN.blit(text4, (480, 430))
        if number_of_wins == 1:
            text5 = ULTRATINYFONT.render("This game has been beaten: 1 time", False, (255, 0, 0))
            SCREEN.blit(text5, (90, 405))
        else:
            text5 = ULTRATINYFONT.render("This game has been beaten: " + str(number_of_wins) + " times", False, (255, 0, 0))
            SCREEN.blit(text5, (90, 405))
        text6 = ULTRATINYFONT.render("Version: " + VERSION, False, (255, 0, 0))
        SCREEN.blit(text6, (20, 20))
          
    # CUTSCENE
    if game_mode == "pregame":
        if pygame.mixer.get_busy() == False:
            PREGAME_MUSIC.play()
        SCREEN.blit(volcanobg, (0, 0))
        text = TINYFONT.render("Click to continue...", False, (0, 0, 0))
        SCREEN.blit(text, (215, 440))
        if pregame_stage == 0:
            SCREEN.blit(playerone0, (60, 180))
            SCREEN.blit(playertwo0, (60, 250))
            text = TINYFONT.render("Time to say our prayers to the volcano...", False, (255, 55, 55))
            SCREEN.blit(text, (85, 360))
        elif pregame_stage == 1:
            SCREEN.blit(playerone0, (60, 180))
            SCREEN.blit(playertwo0, (60, 250))
            SCREEN.blit(boss0, (500, 135))
            text = TINYFONT.render("Who is that evil-looking robot???", False, (255, 55, 55))
            SCREEN.blit(text, (125, 360))
        elif pregame_stage == 2:
            SCREEN.blit(playerone0, (60, 180))
            SCREEN.blit(playertwo0, (515, 280))
            SCREEN.blit(boss0, (500, 135))
            text = SMALLFONT.render("Aaaah-", False, (255, 55, 55))
            SCREEN.blit(text, (255, 360))
            text2 = MEDIUMFONT.render("!", False, (255, 55, 55))
            SCREEN.blit(text2, (75, 130))
        elif pregame_stage == 3:
            SCREEN.blit(playerone0, (60, 180))
            SCREEN.blit(playertwo0, (515, 280))
            SCREEN.blit(boss1, (500, 135))
            text = SMALLFONT.render("She is now mine.", False, (255, 55, 55))
            SCREEN.blit(text, (190, 360))
            text2 = MEDIUMFONT.render("!!", False, (255, 55, 55))
            SCREEN.blit(text2, (65, 130))
        elif pregame_stage == 4:
            SCREEN.blit(playerone0, (60, 180))
            text = MEDIUMFONT.render("HELP ME!!!", False, (255, 55, 55))
            rotated_text = pygame.transform.rotate(text, 25)
            SCREEN.blit(rotated_text, (310, 140))
            text2 = MEDIUMFONT.render("!!!", False, (255, 55, 55))
            SCREEN.blit(text2, (60, 130))
        elif pregame_stage >= 5:
            game_mode = "menu"
            PREGAME_MUSIC.stop()
        text = ULTRATINYFONT.render("Protip: Use escape to skip the cutscene", False, (255, 55, 55))
        SCREEN.blit(text, (170, 20))
        if left_click == True or CURSOR.clicked == True:
            left_click = False
            BUTTON_CLICKED.play()
            pregame_stage += 1
    
    # DOING SOME LOGIC TO MAKE DIRTY RECTANGLE METHOD WORK
    rects_to_update = []
    for platform in platform_list:
        new_rect = pygame.Rect(platform.x_pos, platform.y_pos, platform.studs * 40, 20)
        rects_to_update.append(new_rect)
    for powerup in powerup_list:
        new_rect = pygame.Rect(powerup.x_pos, powerup.y_pos, 24, 24)
        rects_to_update.append(new_rect)
    for projectile in projectile_list:
        new_rect = pygame.Rect(projectile.x_pos - 10, projectile.y_pos, 60, 20)
        rects_to_update.append(new_rect)
    new_rect = pygame.Rect(PLAYER_ONE.x_pos - 25, PLAYER_ONE.y_pos - 25, 100, 150)
    rects_to_update.append(new_rect)
    new_rect = pygame.Rect(PLAYER_TWO.x_pos - 25, PLAYER_TWO.y_pos - 25, 100, 150)
    rects_to_update.append(new_rect)
    if game_mode == "rescue":
        new_rect = pygame.Rect(60, rescue_y - 10, 50, 70)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(500, boss_y - 25, 80, 170)
        rects_to_update.append(new_rect)
    
    # SINGLE-PLAYER MODE
    if game_mode == "play1":
        # LOGIC FOR SINGLE-PLAYER EASY
        if difficulty == "easy":
            # Getting ready to do some logic
            if pygame.mixer.get_busy() == False:
                GRASSLAND_MUSIC.play()
            points_active = True
            PLAYER_ONE.falling = True
            SCREEN.blit(grasslandbg, (0, 0))
            SCREEN.blit(water_image, (0, liquid_y))
            if frame_index >= 0 and frame_index < 4:
                SCREEN.blit(playerone0, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
            if frame_index >= 4 and frame_index < 8:
                SCREEN.blit(playerone1, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
            if frame_index >= 8 and frame_index < 12:
                SCREEN.blit(playerone2, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
            # Making some platforms
            if platforms_scrolling == True and last_platform_y >= 120 - EASY_SCROLL_SPEED:
                left_studs = random.randint(2, 16 - EASY_PLATFORM_GAP)
                right_studs = 16 - left_studs + EASY_PLATFORM_GAP
                temp_platform = Platform(0, left_studs)
                temp_platform2 = Platform(left_studs * 40 + EASY_PLATFORM_GAP * 40, right_studs)
                platform_list.append(temp_platform)
                platform_list.append(temp_platform2)
            # Making some powerups
            speed_make = random.randint(0, speed_rarity)
            if speed_make == 0 and game_over == False:
                new = Powerup("speed", random.randint(40, 600), 0)
                powerup_list.append(new)
            health_make = random.randint(0, health_rarity)
            if health_make == 0 and game_over == False:
                new = Powerup("health", random.randint(40, 600), 0)
                powerup_list.append(new)
            ghost_make = random.randint(0, ghost_rarity)
            if ghost_make == 0 and game_over == False:
                new = Powerup("ghost", random.randint(40, 600), 0)
                powerup_list.append(new)
            freeze_make = random.randint(0, freeze_rarity)
            if freeze_make == 0 and game_over == False:
                new = Powerup("freeze", random.randint(40, 600), 0)
                powerup_list.append(new)
            # Putting powerup text on the screen
            if speed_up == True:
                speed_time_left = round((300 - speed_index) / 30, 1)
                speed_text = SMALLFONT.render("Speed Up: " + str(speed_time_left), False, (0, 205, 0))
                SCREEN.blit(speed_text, (20, 80))
            if ghost_on == True:
                ghost_time_left = round((180 - ghost_index) / 30, 1)
                ghost_text = SMALLFONT.render("Ghost Platforms: " + str(ghost_time_left), False, (150, 0, 210))
                SCREEN.blit(ghost_text, (20, 120))
            if platforms_scrolling == False:
                freeze_time_left = round((120 - platforms_scrolling_index) / 30, 1)
                freeze_text = SMALLFONT.render("Liquid Freeze: " + str(freeze_time_left), False, (35, 35, 255))
                SCREEN.blit(freeze_text, (20, 200))
            # Doing some score and health logic
            text = MEDIUMFONT.render("Score: " + str(points), False, (0, 0, 0))
            SCREEN.blit(text, (20, 20))
            HEALTH_WIDTH = int(240 * PLAYER_ONE.health / 100)
            COLOR_VALUE = round(255 - PLAYER_ONE.health * 2.55)
            if COLOR_VALUE > 255:
                COLOR_VALUE = 255
            text2 = MEDIUMFONT.render("Health: " + str(round(PLAYER_ONE.health)), False, (COLOR_VALUE, (255 - COLOR_VALUE), 0))
            SCREEN.blit(text2, (320, 20))
            if PLAYER_ONE.health <= 20:
                pygame.draw.rect(SCREEN, (COLOR_VALUE, (255 - COLOR_VALUE), 0), pygame.Rect(325 + random.randint(1, (25 - round(PLAYER_ONE.health))), 75, HEALTH_WIDTH, 20))
            else:
                pygame.draw.rect(SCREEN, (COLOR_VALUE, (255 - COLOR_VALUE), 0), pygame.Rect(325, 75, HEALTH_WIDTH, 20))
            PLAYER_ONE.health += 0.05
            if PLAYER_ONE.health > 100:
                PLAYER_ONE.health = 100
            # COLLISION DETECTION
            # If liquid is touched subtract from health
            if PLAYER_ONE.y_pos >= liquid_y - 25 and disable_liquids == False:
                PLAYER_ONE.health -= WATER_DAMAGE
            # Checking if player is above or below platform and proceed accordingly
            for platform in platform_list:
                if PLAYER_ONE.y_pos + 20 <= platform.y_pos and PLAYER_ONE.y_pos + 20 >= platform.y_pos - 20 and PLAYER_ONE.x_pos + 50 >= platform.x_pos and PLAYER_ONE.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_ONE.falling = False
                if ghost_on == False and PLAYER_ONE.y_pos + 20 >= platform.y_pos and PLAYER_ONE.y_pos <= platform.y_pos + 40 and PLAYER_ONE.x_pos + 50 >= platform.x_pos and PLAYER_ONE.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_ONE.jumping = False
                    PLAYER_ONE.falling = True
                    PLAYER_ONE.y_pos += EASY_SCROLL_SPEED
            # Checking for powerup collisions
            for powerup in powerup_list:
                if ((PLAYER_ONE.x_pos >= powerup.x_pos and PLAYER_ONE.x_pos <= powerup.x_pos + 40) or (PLAYER_ONE.x_pos + 25 >= powerup.x_pos and PLAYER_ONE.x_pos + 25 <= powerup.x_pos + 40) or (PLAYER_ONE.x_pos + 50 >= powerup.x_pos and PLAYER_ONE.x_pos + 50 <= powerup.x_pos + 40)) and PLAYER_ONE.y_pos <= powerup.y_pos and PLAYER_ONE.y_pos >= powerup.y_pos - 40 and game_over == False:
                    POWERUP.play()
                    if powerup.powerup == "speed":
                        speed_up = True
                        speed_index = 0
                    elif powerup.powerup == "health":
                        PLAYER_ONE.health = 100
                    elif powerup.powerup == "ghost":
                        ghost_on = True
                        ghost_index = 0
                    elif powerup.powerup == "freeze":
                        platforms_scrolling = False
                        platform_scrolling_index = 0
                    powerup.disabling = True
            # When player dies do this
            if PLAYER_ONE.health <= 0:
                GRASSLAND_MUSIC.stop()
                projectile_list.clear()
                platform_list.clear()
                powerup_list.clear()
                game_over = True
                if can_play_drowning:
                    DROWNING.play()
                    can_play_drowning = False
                points_active = False
                SCREEN.blit(game_over_screen, (0, 0))
                text = MEDIUMFONT.render(str(points), False, (125, 0, 0))
                SCREEN.blit(text, (480, 385))
                # Reading previous scores for this difficulty
                high_score = max(easy_score_list)
                if high_score >= points:
                    text2 = SMALLFONT.render(str(high_score), False, (125, 0, 0))
                    SCREEN.blit(text2, (525, 445))
                else:
                    text2 = SMALLFONT.render(str(points), False, (125, 0, 0))
                    SCREEN.blit(text2, (525, 445))
                pygame.display.update()
                # If player clicks continue do this
                if left_click == True or CURSOR.clicked == True:
                    left_click = False
                    CURSOR.clicked = False
                    BUTTON_CLICKED.play()
                    # Appending current score to previous scores file
                    if high_scores == True:
                        easy_score_list.append(points)
                        with open(EASY_SAVE_FILE, "wb") as file:
                            pickle.dump(easy_score_list, file)
                    # Resetting values
                    PLAYER_ONE.x_pos = 320
                    PLAYER_ONE.y_pos = 120
                    PLAYER_ONE.health = 100
                    PLAYER_ONE.accel_index = 0
                    PLAYER_ONE.jumping = False
                    speed_index = 0
                    ghost_index = 0
                    projectile_proof_index = 0
                    platforms_scrolling_index = 0
                    speed_up = False
                    ghost_on = False
                    projectile_proof = False
                    platforms_scrolling = True
                    EASY_SCROLL_SPEED = 2
                    game_mode = "menu"
                    difficulty = ""
                    CURSOR.x = 320
                    CURSOR.y = 240
                    initial_blit = False
                    credits_y = 0
                    info_y = 0
                    points = 0
                    can_play_drowning = True
                    game_over = False
            # Border collision detection
            if PLAYER_ONE.x_pos >= 590:
                PLAYER_ONE.x_pos -= 10
            if PLAYER_ONE.x_pos <= 0:
                PLAYER_ONE.x_pos += 10
            if PLAYER_ONE.y_pos <= 0:
                PLAYER_ONE.y_pos += 10
            if PLAYER_ONE.y_pos >= 430:
                PLAYER_ONE.falling = False
                PLAYER_ONE.y_pos -= 10
            PLAYER_ONE.update()
            EASY_SCROLL_SPEED += 0.001
        # LOGIC FOR SINGLE-PLAYER NORMAL
        if difficulty == "normal":
            # Getting ready to do some logic
            if pygame.mixer.get_busy() == False:
                FACILITY_MUSIC.play()
            points_active = True
            PLAYER_ONE.falling = True
            SCREEN.blit(facilitybg, (0, 0))
            SCREEN.blit(acid_image, (0, liquid_y))
            if frame_index >= 0 and frame_index < 4:
                SCREEN.blit(playerone0, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
            if frame_index >= 4 and frame_index < 8:
                SCREEN.blit(playerone1, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
            if frame_index >= 8 and frame_index < 12:
                SCREEN.blit(playerone2, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
            # Making some platforms
            if platforms_scrolling == True and last_platform_y >= 120 - NORMAL_SCROLL_SPEED:
                left_studs = random.randint(2, 16 - NORMAL_PLATFORM_GAP)
                right_studs = 16 - left_studs + NORMAL_PLATFORM_GAP
                temp_platform = Platform(0, left_studs)
                temp_platform2 = Platform(left_studs * 40 + NORMAL_PLATFORM_GAP * 40, right_studs)
                platform_list.append(temp_platform)
                platform_list.append(temp_platform2)
            # Making some projectiles
            chance_of_making = random.randint(0, NORMAL_PROJECTILE_RARITY)
            if chance_of_making == 0 and game_over == False and disable_projectiles == False:
                PROJECTILE_FIRE.play()
                new = Projectile(0, random.randint(0, 480), random.randint(2, 5))
                projectile_list.append(new)
            if chance_of_making == 1 and game_over == False and disable_projectiles == False:
                PROJECTILE_FIRE.play()
                new2 = Projectile(640, random.randint(0, 480), random.randint(-5, -2))
                projectile_list.append(new2)
            # Making some powerups
            speed_make = random.randint(0, speed_rarity)
            if speed_make == 0 and game_over == False:
                new = Powerup("speed", random.randint(40, 600), 0)
                powerup_list.append(new)
            health_make = random.randint(0, health_rarity)
            if health_make == 0 and game_over == False:
                new = Powerup("health", random.randint(40, 600), 0)
                powerup_list.append(new)
            ghost_make = random.randint(0, ghost_rarity)
            if ghost_make == 0 and game_over == False:
                new = Powerup("ghost", random.randint(40, 600), 0)
                powerup_list.append(new)
            projectile_proof_make = random.randint(0, projectile_proof_rarity)
            if projectile_proof_make == 0 and game_over == False:
                new = Powerup("projectileproof", random.randint(40, 600), 0)
                powerup_list.append(new)
            freeze_make = random.randint(0, freeze_rarity)
            if freeze_make == 0 and game_over == False:
                new = Powerup("freeze", random.randint(40, 600), 0)
                powerup_list.append(new)
            # Putting powerup text on the screen
            if speed_up == True:
                speed_time_left = round((300 - speed_index) / 30, 1)
                speed_text = SMALLFONT.render("Speed Up: " + str(speed_time_left), False, (0, 205, 0))
                SCREEN.blit(speed_text, (20, 80))
            if ghost_on == True:
                ghost_time_left = round((180 - ghost_index) / 30, 1)
                ghost_text = SMALLFONT.render("Ghost Platforms: " + str(ghost_time_left), False, (150, 0, 210))
                SCREEN.blit(ghost_text, (20, 120))
            if projectile_proof == True:
                projectile_time_left = round((300 - projectile_proof_index) / 30, 1)
                projectile_text = SMALLFONT.render("Projectile Proof: " + str(projectile_time_left), False, (230, 140, 0))
                SCREEN.blit(projectile_text, (20, 160))
            if platforms_scrolling == False:
                freeze_time_left = round((120 - platforms_scrolling_index) / 30, 1)
                freeze_text = SMALLFONT.render("Liquid Freeze: " + str(freeze_time_left), False, (35, 35, 255))
                SCREEN.blit(freeze_text, (20, 200))
            # Doing some score and health logic
            text = MEDIUMFONT.render("Score: " + str(points), False, (0, 0, 0))
            SCREEN.blit(text, (20, 20))
            HEALTH_WIDTH = int(240 * PLAYER_ONE.health / 100)
            COLOR_VALUE = round(255 - PLAYER_ONE.health * 2.55)
            if COLOR_VALUE > 255:
                COLOR_VALUE = 255
            text2 = MEDIUMFONT.render("Health: " + str(round(PLAYER_ONE.health)), False, (COLOR_VALUE, (255 - COLOR_VALUE), 0))
            SCREEN.blit(text2, (320, 20))
            if PLAYER_ONE.health <= 20:
                pygame.draw.rect(SCREEN, (COLOR_VALUE, (255 - COLOR_VALUE), 0), pygame.Rect(325 + random.randint(1, (25 - round(PLAYER_ONE.health))), 75, HEALTH_WIDTH, 20))
            else:
                pygame.draw.rect(SCREEN, (COLOR_VALUE, (255 - COLOR_VALUE), 0), pygame.Rect(325, 75, HEALTH_WIDTH, 20))
            PLAYER_ONE.health += 0.03
            if PLAYER_ONE.health > 100:
                PLAYER_ONE.health = 100
            # COLLISION DETECTION
            # If liquid is touched subtract from health
            if PLAYER_ONE.y_pos >= liquid_y - 25 and disable_liquids == False:
                PLAYER_ONE.health -= ACID_DAMAGE
            # Checking if player is above or below platform and proceed accordingly
            for platform in platform_list:
                if PLAYER_ONE.y_pos + 20 <= platform.y_pos and PLAYER_ONE.y_pos + 20 >= platform.y_pos - 20 and PLAYER_ONE.x_pos + 50 >= platform.x_pos and PLAYER_ONE.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_ONE.falling = False
                if ghost_on == False and PLAYER_ONE.y_pos + 20 >= platform.y_pos and PLAYER_ONE.y_pos <= platform.y_pos + 40 and PLAYER_ONE.x_pos + 50 >= platform.x_pos and PLAYER_ONE.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_ONE.jumping = False
                    PLAYER_ONE.falling = True
                    PLAYER_ONE.y_pos += NORMAL_SCROLL_SPEED
            # Checking for projectile collisions
            for projectile in projectile_list:
                if projectile_proof == False and ((PLAYER_ONE.x_pos >= projectile.x_pos and PLAYER_ONE.x_pos <= projectile.x_pos + 40) or (PLAYER_ONE.x_pos + 25 >= projectile.x_pos and PLAYER_ONE.x_pos + 25 <= projectile.x_pos + 40) or (PLAYER_ONE.x_pos + 50 >= projectile.x_pos and PLAYER_ONE.x_pos + 50 <= projectile.x_pos + 40)) and PLAYER_ONE.y_pos <= projectile.y_pos and PLAYER_ONE.y_pos >= projectile.y_pos - 40 and game_over == False:
                    PROJECTILE_HIT.play()
                    PLAYER_ONE.health -= BULLET_DAMAGE
                    projectile_list.remove(projectile)
            # Checking for powerup collisions
            for powerup in powerup_list:
                if ((PLAYER_ONE.x_pos >= powerup.x_pos and PLAYER_ONE.x_pos <= powerup.x_pos + 40) or (PLAYER_ONE.x_pos + 25 >= powerup.x_pos and PLAYER_ONE.x_pos + 25 <= powerup.x_pos + 40) or (PLAYER_ONE.x_pos + 50 >= powerup.x_pos and PLAYER_ONE.x_pos + 50 <= powerup.x_pos + 40)) and PLAYER_ONE.y_pos <= powerup.y_pos and PLAYER_ONE.y_pos >= powerup.y_pos - 40 and game_over == False:
                    POWERUP.play()
                    if powerup.powerup == "speed":
                        speed_up = True
                        speed_index = 0
                    elif powerup.powerup == "health":
                        PLAYER_ONE.health = 100
                    elif powerup.powerup == "ghost":
                        ghost_on = True
                        ghost_index = 0
                    elif powerup.powerup == "projectileproof":
                        projectile_proof = True
                        projectile_proof_index = 0
                    elif powerup.powerup == "freeze":
                        platforms_scrolling = False
                        platform_scrolling_index = 0
                    powerup.disabling = True
            # When player dies do this
            if PLAYER_ONE.health <= 0:
                FACILITY_MUSIC.stop()
                projectile_list.clear()
                platform_list.clear()
                powerup_list.clear()
                game_over = True
                if can_play_drowning:
                    DROWNING.play()
                    can_play_drowning = False
                points_active = False
                SCREEN.blit(game_over_screen, (0, 0))
                text = MEDIUMFONT.render(str(points), False, (125, 0, 0))
                SCREEN.blit(text, (480, 385))
                # Reading previous scores for this difficulty
                high_score = max(normal_score_list)
                if high_score >= points:
                    text2 = SMALLFONT.render(str(high_score), False, (125, 0, 0))
                    SCREEN.blit(text2, (525, 445))
                else:
                    text2 = SMALLFONT.render(str(points), False, (125, 0, 0))
                    SCREEN.blit(text2, (525, 445))
                pygame.display.update()
                # If player clicks continue do this
                if left_click == True or CURSOR.clicked == True:
                    BUTTON_CLICKED.play()
                    # Appending current score to previous scores file
                    if high_scores == True:
                        normal_score_list.append(points)
                        with open(NORMAL_SAVE_FILE, "wb") as file:
                            pickle.dump(normal_score_list, file)
                    # Resetting values
                    PLAYER_ONE.x_pos = 320
                    PLAYER_ONE.y_pos = 120
                    PLAYER_ONE.health = 100
                    PLAYER_ONE.accel_index = 0
                    PLAYER_ONE.jumping = False
                    speed_index = 0
                    ghost_index = 0
                    projectile_proof_index = 0
                    platforms_scrolling_index = 0
                    speed_up = False
                    ghost_on = False
                    projectile_proof = False
                    platforms_scrolling = True
                    NORMAL_SCROLL_SPEED = 2.75
                    game_mode = "menu"
                    difficulty = ""
                    CURSOR.x = 320
                    CURSOR.y = 240
                    initial_blit = False
                    credits_y = 0
                    info_y = 0
                    points = 0
                    can_play_drowning = True
                    game_over = False
            # Border collision detection
            if PLAYER_ONE.x_pos >= 590:
                PLAYER_ONE.x_pos -= 10
            if PLAYER_ONE.x_pos <= 0:
                PLAYER_ONE.x_pos += 10
            if PLAYER_ONE.y_pos <= 0:
                PLAYER_ONE.y_pos += 10
            if PLAYER_ONE.y_pos >= 430:
                PLAYER_ONE.falling = False
                PLAYER_ONE.y_pos -= 10
            PLAYER_ONE.update()
            NORMAL_SCROLL_SPEED += 0.001
        # LOGIC FOR SINGLE-PLAYER HARD
        if difficulty == "hard":
            # Getting ready to do some logic
            if pygame.mixer.get_busy() == False:
                VOLCANO_MUSIC.play()
            points_active = True
            PLAYER_ONE.falling = True
            SCREEN.blit(volcanobg, (0, 0))
            SCREEN.blit(lava_image, (0, liquid_y))
            if frame_index >= 0 and frame_index < 4:
                SCREEN.blit(playerone0, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
            if frame_index >= 4 and frame_index < 8:
                SCREEN.blit(playerone1, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
            if frame_index >= 8 and frame_index < 12:
                SCREEN.blit(playerone2, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
            # Making some platforms
            if platforms_scrolling == True and last_platform_y >= 120 - HARD_SCROLL_SPEED:
                left_studs = random.randint(2, 16 - HARD_PLATFORM_GAP)
                right_studs = 16 - left_studs + HARD_PLATFORM_GAP
                temp_platform = Platform(0, left_studs)
                temp_platform2 = Platform(left_studs * 40 + HARD_PLATFORM_GAP * 40, right_studs)
                platform_list.append(temp_platform)
                platform_list.append(temp_platform2)
            # Making some projectiles
            chance_of_making = random.randint(0, HARD_PROJECTILE_RARITY)
            if chance_of_making == 0 and game_over == False and disable_projectiles == False:
                PROJECTILE_FIRE.play()
                new = Projectile(0, random.randint(0, 480), random.randint(2, 5))
                projectile_list.append(new)
            if chance_of_making == 1 and game_over == False and disable_projectiles == False:
                PROJECTILE_FIRE.play()
                new2 = Projectile(640, random.randint(0, 480), random.randint(-5, -2))
                projectile_list.append(new2)
            # Making some powerups
            speed_make = random.randint(0, speed_rarity)
            if speed_make == 0 and game_over == False:
                new = Powerup("speed", random.randint(40, 600), 0)
                powerup_list.append(new)
            health_make = random.randint(0, health_rarity)
            if health_make == 0 and game_over == False:
                new = Powerup("health", random.randint(40, 600), 0)
                powerup_list.append(new)
            orb_make = random.randint(0, orb_rarity)
            if orb_make == 0 and game_over == False:
                new = Powerup("orb", random.randint(40, 600), 0)
                powerup_list.append(new)
            ghost_make = random.randint(0, ghost_rarity)
            if ghost_make == 0 and game_over == False:
                new = Powerup("ghost", random.randint(40, 600), 0)
                powerup_list.append(new)
            projectile_proof_make = random.randint(0, projectile_proof_rarity)
            if projectile_proof_make == 0 and game_over == False:
                new = Powerup("projectileproof", random.randint(40, 600), 0)
                powerup_list.append(new)
            freeze_make = random.randint(0, freeze_rarity)
            if freeze_make == 0 and game_over == False:
                new = Powerup("freeze", random.randint(40, 600), 0)
                powerup_list.append(new)
            # Putting powerup text on the screen
            if speed_up == True:
                speed_time_left = round((300 - speed_index) / 30, 1)
                speed_text = SMALLFONT.render("Speed Up: " + str(speed_time_left), False, (0, 205, 0))
                SCREEN.blit(speed_text, (20, 80))
            if ghost_on == True:
                ghost_time_left = round((180 - ghost_index) / 30, 1)
                ghost_text = SMALLFONT.render("Ghost Platforms: " + str(ghost_time_left), False, (150, 0, 210))
                SCREEN.blit(ghost_text, (20, 120))
            if projectile_proof == True:
                projectile_time_left = round((300 - projectile_proof_index) / 30, 1)
                projectile_text = SMALLFONT.render("Projectile Proof: " + str(projectile_time_left), False, (230, 140, 0))
                SCREEN.blit(projectile_text, (20, 160))
            if platforms_scrolling == False:
                freeze_time_left = round((120 - platforms_scrolling_index) / 30, 1)
                freeze_text = SMALLFONT.render("Liquid Freeze: " + str(freeze_time_left), False, (35, 35, 255))
                SCREEN.blit(freeze_text, (20, 200))
            # Doing some score and health logic
            text = MEDIUMFONT.render("Score: " + str(points), False, (0, 0, 0))
            SCREEN.blit(text, (20, 20))
            HEALTH_WIDTH = int(240 * PLAYER_ONE.health / 100)
            COLOR_VALUE = round(255 - PLAYER_ONE.health * 2.55)
            if COLOR_VALUE > 255:
                COLOR_VALUE = 255
            text2 = MEDIUMFONT.render("Health: " + str(round(PLAYER_ONE.health)), False, (COLOR_VALUE, (255 - COLOR_VALUE), 0))
            SCREEN.blit(text2, (320, 20))
            if PLAYER_ONE.health <= 20:
                pygame.draw.rect(SCREEN, (COLOR_VALUE, (255 - COLOR_VALUE), 0), pygame.Rect(325 + random.randint(1, (25 - round(PLAYER_ONE.health))), 75, HEALTH_WIDTH, 20))
            else:
                pygame.draw.rect(SCREEN, (COLOR_VALUE, (255 - COLOR_VALUE), 0), pygame.Rect(325, 75, HEALTH_WIDTH, 20))
            PLAYER_ONE.health += 0.02
            if PLAYER_ONE.health > 100:
                PLAYER_ONE.health = 100
            # COLLISION DETECTION
            # If liquid is touched subtract from health
            if PLAYER_ONE.y_pos >= liquid_y - 25 and disable_liquids == False:
                PLAYER_ONE.health -= LAVA_DAMAGE
            # Checking if player is above or below platform and proceed accordingly
            for platform in platform_list:
                if PLAYER_ONE.y_pos + 20 <= platform.y_pos and PLAYER_ONE.y_pos + 20 >= platform.y_pos - 20 and PLAYER_ONE.x_pos + 50 >= platform.x_pos and PLAYER_ONE.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_ONE.falling = False
                if ghost_on == False and PLAYER_ONE.y_pos + 20 >= platform.y_pos and PLAYER_ONE.y_pos <= platform.y_pos + 40 and PLAYER_ONE.x_pos + 50 >= platform.x_pos and PLAYER_ONE.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_ONE.jumping = False
                    PLAYER_ONE.falling = True
                    PLAYER_ONE.y_pos += HARD_SCROLL_SPEED
            # Checking for projectile collisions
            for projectile in projectile_list:
                if projectile_proof == False and ((PLAYER_ONE.x_pos >= projectile.x_pos and PLAYER_ONE.x_pos <= projectile.x_pos + 40) or (PLAYER_ONE.x_pos + 25 >= projectile.x_pos and PLAYER_ONE.x_pos + 25 <= projectile.x_pos + 40) or (PLAYER_ONE.x_pos + 50 >= projectile.x_pos and PLAYER_ONE.x_pos + 50 <= projectile.x_pos + 40)) and PLAYER_ONE.y_pos <= projectile.y_pos and PLAYER_ONE.y_pos >= projectile.y_pos - 40 and game_over == False:
                    PROJECTILE_HIT.play()
                    PLAYER_ONE.health -= FIREBALL_DAMAGE
                    projectile_list.remove(projectile)
            # Checking for powerup collisions
            for powerup in powerup_list:
                if ((PLAYER_ONE.x_pos >= powerup.x_pos and PLAYER_ONE.x_pos <= powerup.x_pos + 40) or (PLAYER_ONE.x_pos + 25 >= powerup.x_pos and PLAYER_ONE.x_pos + 25 <= powerup.x_pos + 40) or (PLAYER_ONE.x_pos + 50 >= powerup.x_pos and PLAYER_ONE.x_pos + 50 <= powerup.x_pos + 40)) and PLAYER_ONE.y_pos <= powerup.y_pos and PLAYER_ONE.y_pos >= powerup.y_pos - 40 and game_over == False:
                    POWERUP.play()
                    if powerup.powerup == "speed":
                        speed_up = True
                        speed_index = 0
                    elif powerup.powerup == "health":
                        PLAYER_ONE.health = 100
                    elif powerup.powerup == "orb":
                        game_mode = "rescue"
                        difficulty = ""
                        # Appending current score to previous scores file
                        if high_scores == True:
                            hard_score_list.append(points)
                            with open(HARD_SAVE_FILE, "wb") as file:
                                pickle.dump(hard_score_list, file)
                    elif powerup.powerup == "ghost":
                        ghost_on = True
                        ghost_index = 0
                    elif powerup.powerup == "projectileproof":
                        projectile_proof = True
                        projectile_proof_index = 0
                    elif powerup.powerup == "freeze":
                        platforms_scrolling = False
                        platform_scrolling_index = 0
                    powerup.disabling = True
            # When player dies do this
            if PLAYER_ONE.health <= 0:
                VOLCANO_MUSIC.stop()
                projectile_list.clear()
                platform_list.clear()
                powerup_list.clear()
                game_over = True
                if can_play_drowning:
                    DROWNING.play()
                    can_play_drowning = False
                points_active = False
                SCREEN.blit(game_over_screen, (0, 0))
                text = MEDIUMFONT.render(str(points), False, (125, 0, 0))
                SCREEN.blit(text, (480, 385))
                # Reading previous scores for this difficulty
                high_score = max(hard_score_list)
                if high_score >= points:
                    text2 = SMALLFONT.render(str(high_score), False, (125, 0, 0))
                    SCREEN.blit(text2, (525, 445))
                else:
                    text2 = SMALLFONT.render(str(points), False, (125, 0, 0))
                    SCREEN.blit(text2, (525, 445))
                pygame.display.update()
                # If player clicks continue do this
                if left_click == True or CURSOR.clicked == True:
                    BUTTON_CLICKED.play()
                    # Appending current score to previous scores file
                    if high_scores == True:
                        hard_score_list.append(points)
                        with open(HARD_SAVE_FILE, "wb") as file:
                            pickle.dump(hard_score_list, file)
                    # Resetting values
                    PLAYER_ONE.x_pos = 320
                    PLAYER_ONE.y_pos = 120
                    PLAYER_ONE.health = 100
                    PLAYER_ONE.accel_index = 0
                    PLAYER_ONE.jumping = False
                    speed_index = 0
                    ghost_index = 0
                    projectile_proof_index = 0
                    platforms_scrolling_index = 0
                    speed_up = False
                    ghost_on = False
                    projectile_proof = False
                    platforms_scrolling = True
                    HARD_SCROLL_SPEED = 3.5
                    game_mode = "menu"
                    difficulty = ""
                    CURSOR.x = 320
                    CURSOR.y = 240
                    initial_blit = False
                    credits_y = 0
                    info_y = 0
                    points = 0
                    can_play_drowning = True
                    game_over = False
            # Border collision detection
            if PLAYER_ONE.x_pos >= 590:
                PLAYER_ONE.x_pos -= 10
            if PLAYER_ONE.x_pos <= 0:
                PLAYER_ONE.x_pos += 10
            if PLAYER_ONE.y_pos <= 0:
                PLAYER_ONE.y_pos += 10
            if PLAYER_ONE.y_pos >= 430:
                PLAYER_ONE.falling = False
                PLAYER_ONE.y_pos -= 10
            PLAYER_ONE.update()
            HARD_SCROLL_SPEED += 0.001
    
    # TWO-PLAYER MODE
    if game_mode == "play2":
        # LOGIC FOR TWO-PLAYER EASY
        if difficulty == "easy":
            # Getting ready to do some logic
            if pygame.mixer.get_busy() == False:
                GRASSLAND_MUSIC.play()
            points_active = True
            PLAYER_ONE.falling = True
            PLAYER_TWO.falling = True
            SCREEN.blit(grasslandbg, (0, 0))
            SCREEN.blit(water_image, (0, liquid_y))
            if frame_index >= 0 and frame_index < 4:
                SCREEN.blit(playerone0, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
                SCREEN.blit(playertwo1, (PLAYER_TWO.x_pos, PLAYER_TWO.y_pos))
            if frame_index >= 4 and frame_index < 8:
                SCREEN.blit(playerone1, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
                SCREEN.blit(playertwo2, (PLAYER_TWO.x_pos, PLAYER_TWO.y_pos))
            if frame_index >= 8 and frame_index < 12:
                SCREEN.blit(playerone2, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
                SCREEN.blit(playertwo0, (PLAYER_TWO.x_pos, PLAYER_TWO.y_pos))
            # Making some platforms
            if platforms_scrolling == True and last_platform_y >= 120 - EASY_SCROLL_SPEED:
                left_studs = random.randint(2, 16 - EASY_PLATFORM_GAP)
                right_studs = 16 - left_studs + EASY_PLATFORM_GAP
                temp_platform = Platform(0, left_studs)
                temp_platform2 = Platform(left_studs * 40 + EASY_PLATFORM_GAP * 40, right_studs)
                platform_list.append(temp_platform)
                platform_list.append(temp_platform2)
            # Making some powerups
            speed_make = random.randint(0, speed_rarity)
            if speed_make == 0 and game_over == False:
                new = Powerup("speed", random.randint(40, 600), 0)
                powerup_list.append(new)
            health_make = random.randint(0, health_rarity)
            if health_make == 0 and game_over == False:
                new = Powerup("health", random.randint(40, 600), 0)
                powerup_list.append(new)
            ghost_make = random.randint(0, ghost_rarity)
            if ghost_make == 0 and game_over == False:
                new = Powerup("ghost", random.randint(40, 600), 0)
                powerup_list.append(new)
            freeze_make = random.randint(0, freeze_rarity)
            if freeze_make == 0 and game_over == False:
                new = Powerup("freeze", random.randint(40, 600), 0)
                powerup_list.append(new)
            # Putting powerup text on the screen
            if speed_up == True:
                speed_time_left = round((300 - speed_index) / 30, 1)
                speed_text = SMALLFONT.render("Speed Up: " + str(speed_time_left), False, (0, 205, 0))
                SCREEN.blit(speed_text, (20, 80))
            if ghost_on == True:
                ghost_time_left = round((180 - ghost_index) / 30, 1)
                ghost_text = SMALLFONT.render("Ghost Platforms: " + str(ghost_time_left), False, (150, 0, 210))
                SCREEN.blit(ghost_text, (20, 120))
            if platforms_scrolling == False:
                freeze_time_left = round((120 - platforms_scrolling_index) / 30, 1)
                freeze_text = SMALLFONT.render("Liquid Freeze: " + str(freeze_time_left), False, (35, 35, 255))
                SCREEN.blit(freeze_text, (20, 200))
            # Doing some score and health logic
            text = MEDIUMFONT.render("Score: " + str(points), False, (0, 0, 0))
            SCREEN.blit(text, (20, 20))
            HEALTH_WIDTH1 = int(180 * PLAYER_ONE.health / 100)
            HEALTH_WIDTH2 = int(180 * PLAYER_TWO.health / 100)
            COLOR_VALUE1 = round(255 - PLAYER_ONE.health * 2.55)
            COLOR_VALUE2 = round(255 - PLAYER_TWO.health * 2.55)
            if COLOR_VALUE1 > 255:
                COLOR_VALUE1 = 255
            if COLOR_VALUE2 > 255:
                COLOR_VALUE2 = 255
            text3 = SMALLFONT.render("Health (1): " + str(round(PLAYER_ONE.health)), False, (COLOR_VALUE1, (255 - COLOR_VALUE1), 0))
            text4 = SMALLFONT.render("Health (2): " + str(round(PLAYER_TWO.health)), False, (COLOR_VALUE2, (255 - COLOR_VALUE2), 0))
            SCREEN.blit(text3, (320, 20))
            SCREEN.blit(text4, (320, 90))
            if PLAYER_ONE.health <= 20:
                pygame.draw.rect(SCREEN, (COLOR_VALUE1, (255 - COLOR_VALUE1), 0), pygame.Rect(325 + random.randint(1, (25 - round(PLAYER_ONE.health))), 60, HEALTH_WIDTH1, 10))
            else:
                pygame.draw.rect(SCREEN, (COLOR_VALUE1, (255 - COLOR_VALUE1), 0), pygame.Rect(325, 60, HEALTH_WIDTH1, 10))
            if PLAYER_TWO.health <= 20:
                pygame.draw.rect(SCREEN, (COLOR_VALUE2, (255 - COLOR_VALUE2), 0), pygame.Rect(325 + random.randint(1, (25 - round(PLAYER_TWO.health))), 130, HEALTH_WIDTH2, 10))
            else:
                pygame.draw.rect(SCREEN, (COLOR_VALUE2, (255 - COLOR_VALUE2), 0), pygame.Rect(325, 130, HEALTH_WIDTH2, 10))
            PLAYER_ONE.health += 0.05
            if PLAYER_ONE.health > 100:
                PLAYER_ONE.health = 100
            PLAYER_TWO.health += 0.05
            if PLAYER_TWO.health > 100:
                PLAYER_TWO.health = 100
            # COLLISION DETECTION
            # If liquid is touched subtract from health
            if PLAYER_ONE.y_pos >= liquid_y - 25 and disable_liquids == False:
                PLAYER_ONE.health -= WATER_DAMAGE
            if PLAYER_TWO.y_pos >= liquid_y - 25 and disable_liquids == False:
                PLAYER_TWO.health -= WATER_DAMAGE
            # Checking if player is above or below platform and proceed accordingly
            for platform in platform_list:
                if PLAYER_ONE.y_pos + 20 <= platform.y_pos and PLAYER_ONE.y_pos + 20 >= platform.y_pos - 20 and PLAYER_ONE.x_pos + 50 >= platform.x_pos and PLAYER_ONE.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_ONE.falling = False
                if ghost_on == False and PLAYER_ONE.y_pos + 20 >= platform.y_pos and PLAYER_ONE.y_pos <= platform.y_pos + 40 and PLAYER_ONE.x_pos + 50 >= platform.x_pos and PLAYER_ONE.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_ONE.jumping = False
                    PLAYER_ONE.falling = True
                    PLAYER_ONE.y_pos += EASY_SCROLL_SPEED
                if PLAYER_TWO.y_pos + 20 <= platform.y_pos and PLAYER_TWO.y_pos + 20 >= platform.y_pos - 20 and PLAYER_TWO.x_pos + 50 >= platform.x_pos and PLAYER_TWO.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_TWO.falling = False
                if ghost_on == False and PLAYER_TWO.y_pos + 20 >= platform.y_pos and PLAYER_TWO.y_pos <= platform.y_pos + 40 and PLAYER_TWO.x_pos + 50 >= platform.x_pos and PLAYER_TWO.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_TWO.jumping = False
                    PLAYER_TWO.falling = True
                    PLAYER_TWO.y_pos += EASY_SCROLL_SPEED
            # Checking for powerup collisions
            for powerup in powerup_list:
                if (((PLAYER_ONE.x_pos >= powerup.x_pos and PLAYER_ONE.x_pos <= powerup.x_pos + 40) or (PLAYER_ONE.x_pos + 25 >= powerup.x_pos and PLAYER_ONE.x_pos + 25 <= powerup.x_pos + 40) or (PLAYER_ONE.x_pos + 50 >= powerup.x_pos and PLAYER_ONE.x_pos + 50 <= powerup.x_pos + 40)) and PLAYER_ONE.y_pos <= powerup.y_pos and PLAYER_ONE.y_pos >= powerup.y_pos - 40) or (((PLAYER_TWO.x_pos >= powerup.x_pos and PLAYER_TWO.x_pos <= powerup.x_pos + 40) or (PLAYER_TWO.x_pos + 25 >= powerup.x_pos and PLAYER_TWO.x_pos + 25 <= powerup.x_pos + 40) or (PLAYER_TWO.x_pos + 50 >= powerup.x_pos and PLAYER_TWO.x_pos + 50 <= powerup.x_pos + 40)) and PLAYER_TWO.y_pos <= powerup.y_pos and PLAYER_TWO.y_pos >= powerup.y_pos - 40) and game_over == False:
                    POWERUP.play()
                    if powerup.powerup == "speed":
                        speed_up = True
                        speed_index = 0
                    elif powerup.powerup == "health":
                        PLAYER_ONE.health = 100
                        PLAYER_TWO.health = 100
                    elif powerup.powerup == "ghost":
                        ghost_on = True
                        ghost_index = 0
                    elif powerup.powerup == "freeze":
                        platforms_scrolling = False
                        platform_scrolling_index = 0
                    powerup.disabling = True
            # When player dies do this
            if PLAYER_ONE.health <= 0 or PLAYER_TWO.health <= 0:
                GRASSLAND_MUSIC.stop()
                projectile_list.clear()
                platform_list.clear()
                powerup_list.clear()
                game_over = True
                if can_play_drowning:
                    DROWNING.play()
                    can_play_drowning = False
                points_active = False
                SCREEN.blit(player_won_screen, (0, 0))
                text = MEDIUMFONT.render(str(points), False, (125, 0, 0))
                SCREEN.blit(text, (495, 375))
                # If player one died first
                if PLAYER_ONE.health <= 0 and one_has_died == False:
                    text2 = LARGEFONT.render("2", False, (125, 0, 0))
                    one_has_died = True
                # If player two died first
                elif PLAYER_TWO.health <= 0 and one_has_died == False:
                    text2 = LARGEFONT.render("1", False, (125, 0, 0))
                    one_has_died = True
                SCREEN.blit(text2, (310, 250))
                # Reading previous scores for this difficulty
                high_score = max(easy_score_list)
                if high_score >= points:
                    text3 = SMALLFONT.render(str(high_score), False, (125, 0, 0))
                    SCREEN.blit(text3, (525, 440))
                else:
                    text3 = SMALLFONT.render(str(points), False, (125, 0, 0))
                    SCREEN.blit(text3, (525, 440))
                pygame.display.update()
                # If player clicks continue do this
                if left_click == True or CURSOR.clicked == True:
                    BUTTON_CLICKED.play()
                    # Appending current score to previous scores file
                    if high_scores == True:
                        easy_score_list.append(points)
                        with open(EASY_SAVE_FILE, "wb") as file:
                            pickle.dump(easy_score_list, file)
                    # Resetting values
                    PLAYER_ONE.x_pos = 320
                    PLAYER_ONE.y_pos = 120
                    PLAYER_ONE.health = 100
                    PLAYER_ONE.accel_index = 0
                    PLAYER_ONE.jumping = False
                    PLAYER_TWO.x_pos = 320
                    PLAYER_TWO.y_pos = 120
                    PLAYER_TWO.health = 100
                    PLAYER_TWO.accel_index = 0
                    PLAYER_TWO.jumping = False
                    speed_index = 0
                    ghost_index = 0
                    projectile_proof_index = 0
                    platforms_scrolling_index = 0
                    speed_up = False
                    ghost_on = False
                    projectile_proof = False
                    platforms_scrolling = True
                    EASY_SCROLL_SPEED = 2
                    game_mode = "menu"
                    difficulty = ""
                    CURSOR.x = 320
                    CURSOR.y = 240
                    initial_blit = False
                    credits_y = 0
                    info_y = 0
                    points = 0
                    can_play_drowning = True
                    one_has_died = False
                    game_over = False
            # Border collision detection
            if PLAYER_ONE.x_pos >= 590:
                PLAYER_ONE.x_pos -= 10
            if PLAYER_ONE.x_pos <= 0:
                PLAYER_ONE.x_pos += 10
            if PLAYER_ONE.y_pos <= 0:
                PLAYER_ONE.y_pos += 10
            if PLAYER_ONE.y_pos >= 430:
                PLAYER_ONE.falling = False
                PLAYER_ONE.y_pos -= 10
            if PLAYER_TWO.x_pos >= 590:
                PLAYER_TWO.x_pos -= 10
            if PLAYER_TWO.x_pos <= 0:
                PLAYER_TWO.x_pos += 10
            if PLAYER_TWO.y_pos <= 0:
                PLAYER_TWO.y_pos += 10
            if PLAYER_TWO.y_pos >= 430:
                PLAYER_TWO.falling = False
                PLAYER_TWO.y_pos -= 10
            PLAYER_ONE.update()
            PLAYER_TWO.update()
            EASY_SCROLL_SPEED += 0.001
        # LOGIC FOR TWO-PLAYER NORMAL
        if difficulty == "normal":
            # Getting ready to do some logic
            if pygame.mixer.get_busy() == False:
                FACILITY_MUSIC.play()
            points_active = True
            PLAYER_ONE.falling = True
            PLAYER_TWO.falling = True
            SCREEN.blit(facilitybg, (0, 0))
            SCREEN.blit(acid_image, (0, liquid_y))
            if frame_index >= 0 and frame_index < 4:
                SCREEN.blit(playerone0, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
                SCREEN.blit(playertwo1, (PLAYER_TWO.x_pos, PLAYER_TWO.y_pos))
            if frame_index >= 4 and frame_index < 8:
                SCREEN.blit(playerone1, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
                SCREEN.blit(playertwo2, (PLAYER_TWO.x_pos, PLAYER_TWO.y_pos))
            if frame_index >= 8 and frame_index < 12:
                SCREEN.blit(playerone2, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
                SCREEN.blit(playertwo0, (PLAYER_TWO.x_pos, PLAYER_TWO.y_pos))
            # Making some platforms
            if platforms_scrolling == True and last_platform_y >= 120 - NORMAL_SCROLL_SPEED:
                left_studs = random.randint(2, 16 - NORMAL_PLATFORM_GAP)
                right_studs = 16 - left_studs + NORMAL_PLATFORM_GAP
                temp_platform = Platform(0, left_studs)
                temp_platform2 = Platform(left_studs * 40 + NORMAL_PLATFORM_GAP * 40, right_studs)
                platform_list.append(temp_platform)
                platform_list.append(temp_platform2)
            # Making some projectiles
            chance_of_making = random.randint(0, NORMAL_PROJECTILE_RARITY)
            if chance_of_making == 0 and game_over == False and disable_projectiles == False:
                PROJECTILE_FIRE.play()
                new = Projectile(0, random.randint(0, 480), random.randint(2, 5))
                projectile_list.append(new)
            if chance_of_making == 1 and game_over == False and disable_projectiles == False:
                PROJECTILE_FIRE.play()
                new2 = Projectile(640, random.randint(0, 480), random.randint(-5, -2))
                projectile_list.append(new2)
            # Making some powerups
            speed_make = random.randint(0, speed_rarity)
            if speed_make == 0 and game_over == False:
                new = Powerup("speed", random.randint(40, 600), 0)
                powerup_list.append(new)
            health_make = random.randint(0, health_rarity)
            if health_make == 0 and game_over == False:
                new = Powerup("health", random.randint(40, 600), 0)
                powerup_list.append(new)
            ghost_make = random.randint(0, ghost_rarity)
            if ghost_make == 0 and game_over == False:
                new = Powerup("ghost", random.randint(40, 600), 0)
                powerup_list.append(new)
            projectile_proof_make = random.randint(0, projectile_proof_rarity)
            if projectile_proof_make == 0 and game_over == False:
                new = Powerup("projectileproof", random.randint(40, 600), 0)
                powerup_list.append(new)
            freeze_make = random.randint(0, freeze_rarity)
            if freeze_make == 0 and game_over == False:
                new = Powerup("freeze", random.randint(40, 600), 0)
                powerup_list.append(new)
            # Putting powerup text on the screen
            if speed_up == True:
                speed_time_left = round((300 - speed_index) / 30, 1)
                speed_text = SMALLFONT.render("Speed Up: " + str(speed_time_left), False, (0, 205, 0))
                SCREEN.blit(speed_text, (20, 80))
            if ghost_on == True:
                ghost_time_left = round((180 - ghost_index) / 30, 1)
                ghost_text = SMALLFONT.render("Ghost Platforms: " + str(ghost_time_left), False, (150, 0, 210))
                SCREEN.blit(ghost_text, (20, 120))
            if projectile_proof == True:
                projectile_time_left = round((300 - projectile_proof_index) / 30, 1)
                projectile_text = SMALLFONT.render("Projectile Proof: " + str(projectile_time_left), False, (230, 140, 0))
                SCREEN.blit(projectile_text, (20, 160))
            if platforms_scrolling == False:
                freeze_time_left = round((120 - platforms_scrolling_index) / 30, 1)
                freeze_text = SMALLFONT.render("Liquid Freeze: " + str(freeze_time_left), False, (35, 35, 255))
                SCREEN.blit(freeze_text, (20, 200))
            # Doing some score and health logic
            text = MEDIUMFONT.render("Score: " + str(points), False, (0, 0, 0))
            SCREEN.blit(text, (20, 20))
            HEALTH_WIDTH1 = int(180 * PLAYER_ONE.health / 100)
            HEALTH_WIDTH2 = int(180 * PLAYER_TWO.health / 100)
            COLOR_VALUE1 = round(255 - PLAYER_ONE.health * 2.55)
            COLOR_VALUE2 = round(255 - PLAYER_TWO.health * 2.55)
            if COLOR_VALUE1 > 255:
                COLOR_VALUE1 = 255
            if COLOR_VALUE2 > 255:
                COLOR_VALUE2 = 255
            text3 = SMALLFONT.render("Health (1): " + str(round(PLAYER_ONE.health)), False, (COLOR_VALUE1, (255 - COLOR_VALUE1), 0))
            text4 = SMALLFONT.render("Health (2): " + str(round(PLAYER_TWO.health)), False, (COLOR_VALUE2, (255 - COLOR_VALUE2), 0))
            SCREEN.blit(text3, (320, 20))
            SCREEN.blit(text4, (320, 90))
            if PLAYER_ONE.health <= 20:
                pygame.draw.rect(SCREEN, (COLOR_VALUE1, (255 - COLOR_VALUE1), 0), pygame.Rect(325 + random.randint(1, (25 - round(PLAYER_ONE.health))), 60, HEALTH_WIDTH1, 10))
            else:
                pygame.draw.rect(SCREEN, (COLOR_VALUE1, (255 - COLOR_VALUE1), 0), pygame.Rect(325, 60, HEALTH_WIDTH1, 10))
            if PLAYER_TWO.health <= 20:
                pygame.draw.rect(SCREEN, (COLOR_VALUE2, (255 - COLOR_VALUE2), 0), pygame.Rect(325 + random.randint(1, (25 - round(PLAYER_TWO.health))), 130, HEALTH_WIDTH2, 10))
            else:
                pygame.draw.rect(SCREEN, (COLOR_VALUE2, (255 - COLOR_VALUE2), 0), pygame.Rect(325, 130, HEALTH_WIDTH2, 10))
            PLAYER_ONE.health += 0.03
            if PLAYER_ONE.health > 100:
                PLAYER_ONE.health = 100
            PLAYER_TWO.health += 0.03
            if PLAYER_TWO.health > 100:
                PLAYER_TWO.health = 100
            # COLLISION DETECTION
            # If liquid is touched subtract from health
            if PLAYER_ONE.y_pos >= liquid_y - 25 and disable_liquids == False:
                PLAYER_ONE.health -= ACID_DAMAGE
            if PLAYER_TWO.y_pos >= liquid_y - 25 and disable_liquids == False:
                PLAYER_TWO.health -= ACID_DAMAGE
            # Checking if player is above or below platform and proceed accordingly
            for platform in platform_list:
                if PLAYER_ONE.y_pos + 20 <= platform.y_pos and PLAYER_ONE.y_pos + 20 >= platform.y_pos - 20 and PLAYER_ONE.x_pos + 50 >= platform.x_pos and PLAYER_ONE.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_ONE.falling = False
                if ghost_on == False and PLAYER_ONE.y_pos + 20 >= platform.y_pos and PLAYER_ONE.y_pos <= platform.y_pos + 40 and PLAYER_ONE.x_pos + 50 >= platform.x_pos and PLAYER_ONE.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_ONE.jumping = False
                    PLAYER_ONE.falling = True
                    PLAYER_ONE.y_pos += NORMAL_SCROLL_SPEED
                if PLAYER_TWO.y_pos + 20 <= platform.y_pos and PLAYER_TWO.y_pos + 20 >= platform.y_pos - 20 and PLAYER_TWO.x_pos + 50 >= platform.x_pos and PLAYER_TWO.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_TWO.falling = False
                if ghost_on == False and PLAYER_TWO.y_pos + 20 >= platform.y_pos and PLAYER_TWO.y_pos <= platform.y_pos + 40 and PLAYER_TWO.x_pos + 50 >= platform.x_pos and PLAYER_TWO.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_TWO.jumping = False
                    PLAYER_TWO.falling = True
                    PLAYER_TWO.y_pos += NORMAL_SCROLL_SPEED
            # Checking for projectile collisions
            for projectile in projectile_list:
                if projectile_proof == False and ((PLAYER_ONE.x_pos >= projectile.x_pos and PLAYER_ONE.x_pos <= projectile.x_pos + 40) or (PLAYER_ONE.x_pos + 25 >= projectile.x_pos and PLAYER_ONE.x_pos + 25 <= projectile.x_pos + 40) or (PLAYER_ONE.x_pos + 50 >= projectile.x_pos and PLAYER_ONE.x_pos + 50 <= projectile.x_pos + 40)) and PLAYER_ONE.y_pos <= projectile.y_pos and PLAYER_ONE.y_pos >= projectile.y_pos - 40 and game_over == False:
                    PROJECTILE_HIT.play()
                    PLAYER_ONE.health -= BULLET_DAMAGE
                    try:
                        projectile_list.remove(projectile)
                    except:
                        pass
                if projectile_proof == False and ((PLAYER_TWO.x_pos >= projectile.x_pos and PLAYER_TWO.x_pos <= projectile.x_pos + 40) or (PLAYER_TWO.x_pos + 25 >= projectile.x_pos and PLAYER_TWO.x_pos + 25 <= projectile.x_pos + 40) or (PLAYER_TWO.x_pos + 50 >= projectile.x_pos and PLAYER_TWO.x_pos + 50 <= projectile.x_pos + 40)) and PLAYER_TWO.y_pos <= projectile.y_pos and PLAYER_TWO.y_pos >= projectile.y_pos - 40 and game_over == False:
                    PROJECTILE_HIT.play()
                    PLAYER_TWO.health -= BULLET_DAMAGE
                    try:
                        projectile_list.remove(projectile)
                    except:
                        pass
            # Checking for powerup collisions
            for powerup in powerup_list:
                if (((PLAYER_ONE.x_pos >= powerup.x_pos and PLAYER_ONE.x_pos <= powerup.x_pos + 40) or (PLAYER_ONE.x_pos + 25 >= powerup.x_pos and PLAYER_ONE.x_pos + 25 <= powerup.x_pos + 40) or (PLAYER_ONE.x_pos + 50 >= powerup.x_pos and PLAYER_ONE.x_pos + 50 <= powerup.x_pos + 40)) and PLAYER_ONE.y_pos <= powerup.y_pos and PLAYER_ONE.y_pos >= powerup.y_pos - 40) or (((PLAYER_TWO.x_pos >= powerup.x_pos and PLAYER_TWO.x_pos <= powerup.x_pos + 40) or (PLAYER_TWO.x_pos + 25 >= powerup.x_pos and PLAYER_TWO.x_pos + 25 <= powerup.x_pos + 40) or (PLAYER_TWO.x_pos + 50 >= powerup.x_pos and PLAYER_TWO.x_pos + 50 <= powerup.x_pos + 40)) and PLAYER_TWO.y_pos <= powerup.y_pos and PLAYER_TWO.y_pos >= powerup.y_pos - 40) and game_over == False:
                    POWERUP.play()
                    if powerup.powerup == "speed":
                        speed_up = True
                        speed_index = 0
                    elif powerup.powerup == "health":
                        PLAYER_ONE.health = 100
                        PLAYER_TWO.health = 100
                    elif powerup.powerup == "ghost":
                        ghost_on = True
                        ghost_index = 0
                    elif powerup.powerup == "projectileproof":
                        projectile_proof = True
                        projectile_proof_index = 0
                    elif powerup.powerup == "freeze":
                        platforms_scrolling = False
                        platform_scrolling_index = 0
                    powerup.disabling = True
            # When player dies do this
            if PLAYER_ONE.health <= 0 or PLAYER_TWO.health <= 0:
                FACILITY_MUSIC.stop()
                projectile_list.clear()
                platform_list.clear()
                powerup_list.clear()
                game_over = True
                if can_play_drowning:
                    DROWNING.play()
                    can_play_drowning = False
                points_active = False
                SCREEN.blit(player_won_screen, (0, 0))
                text = MEDIUMFONT.render(str(points), False, (125, 0, 0))
                SCREEN.blit(text, (495, 375))
                # If player one died first
                if PLAYER_ONE.health <= 0 and one_has_died == False:
                    text2 = LARGEFONT.render("2", False, (125, 0, 0))
                    one_has_died = True
                # If player two died first
                elif PLAYER_TWO.health <= 0 and one_has_died == False:
                    text2 = LARGEFONT.render("1", False, (125, 0, 0))
                    one_has_died = True
                SCREEN.blit(text2, (310, 250))
                # Reading previous scores for this difficulty
                high_score = max(normal_score_list)
                if high_score >= points:
                    text3 = SMALLFONT.render(str(high_score), False, (125, 0, 0))
                    SCREEN.blit(text3, (525, 445))
                else:
                    text3 = SMALLFONT.render(str(points), False, (125, 0, 0))
                    SCREEN.blit(text3, (525, 445))
                pygame.display.update()
                # If player clicks continue do this
                if left_click == True or CURSOR.clicked == True:
                    BUTTON_CLICKED.play()
                    # Appending current score to previous scores file
                    if high_scores == True:
                        normal_score_list.append(points)
                        with open(NORMAL_SAVE_FILE, "wb") as file:
                            pickle.dump(normal_score_list, file)
                    # Resetting values
                    PLAYER_ONE.x_pos = 320
                    PLAYER_ONE.y_pos = 120
                    PLAYER_ONE.health = 100
                    PLAYER_ONE.accel_index = 0
                    PLAYER_ONE.jumping = False
                    PLAYER_TWO.x_pos = 320
                    PLAYER_TWO.y_pos = 120
                    PLAYER_TWO.health = 100
                    PLAYER_TWO.accel_index = 0
                    PLAYER_TWO.jumping = False
                    speed_index = 0
                    ghost_index = 0
                    projectile_proof_index = 0
                    platforms_scrolling_index = 0
                    speed_up = False
                    ghost_on = False
                    projectile_proof = False
                    platforms_scrolling = True
                    NORMAL_SCROLL_SPEED = 2.75
                    game_mode = "menu"
                    difficulty = ""
                    CURSOR.x = 320
                    CURSOR.y = 240
                    initial_blit = False
                    credits_y = 0
                    info_y = 0
                    points = 0
                    can_play_drowning = True
                    one_has_died = False
                    game_over = False
            # Border collision detection
            if PLAYER_ONE.x_pos >= 590:
                PLAYER_ONE.x_pos -= 10
            if PLAYER_ONE.x_pos <= 0:
                PLAYER_ONE.x_pos += 10
            if PLAYER_ONE.y_pos <= 0:
                PLAYER_ONE.y_pos += 10
            if PLAYER_ONE.y_pos >= 430:
                PLAYER_ONE.falling = False
                PLAYER_ONE.y_pos -= 10
            if PLAYER_TWO.x_pos >= 590:
                PLAYER_TWO.x_pos -= 10
            if PLAYER_TWO.x_pos <= 0:
                PLAYER_TWO.x_pos += 10
            if PLAYER_TWO.y_pos <= 0:
                PLAYER_TWO.y_pos += 10
            if PLAYER_TWO.y_pos >= 430:
                PLAYER_TWO.falling = False
                PLAYER_TWO.y_pos -= 10
            PLAYER_ONE.update()
            PLAYER_TWO.update()
            NORMAL_SCROLL_SPEED += 0.001
        # LOGIC FOR TWO-PLAYER HARD
        if difficulty == "hard":
            # Getting ready to do some logic
            if pygame.mixer.get_busy() == False:
                VOLCANO_MUSIC.play()
            points_active = True
            PLAYER_ONE.falling = True
            PLAYER_TWO.falling = True
            SCREEN.blit(volcanobg, (0, 0))
            SCREEN.blit(lava_image, (0, liquid_y))
            if frame_index >= 0 and frame_index < 4:
                SCREEN.blit(playerone0, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
                SCREEN.blit(playertwo1, (PLAYER_TWO.x_pos, PLAYER_TWO.y_pos))
            if frame_index >= 4 and frame_index < 8:
                SCREEN.blit(playerone1, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
                SCREEN.blit(playertwo2, (PLAYER_TWO.x_pos, PLAYER_TWO.y_pos))
            if frame_index >= 8 and frame_index < 12:
                SCREEN.blit(playerone2, (PLAYER_ONE.x_pos, PLAYER_ONE.y_pos))
                SCREEN.blit(playertwo0, (PLAYER_TWO.x_pos, PLAYER_TWO.y_pos))
            # Making some platforms
            if platforms_scrolling == True and last_platform_y >= 120 - HARD_SCROLL_SPEED:
                left_studs = random.randint(2, 16 - HARD_PLATFORM_GAP)
                right_studs = 16 - left_studs + HARD_PLATFORM_GAP
                temp_platform = Platform(0, left_studs)
                temp_platform2 = Platform(left_studs * 40 + HARD_PLATFORM_GAP * 40, right_studs)
                platform_list.append(temp_platform)
                platform_list.append(temp_platform2)
            # Making some projectiles
            chance_of_making = random.randint(0, HARD_PROJECTILE_RARITY)
            if chance_of_making == 0 and game_over == False and disable_projectiles == False:
                PROJECTILE_FIRE.play()
                new = Projectile(0, random.randint(0, 480), random.randint(2, 5))
                projectile_list.append(new)
            if chance_of_making == 1 and game_over == False and disable_projectiles == False:
                PROJECTILE_FIRE.play()
                new2 = Projectile(640, random.randint(0, 480), random.randint(-5, -2))
                projectile_list.append(new2)
            # Making some powerups
            speed_make = random.randint(0, speed_rarity)
            if speed_make == 0 and game_over == False:
                new = Powerup("speed", random.randint(40, 600), 0)
                powerup_list.append(new)
            health_make = random.randint(0, health_rarity)
            if health_make == 0 and game_over == False:
                new = Powerup("health", random.randint(40, 600), 0)
                powerup_list.append(new)
            orb_make = random.randint(0, orb_rarity)
            if orb_make == 0 and game_over == False:
                new = Powerup("orb", random.randint(40, 600), 0)
                powerup_list.append(new)
            ghost_make = random.randint(0, ghost_rarity)
            if ghost_make == 0 and game_over == False:
                new = Powerup("ghost", random.randint(40, 600), 0)
                powerup_list.append(new)
            projectile_proof_make = random.randint(0, projectile_proof_rarity)
            if projectile_proof_make == 0 and game_over == False:
                new = Powerup("projectileproof", random.randint(40, 600), 0)
                powerup_list.append(new)
            freeze_make = random.randint(0, freeze_rarity)
            if freeze_make == 0 and game_over == False:
                new = Powerup("freeze", random.randint(40, 600), 0)
                powerup_list.append(new)
            # Putting powerup text on the screen
            if speed_up == True:
                speed_time_left = round((300 - speed_index) / 30, 1)
                speed_text = SMALLFONT.render("Speed Up: " + str(speed_time_left), False, (0, 205, 0))
                SCREEN.blit(speed_text, (20, 80))
            if ghost_on == True:
                ghost_time_left = round((180 - ghost_index) / 30, 1)
                ghost_text = SMALLFONT.render("Ghost Platforms: " + str(ghost_time_left), False, (150, 0, 210))
                SCREEN.blit(ghost_text, (20, 120))
            if projectile_proof == True:
                projectile_time_left = round((300 - projectile_proof_index) / 30, 1)
                projectile_text = SMALLFONT.render("Projectile Proof: " + str(projectile_time_left), False, (230, 140, 0))
                SCREEN.blit(projectile_text, (20, 160))
            if platforms_scrolling == False:
                freeze_time_left = round((120 - platforms_scrolling_index) / 30, 1)
                freeze_text = SMALLFONT.render("Liquid Freeze: " + str(freeze_time_left), False, (35, 35, 255))
                SCREEN.blit(freeze_text, (20, 200))
            # Doing some score and health logic
            text = MEDIUMFONT.render("Score: " + str(points), False, (0, 0, 0))
            SCREEN.blit(text, (20, 20))
            HEALTH_WIDTH1 = int(180 * PLAYER_ONE.health / 100)
            HEALTH_WIDTH2 = int(180 * PLAYER_TWO.health / 100)
            COLOR_VALUE1 = round(255 - PLAYER_ONE.health * 2.55)
            COLOR_VALUE2 = round(255 - PLAYER_TWO.health * 2.55)
            if COLOR_VALUE1 > 255:
                COLOR_VALUE1 = 255
            if COLOR_VALUE2 > 255:
                COLOR_VALUE2 = 255
            text3 = SMALLFONT.render("Health (1): " + str(round(PLAYER_ONE.health)), False, (COLOR_VALUE1, (255 - COLOR_VALUE1), 0))
            text4 = SMALLFONT.render("Health (2): " + str(round(PLAYER_TWO.health)), False, (COLOR_VALUE2, (255 - COLOR_VALUE2), 0))
            SCREEN.blit(text3, (320, 20))
            SCREEN.blit(text4, (320, 90))
            if PLAYER_ONE.health <= 20:
                pygame.draw.rect(SCREEN, (COLOR_VALUE1, (255 - COLOR_VALUE1), 0), pygame.Rect(325 + random.randint(1, (25 - round(PLAYER_ONE.health))), 60, HEALTH_WIDTH1, 10))
            else:
                pygame.draw.rect(SCREEN, (COLOR_VALUE1, (255 - COLOR_VALUE1), 0), pygame.Rect(325, 60, HEALTH_WIDTH1, 10))
            if PLAYER_TWO.health <= 20:
                pygame.draw.rect(SCREEN, (COLOR_VALUE2, (255 - COLOR_VALUE2), 0), pygame.Rect(325 + random.randint(1, (25 - round(PLAYER_TWO.health))), 130, HEALTH_WIDTH2, 10))
            else:
                pygame.draw.rect(SCREEN, (COLOR_VALUE2, (255 - COLOR_VALUE2), 0), pygame.Rect(325, 130, HEALTH_WIDTH2, 10))
            PLAYER_ONE.health += 0.02
            if PLAYER_ONE.health > 100:
                PLAYER_ONE.health = 100
            PLAYER_TWO.health += 0.02
            if PLAYER_TWO.health > 100:
                PLAYER_TWO.health = 100
            # COLLISION DETECTION
            # If liquid is touched subtract from health
            if PLAYER_ONE.y_pos >= liquid_y - 25 and disable_liquids == False:
                PLAYER_ONE.health -= LAVA_DAMAGE
            if PLAYER_TWO.y_pos >= liquid_y - 25 and disable_liquids == False:
                PLAYER_TWO.health -= LAVA_DAMAGE
            # Checking if player is above or below platform and proceed accordingly
            for platform in platform_list:
                if PLAYER_ONE.y_pos + 20 <= platform.y_pos and PLAYER_ONE.y_pos + 20 >= platform.y_pos - 20 and PLAYER_ONE.x_pos + 50 >= platform.x_pos and PLAYER_ONE.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_ONE.falling = False
                if ghost_on == False and PLAYER_ONE.y_pos + 20 >= platform.y_pos and PLAYER_ONE.y_pos <= platform.y_pos + 40 and PLAYER_ONE.x_pos + 50 >= platform.x_pos and PLAYER_ONE.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_ONE.jumping = False
                    PLAYER_ONE.falling = True
                    PLAYER_ONE.y_pos += HARD_SCROLL_SPEED
                if PLAYER_TWO.y_pos + 20 <= platform.y_pos and PLAYER_TWO.y_pos + 20 >= platform.y_pos - 20 and PLAYER_TWO.x_pos + 50 >= platform.x_pos and PLAYER_TWO.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_TWO.falling = False
                if ghost_on == False and PLAYER_TWO.y_pos + 20 >= platform.y_pos and PLAYER_TWO.y_pos <= platform.y_pos + 40 and PLAYER_TWO.x_pos + 50 >= platform.x_pos and PLAYER_TWO.x_pos <= platform.x_pos + platform.studs * 40:
                    PLAYER_TWO.jumping = False
                    PLAYER_TWO.falling = True
                    PLAYER_TWO.y_pos += HARD_SCROLL_SPEED
            # Checking for projectile collisions
            for projectile in projectile_list:
                if projectile_proof == False and ((PLAYER_ONE.x_pos >= projectile.x_pos and PLAYER_ONE.x_pos <= projectile.x_pos + 40) or (PLAYER_ONE.x_pos + 25 >= projectile.x_pos and PLAYER_ONE.x_pos + 25 <= projectile.x_pos + 40) or (PLAYER_ONE.x_pos + 50 >= projectile.x_pos and PLAYER_ONE.x_pos + 50 <= projectile.x_pos + 40)) and PLAYER_ONE.y_pos <= projectile.y_pos and PLAYER_ONE.y_pos >= projectile.y_pos - 40 and game_over == False:
                    PROJECTILE_HIT.play()
                    PLAYER_ONE.health -= FIREBALL_DAMAGE
                    try:
                        projectile_list.remove(projectile)
                    except:
                        pass
                if projectile_proof == False and ((PLAYER_TWO.x_pos >= projectile.x_pos and PLAYER_TWO.x_pos <= projectile.x_pos + 40) or (PLAYER_TWO.x_pos + 25 >= projectile.x_pos and PLAYER_TWO.x_pos + 25 <= projectile.x_pos + 40) or (PLAYER_TWO.x_pos + 50 >= projectile.x_pos and PLAYER_TWO.x_pos + 50 <= projectile.x_pos + 40)) and PLAYER_TWO.y_pos <= projectile.y_pos and PLAYER_TWO.y_pos >= projectile.y_pos - 40 and game_over == False:
                    PROJECTILE_HIT.play()
                    PLAYER_TWO.health -= FIREBALL_DAMAGE
                    try:
                        projectile_list.remove(projectile)
                    except:
                        pass
            # Checking for powerup collisions
            for powerup in powerup_list:
                if (((PLAYER_ONE.x_pos >= powerup.x_pos and PLAYER_ONE.x_pos <= powerup.x_pos + 40) or (PLAYER_ONE.x_pos + 25 >= powerup.x_pos and PLAYER_ONE.x_pos + 25 <= powerup.x_pos + 40) or (PLAYER_ONE.x_pos + 50 >= powerup.x_pos and PLAYER_ONE.x_pos + 50 <= powerup.x_pos + 40)) and PLAYER_ONE.y_pos <= powerup.y_pos and PLAYER_ONE.y_pos >= powerup.y_pos - 40) or (((PLAYER_TWO.x_pos >= powerup.x_pos and PLAYER_TWO.x_pos <= powerup.x_pos + 40) or (PLAYER_TWO.x_pos + 25 >= powerup.x_pos and PLAYER_TWO.x_pos + 25 <= powerup.x_pos + 40) or (PLAYER_TWO.x_pos + 50 >= powerup.x_pos and PLAYER_TWO.x_pos + 50 <= powerup.x_pos + 40)) and PLAYER_TWO.y_pos <= powerup.y_pos and PLAYER_TWO.y_pos >= powerup.y_pos - 40) and game_over == False:
                    POWERUP.play()
                    if powerup.powerup == "speed":
                        speed_up = True
                        speed_index = 0
                    elif powerup.powerup == "health":
                        PLAYER_ONE.health = 100
                        PLAYER_TWO.health = 100
                    elif powerup.powerup == "orb":
                        game_mode = "rescue"
                        difficulty = ""
                        # Appending current score to previous scores file
                        if high_scores == True:
                            hard_score_list.append(points)
                            with open(HARD_SAVE_FILE, "wb") as file:
                                pickle.dump(hard_score_list, file)
                    elif powerup.powerup == "ghost":
                        ghost_on = True
                        ghost_index = 0
                    elif powerup.powerup == "projectileproof":
                        projectile_proof = True
                        projectile_proof_index = 0
                    elif powerup.powerup == "freeze":
                        platforms_scrolling = False
                        platform_scrolling_index = 0
                    powerup.disabling = True
            # When player dies do this
            if PLAYER_ONE.health <= 0 or PLAYER_TWO.health <= 0:
                VOLCANO_MUSIC.stop()
                projectile_list.clear()
                platform_list.clear()
                powerup_list.clear()
                game_over = True
                if can_play_drowning:
                    DROWNING.play()
                    can_play_drowning = False
                points_active = False
                SCREEN.blit(player_won_screen, (0, 0))
                text = MEDIUMFONT.render(str(points), False, (125, 0, 0))
                SCREEN.blit(text, (495, 375))
                # If player one died first
                if PLAYER_ONE.health <= 0 and one_has_died == False:
                    text2 = LARGEFONT.render("2", False, (125, 0, 0))
                    one_has_died = True
                # If player two died first
                elif PLAYER_TWO.health <= 0 and one_has_died == False:
                    text2 = LARGEFONT.render("1", False, (125, 0, 0))
                    one_has_died = True
                SCREEN.blit(text2, (310, 250))
                # Reading previous scores for this difficulty
                high_score = max(hard_score_list)
                if high_score >= points:
                    text3 = SMALLFONT.render(str(high_score), False, (125, 0, 0))
                    SCREEN.blit(text3, (525, 445))
                else:
                    text3 = SMALLFONT.render(str(points), False, (125, 0, 0))
                    SCREEN.blit(text3, (525, 445))
                pygame.display.update()
                # If player clicks continue do this
                if left_click == True or CURSOR.clicked == True:
                    BUTTON_CLICKED.play()
                    # Appending current score to previous scores file
                    if high_scores == True:
                        hard_score_list.append(points)
                        with open(HARD_SAVE_FILE, "wb") as file:
                            pickle.dump(hard_score_list, file)
                    # Resetting values
                    PLAYER_ONE.x_pos = 320
                    PLAYER_ONE.y_pos = 120
                    PLAYER_ONE.health = 100
                    PLAYER_ONE.accel_index = 0
                    PLAYER_ONE.jumping = False
                    PLAYER_TWO.x_pos = 320
                    PLAYER_TWO.y_pos = 120
                    PLAYER_TWO.health = 100
                    PLAYER_TWO.accel_index = 0
                    PLAYER_TWO.jumping = False
                    speed_index = 0
                    ghost_index = 0
                    projectile_proof_index = 0
                    platforms_scrolling_index = 0
                    speed_up = False
                    ghost_on = False
                    projectile_proof = False
                    platforms_scrolling = True
                    HARD_SCROLL_SPEED = 3.5
                    game_mode = "menu"
                    difficulty = ""
                    CURSOR.x = 320
                    CURSOR.y = 240
                    initial_blit = False
                    credits_y = 0
                    info_y = 0
                    points = 0
                    can_play_drowning = True
                    one_has_died = False
                    game_over = False
            # Border collision detection
            if PLAYER_ONE.x_pos >= 590:
                PLAYER_ONE.x_pos -= 10
            if PLAYER_ONE.x_pos <= 0:
                PLAYER_ONE.x_pos += 10
            if PLAYER_ONE.y_pos <= 0:
                PLAYER_ONE.y_pos += 10
            if PLAYER_ONE.y_pos >= 430:
                PLAYER_ONE.falling = False
                PLAYER_ONE.y_pos -= 10
            if PLAYER_TWO.x_pos >= 590:
                PLAYER_TWO.x_pos -= 10
            if PLAYER_TWO.x_pos <= 0:
                PLAYER_TWO.x_pos += 10
            if PLAYER_TWO.y_pos <= 0:
                PLAYER_TWO.y_pos += 10
            if PLAYER_TWO.y_pos >= 430:
                PLAYER_TWO.falling = False
                PLAYER_TWO.y_pos -= 10
            PLAYER_ONE.update()
            PLAYER_TWO.update()
            HARD_SCROLL_SPEED += 0.001
    
    # DIFFICULTY SELECTION FOR SINGLE-PLAYER USING NORMAL KEYBINDS
    if game_mode == "diff1" and ARCADE_MODE == False:
        if EASY_RECT.collidepoint(mouse_x, mouse_y) == True:
            SCREEN.blit(diffscreeneasy, (0, 0))
            if left_click == True or CURSOR.clicked == True:
                left_click = False
                game_mode = "play1"
                BUTTON_CLICKED.play()
                MAIN_MUSIC.stop()
                difficulty = "easy"
        elif NORMAL_RECT.collidepoint(mouse_x, mouse_y) == True:
            SCREEN.blit(diffscreennormal, (0, 0))
            if left_click == True or CURSOR.clicked == True:
                left_click = False
                game_mode = "play1"
                BUTTON_CLICKED.play()
                MAIN_MUSIC.stop()
                difficulty = "normal"
        elif HARD_RECT.collidepoint(mouse_x, mouse_y) == True:
            SCREEN.blit(diffscreenhard, (0, 0))
            if left_click == True or CURSOR.clicked == True:
                left_click = False
                game_mode = "play1"
                BUTTON_CLICKED.play()
                MAIN_MUSIC.stop()
                difficulty = "hard"
        else:
            SCREEN.blit(diffscreen, (0, 0))
            
    # DIFFICULTY SELECTION FOR SINGLE-PLAYER USING ARCADE CABINET KEYBINDS
    if game_mode == "diff1" and ARCADE_MODE == True:
        if EASY_RECT.collidepoint(CURSOR.x, CURSOR.y) == True:
            SCREEN.blit(diffscreeneasy, (0, 0))
            if CURSOR.clicked == True:
                CURSOR.clicked = False
                game_mode = "play1"
                BUTTON_CLICKED.play()
                MAIN_MUSIC.stop()
                difficulty = "easy"
        elif NORMAL_RECT.collidepoint(CURSOR.x, CURSOR.y) == True:
            SCREEN.blit(diffscreennormal, (0, 0))
            if CURSOR.clicked == True:
                CURSOR.clicked = False
                game_mode = "play1"
                BUTTON_CLICKED.play()
                MAIN_MUSIC.stop()
                difficulty = "normal"
        elif HARD_RECT.collidepoint(CURSOR.x, CURSOR.y) == True:
            SCREEN.blit(diffscreenhard, (0, 0))
            if CURSOR.clicked == True:
                CURSOR.clicked = False
                game_mode = "play1"
                BUTTON_CLICKED.play()
                MAIN_MUSIC.stop()
                difficulty = "hard"
        else:
            SCREEN.blit(diffscreen, (0, 0))

    # DIFFICULTY SELECTION FOR TWO-PLAYER USING NORMAL KEYBINDS
    if game_mode == "diff2" and ARCADE_MODE == False:
        if EASY_RECT.collidepoint(mouse_x, mouse_y) == True:
            SCREEN.blit(diffscreeneasy, (0, 0))
            if left_click == True or CURSOR.clicked == True:
                left_click = False
                game_mode = "play2"
                BUTTON_CLICKED.play()
                MAIN_MUSIC.stop()
                difficulty = "easy"
        elif NORMAL_RECT.collidepoint(mouse_x, mouse_y) == True:
            SCREEN.blit(diffscreennormal, (0, 0))
            if left_click == True or CURSOR.clicked == True:
                left_click = False
                game_mode = "play2"
                BUTTON_CLICKED.play()
                MAIN_MUSIC.stop()
                difficulty = "normal"
        elif HARD_RECT.collidepoint(mouse_x, mouse_y) == True:
            SCREEN.blit(diffscreenhard, (0, 0))
            if left_click == True or CURSOR.clicked == True:
                left_click = False
                game_mode = "play2"
                BUTTON_CLICKED.play()
                MAIN_MUSIC.stop()
                difficulty = "hard"
        else:
            SCREEN.blit(diffscreen, (0, 0))
            
    # DIFFICULTY SELECTION FOR TWO-PLAYER USING ARCADE CABINET KEYBINDS
    if game_mode == "diff2" and ARCADE_MODE == True:
        if EASY_RECT.collidepoint(CURSOR.x, CURSOR.y) == True:
            SCREEN.blit(diffscreeneasy, (0, 0))
            if CURSOR.clicked == True:
                CURSOR.clicked = False
                game_mode = "play2"
                BUTTON_CLICKED.play()
                MAIN_MUSIC.stop()
                difficulty = "easy"
        elif NORMAL_RECT.collidepoint(CURSOR.x, CURSOR.y) == True:
            SCREEN.blit(diffscreennormal, (0, 0))
            if CURSOR.clicked == True:
                CURSOR.clicked = False
                game_mode = "play2"
                BUTTON_CLICKED.play()
                MAIN_MUSIC.stop()
                difficulty = "normal"
        elif HARD_RECT.collidepoint(CURSOR.x, CURSOR.y) == True:
            SCREEN.blit(diffscreenhard, (0, 0))
            if CURSOR.clicked == True:
                CURSOR.clicked = False
                game_mode = "play2"
                BUTTON_CLICKED.play()
                MAIN_MUSIC.stop()
                difficulty = "hard"
        else:
            SCREEN.blit(diffscreen, (0, 0))
    
    # RESCUE SCREEN
    if game_mode == "rescue":
        VOLCANO_MUSIC.stop()
        if pygame.mixer.get_busy() == False:
            ENDING_MUSIC.play()
        # Checking if player is hitting the hit button using normal keybinds
        if HIT_RECT.collidepoint(mouse_x, mouse_y) == True and hit_cooldown >= 2 and ARCADE_MODE == False:
            SCREEN.blit(volcanohit1, (0, 0))
            text = ULTRATINYFONT.render("Assume you have gained fireballing power from the orb.", False, (255, 55, 55))
            SCREEN.blit(text, (90, 440))
            if left_click == True or CURSOR.clicked == True:
                left_click = False
                PROJECTILE_FIRE.play()
                hit_cooldown = 0
                new = Projectile(100, rescue_y, 5)
                projectile_list.append(new)
        elif HIT_RECT.collidepoint(mouse_x, mouse_y) == False and ARCADE_MODE == False:
            SCREEN.blit(volcanohit0, (0, 0))
            text = ULTRATINYFONT.render("Assume you have gained fireballing power from the orb.", False, (255, 55, 55))
            SCREEN.blit(text, (90, 440))
        # Changing the keybind to the right arrow key in case we are using arcade cabinet keybinds
        if arcade_hit == False and ARCADE_MODE == True:
            SCREEN.blit(volcanobg, (0, 0))
            text = TINYFONT.render("Use the right movement to shoot fireballs.", False, (255, 55, 55))
            SCREEN.blit(text, (65, 400))
            text2 = ULTRATINYFONT.render("Assume you have gained fireballing power from the orb.", False, (255, 55, 55))
            SCREEN.blit(text2, (90, 440))
        if arcade_hit == True and hit_cooldown >= 2 and ARCADE_MODE == True:
            arcade_hit = False
            PROJECTILE_FIRE.play()
            hit_cooldown = 0
            new = Projectile(100, rescue_y, 5)
            projectile_list.append(new)
        if frame_index >= 0 and frame_index < 4:
            SCREEN.blit(playerone0, (60, rescue_y))
        if frame_index >= 4 and frame_index < 8:
            SCREEN.blit(playerone1, (60, rescue_y))
        if frame_index >= 8 and frame_index < 12:
            SCREEN.blit(playerone2, (60, rescue_y))
        if frame_index >= 0 and frame_index < 6:
            SCREEN.blit(boss0, (500, boss_y))
        if frame_index >= 6 and frame_index < 12:
            SCREEN.blit(boss1, (500, boss_y))
        boss_health += 0.8 * (2 - boss_health/10000)
        if boss_health > 10000:
            boss_health = 10000
        rescue_health += 0.02
        if rescue_health > 100:
            rescue_health = 100
        # Doing some health logic for player
        HEALTH_WIDTH = int(240 * rescue_health / 100)
        COLOR_VALUE = round(255 - rescue_health * 2.55)
        if COLOR_VALUE > 255:
            COLOR_VALUE = 255
        text = SMALLFONT.render("Player Health: " + str(round(rescue_health)), False, (COLOR_VALUE, (255 - COLOR_VALUE), 0))
        SCREEN.blit(text, (20, 20))
        if rescue_health <= 20:
            pygame.draw.rect(SCREEN, (COLOR_VALUE, (255 - COLOR_VALUE), 0), pygame.Rect(25 + random.randint(1, (25 - round(rescue_health))), 60, HEALTH_WIDTH, 20))
        else:
            pygame.draw.rect(SCREEN, (COLOR_VALUE, (255 - COLOR_VALUE), 0), pygame.Rect(25, 60, HEALTH_WIDTH, 20))
        # Doing some health logic for boss
        HEALTH_WIDTH = int(240 * boss_health / 10000)
        COLOR_VALUE = round(255 - boss_health * 0.0255)
        if COLOR_VALUE > 255:
            COLOR_VALUE = 255
        text = SMALLFONT.render("Boss Health: " + str(round(boss_health)), False, (COLOR_VALUE, (255 - COLOR_VALUE), 0))
        SCREEN.blit(text, (340, 20))
        if boss_health <= 2000:
            pygame.draw.rect(SCREEN, (COLOR_VALUE, (255 - COLOR_VALUE), 0), pygame.Rect(345 + random.randint(1, (25 - round(boss_health/100))), 60, HEALTH_WIDTH, 20))
        else:
            pygame.draw.rect(SCREEN, (COLOR_VALUE, (255 - COLOR_VALUE), 0), pygame.Rect(345, 60, HEALTH_WIDTH, 20))
        # Collision detection for fireballs hitting boss
        for projectile in projectile_list:
            if 525 >= projectile.x_pos and 525 <= projectile.x_pos + 40 and boss_y <= projectile.y_pos and boss_y >= projectile.y_pos - 80:
                PROJECTILE_HIT.play()
                boss_health -= FIREBALL_DAMAGE
                projectile_list.remove(projectile)
        # Collision detection for fireballs hitting player
        for projectile in projectile_list:
            if 85 >= projectile.x_pos and 85 <= projectile.x_pos + 40 and rescue_y <= projectile.y_pos and rescue_y >= projectile.y_pos - 40:
                PROJECTILE_HIT.play()
                rescue_health -= BULLET_DAMAGE
                projectile_list.remove(projectile)
        # Making random projectiles to hit player
        fireball_make = random.randint(0, BOSS_FIREBALL_RARITY)
        if fireball_make == 0:
            PROJECTILE_FIRE.play()
            new = Projectile(460, boss_y + random.randint(0, 120), -5)
            projectile_list.append(new)
        # Checking if player is dead
        if rescue_health <= 0:
            game_mode = "tryagain"
        # Checking if boss is dead
        if boss_health <= 0:
            number_of_wins += 1
            if high_scores == True:
                with open(NUMBER_OF_WINS_SAVE_FILE, "wb") as file:
                    pickle.dump(number_of_wins, file)
            YOU_WIN.play()
            game_mode = "youwon"
    
    # If the player was defeated in the boss battle
    if game_mode == "tryagain":
        SCREEN.blit(volcanobg, (0, 0))
        SCREEN.blit(playerone0, (200, 200))
        SCREEN.blit(boss1, (370, 160))
        text = SMALLFONT.render("You died!", False, (255, 55, 55))
        SCREEN.blit(text, (250, 60))
        text2 = TINYFONT.render("Better luck next time.", False, (255, 55, 55))
        SCREEN.blit(text2, (200, 100))
        text4 = TINYFONT.render("Click escape to return to menu.", False, (255, 55, 55))
        SCREEN.blit(text4, (135, 360))
    
    # If the player won the boss battle
    if game_mode == "youwon":
        SCREEN.blit(volcanobg, (0, 0))
        SCREEN.blit(playerone0, (200, 200))
        SCREEN.blit(playertwo0, (250, 200))
        SCREEN.blit(deadboss, (370, 160))
        text = TINYFONT.render("You have beaten the game!", False, (255, 55, 55))
        SCREEN.blit(text, (160, 60))
        text2 = TINYFONT.render("Player 1 and Player 2 are re-united.", False, (255, 55, 55))
        SCREEN.blit(text2, (110, 100))
        text3 = TINYFONT.render("Not many people have achieved this! Props to you.", False, (255, 55, 55))
        SCREEN.blit(text3, (20, 320))
        text4 = TINYFONT.render("Save this page. Click escape to return to menu.", False, (255, 55, 55))
        SCREEN.blit(text4, (45, 360))
      
    # CREDITS SCREEN
    if game_mode == "credits":
        SCREEN.blit(credits_image, (0, credits_y))
        credits_y -= CREDITS_SCROLL_SPEED
        if credits_y <= -360:
            credits_y = 0
            CREDITS_MUSIC.stop()
            game_mode = "menu"

    # INFO SCREEN
    if game_mode == "info":
        SCREEN.blit(infocard, (0, info_y))
        info_y -= CREDITS_SCROLL_SPEED
        if info_y <= -360:
            info_y = 0
            CREDITS_MUSIC.stop()
            game_mode = "menu"
    
    # PLATFORM HANDLER
    for platform in platform_list:
        if difficulty == "easy" and spawn_platforms == True:
            image = grasslandplatform
            scroll = EASY_SCROLL_SPEED
            platform.draw(SCREEN, image, scroll)
        if difficulty == "normal" and spawn_platforms == True:
            image = facilityplatform
            scroll = NORMAL_SCROLL_SPEED
            platform.draw(SCREEN, image, scroll)
        if difficulty == "hard" and spawn_platforms == True:
            image = volcanoplatform
            scroll = HARD_SCROLL_SPEED
            platform.draw(SCREEN, image, scroll)
        if platform.y_pos >= 480:
            platform_list.remove(platform)
    
    # PROJECTILE HANDLER
    for projectile in projectile_list:
        if difficulty == "normal":
            if projectile.direction == "left":
                projectile.draw(SCREEN, bulletleft)
            else:
                projectile.draw(SCREEN, bulletright)
        if difficulty == "hard" or game_mode == "rescue":
            if projectile.direction == "left":
                if frame_index >= 0 and frame_index < 4:
                    projectile.draw(SCREEN, fireballleft0)
                if frame_index >= 4 and frame_index < 8:
                    projectile.draw(SCREEN, fireballleft1)
                if frame_index >= 8 and frame_index < 12:
                    projectile.draw(SCREEN, fireballleft2)
            else:
                if frame_index >= 0 and frame_index < 4:
                    projectile.draw(SCREEN, fireballright0)
                if frame_index >= 4 and frame_index < 8:
                    projectile.draw(SCREEN, fireballright1)
                if frame_index >= 8 and frame_index < 12:
                    projectile.draw(SCREEN, fireballright2)
        if projectile.x_pos <= -60 or projectile.x_pos >= 700 or projectile.y_pos <= 0 or projectile.y_pos >= 480:
            projectile_list.remove(projectile)
        
    # POWERUP HANDLER
    for powerup in powerup_list:
        if difficulty == "easy":
            powerup.draw(SCREEN, EASY_SCROLL_SPEED)
        if difficulty == "normal":
            powerup.draw(SCREEN, NORMAL_SCROLL_SPEED)
        if difficulty == "hard":
            powerup.draw(SCREEN, HARD_SCROLL_SPEED)
        if powerup.y_pos >= 480 or powerup.current_frame >= 13:
            powerup_list.remove(powerup)
    # Timing powerup lengths
    if speed_up == True or speed_index <= 1:
        speed_index += 1
        new_rect = pygame.Rect(20, 80, 320, 40)
        rects_to_update.append(new_rect)
    if ghost_on == True or ghost_index <= 1:
        ghost_index += 1
        new_rect = pygame.Rect(20, 120, 320, 40)
        rects_to_update.append(new_rect)
    if projectile_proof == True or projectile_proof_index <= 1:
        projectile_proof_index += 1
        new_rect = pygame.Rect(20, 160, 320, 40)
        rects_to_update.append(new_rect)
    if platforms_scrolling == False or platforms_scrolling_index <= 1:
        platforms_scrolling_index += 1
        new_rect = pygame.Rect(20, 200, 320, 40)
        rects_to_update.append(new_rect)
    if speed_index >= 300:
        speed_index = 0
        speed_up = False
    if ghost_index >= 180:
        ghost_index = 0
        ghost_on = False
    if projectile_proof_index >= 300:
        projectile_proof_index = 0
        projectile_proof = False
    if platforms_scrolling_index >= 120:
        platforms_scrolling_index = 0
        platforms_scrolling = True
    
    # MANAGING THE CURSOR IN ARCADE MODE
    if cursor_mode == True and difficulty == "" and game_mode != "rescue":
        CURSOR.draw(SCREEN)

    # LIQUID CYCLE HANDLER (makes liquid move up and down)
    if liquid_cycle == 1:
        liquid_y += 1
    if liquid_cycle == 3:
        liquid_y += 2
    if liquid_cycle == 5:
        liquid_y += 3
    if liquid_cycle == 7:
        liquid_y += 4
    if liquid_cycle == 9:
        liquid_y -= 4
    if liquid_cycle == 11:
        liquid_y -= 3
    if liquid_cycle == 13:
        liquid_y -= 2
    if liquid_cycle == 15:
        liquid_y -= 1
    liquid_cycle += 1
    if liquid_cycle >= 16:
        liquid_cycle = 1
        
    # MAKING THE BOSS MOVE UP AND DOWN
    if liquid_cycle == 1:
        boss_y += 5
    if liquid_cycle == 2:
        boss_y += 7
    if liquid_cycle == 3:
        boss_y += 9
    if liquid_cycle == 4:
        boss_y += 11
    if liquid_cycle == 5:
        boss_y += 13
    if liquid_cycle == 6:
        boss_y += 15
    if liquid_cycle == 7:
        boss_y += 17
    if liquid_cycle == 8:
        boss_y -= 17
    if liquid_cycle == 9:
        boss_y -= 15
    if liquid_cycle == 10:
        boss_y -= 13
    if liquid_cycle == 11:
        boss_y -= 11
    if liquid_cycle == 12:
        boss_y -= 9
    if liquid_cycle == 13:
        boss_y -= 7
    if liquid_cycle == 14:
        boss_y -= 5
    
    # UPDATING SOME TIMING LOGIC
    frame_index += 1
    if points_active == True:
        points += 1
    hit_cooldown += 1
    if difficulty == "easy":
        last_platform_y += EASY_SCROLL_SPEED
    if difficulty == "normal":
        last_platform_y += NORMAL_SCROLL_SPEED
    if difficulty == "hard":
        last_platform_y += HARD_SCROLL_SPEED
    if last_platform_y > 120:
        last_platform_y = 0
    if frame_index >= 12:
        frame_index = 0
    
    # CALCULATING FPS
    counter += 1
    if (game_mode == "play1" or game_mode == "play2" or game_mode == "rescue") and game_over == False:
        if frame_rate > 20:
            text = TINYFONT.render("FPS: " + str(frame_rate), False, (55, 255, 55))
            SCREEN.blit(text, (535, 440))
        elif frame_rate <= 20 and frame_rate > 10:
            text = TINYFONT.render("FPS: " + str(frame_rate), False, (255, 255, 55))
            SCREEN.blit(text, (535, 440))
        elif frame_rate <= 10 and frame_rate > 0:
            text = TINYFONT.render("FPS: " + str(frame_rate), False, (255, 55, 55))
            SCREEN.blit(text, (535, 440))
    if (time.time() - start_time) > frame_rate_delay:
        frame_rate = round(counter / (time.time() - start_time))
        counter = 0
        start_time = time.time()
    
    # MAKING DIRTY RECTANGLES
    for platform in platform_list:
        new_rect = pygame.Rect(platform.x_pos, platform.y_pos, platform.studs * 40, 20)
        rects_to_update.append(new_rect)
    for powerup in powerup_list:
        new_rect = pygame.Rect(powerup.x_pos, powerup.y_pos, 24, 24)
        rects_to_update.append(new_rect)
    for projectile in projectile_list:
        new_rect = pygame.Rect(projectile.x_pos - 10, projectile.y_pos, 60, 20)
        rects_to_update.append(new_rect)
    if game_mode == "play1":
        new_rect = pygame.Rect(20, 20, 320, 80)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(320, 20, 300, 80)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(0, 360, 640, 120)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(PLAYER_ONE.x_pos - 25, PLAYER_ONE.y_pos - 25, 100, 150)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(PLAYER_TWO.x_pos - 25, PLAYER_TWO.y_pos - 25, 100, 150)
        rects_to_update.append(new_rect)
    if game_mode == "play2":
        new_rect = pygame.Rect(20, 20, 320, 80)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(320, 20, 300, 120)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(0, 360, 640, 120)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(PLAYER_ONE.x_pos - 25, PLAYER_ONE.y_pos - 25, 100, 150)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(PLAYER_TWO.x_pos - 25, PLAYER_TWO.y_pos - 25, 100, 150)
        rects_to_update.append(new_rect)
    if game_mode == "rescue":
        new_rect = pygame.Rect(20, 20, 320, 80)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(320, 20, 320, 120)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(220, 360, 200, 70)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(520, 440, 90, 30)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(0, 400, 640, 80)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(60, rescue_y - 10, 50, 70)
        rects_to_update.append(new_rect)
        new_rect = pygame.Rect(500, boss_y - 25, 80, 170)
        rects_to_update.append(new_rect)
    if game_mode == "play1" or game_mode == "play2" or game_mode == "rescue":
        if initial_blit == False:
            initial_blit = True
            if difficulty == "easy":
                SCREEN.blit(grasslandbg, (0, 0))
                pygame.display.update()
            elif difficulty == "normal":
                SCREEN.blit(facilitybg, (0, 0))
                pygame.display.update()
            elif difficulty == "hard":
                SCREEN.blit(volcanobg, (0, 0))
                pygame.display.update()
            elif game_mode == "rescue" and ARCADE_MODE == False:
                SCREEN.blit(volcanohit0, (0, 0))
                pygame.display.update()
            elif game_mode == "rescue" and ARCADE_MODE == True:
                SCREEN.blit(volcanobg, (0, 0))
                pygame.display.update()
        pygame.display.update(rects_to_update)
    else:
        pygame.display.update()
    
    # WAITING FOR FPS
    if cap_fps == True:
        CLOCK.tick(FPS)