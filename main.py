import pygame as pg
import random
import sys

from pygame.constants import K_SPACE


# Functions
"""
__________________________START__________________________

__________________________FUNCTIONS______________________
"""
def events():

    global game_active
    global bird_movement
    global bird_index
    global bird_img
    global bird_rect
    global pipe_speed


    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    
        if event.type == pg.KEYDOWN:
            if event.key == K_SPACE and game_active:
                bird_movement = 0  
                bird_movement -= 3
                flap.play()
            
            if event.key == K_SPACE and not game_active:
                game_active = True
            
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1

            else:
                bird_index = 0

            bird_img, bird_rect = bird_animation()

              
def bird_animation():

    new_bird_image = bird_frames[bird_index]
    new_bird_rect = new_bird_image.get_rect(center = (100, bird_rect.centery))

    return new_bird_image, new_bird_rect

def draw_floor():
    screen.blit(floor_img, (floor_x_pos, 425))
    screen.blit(floor_img, (floor_x_pos + 288, 425 ))

def create_pipe():
    rand_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_img.get_rect(midtop = (450, rand_pipe_pos)) 
    top_pipe = pipe_img.get_rect(midbottom = (450, rand_pipe_pos - 150))

    return bottom_pipe, top_pipe

def move_pipes(pipes):
    global pipe_speed


    for pipe in pipes:
        pipe.centerx -= pipe_speed

    visible_pipes = [pipe for pipe in pipes if pipe.right > -25 ]
    return visible_pipes

def draw_pipes(pipes): 
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_img, pipe)

        else:
            fliped_pipe = pg.transform.flip(pipe_img, False, True)
            screen.blit(fliped_pipe, pipe)


def rotate_bird(img):
    new_bird = pg.transform.rotozoom(img, -bird_movement * 3, 1)

    return new_bird

def check_collision(pipes):
    global bird_rect

    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            pipe_hit.play()
            return False
    
    if bird_rect.centery >= 425 or bird_rect.centery <= -100:
        ground_hit.play()
        return False
    

    return True    

def pipe_score_check():

    global player_can_score
    global player_score
    global reset_score
    global high_score

    player_score = reset_score

    
    for pipe in pipe_list:
        if 95 < pipe.centerx  < 105 and player_can_score:
            player_score += 1
            reset_score += 1
            point.play()
            player_can_score = False
        
        if pipe.centerx < 95:
            player_can_score = True

def update_high_score(score):
    global high_score

    if score > high_score:
        high_score = player_score

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(player_score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (140,50))
        screen.blit(score_surface, score_rect)
    
    if game_state == 'game_over': 
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (140,65))
        screen.blit(high_score_surface, high_score_rect)
    
        
            
            


"""
___________________________END___________________________
"""








"""
__________________________START__________________________

__________________________INIT___________________________
"""
# Initializing
pg.init()

# Screen
screen = pg.display.set_mode((288, 512))

# Clock
clock = pg.time.Clock()
FPS = 120

"""
___________________________END___________________________
"""









"""
__________________________START__________________________

__________________________GAME VARIABLES______________________
"""
# Background
background_img = pg.image.load(".\Resources\Assets\\background-day.png").convert()
# Floors
floor_img = pg.image.load(".\Resources\Assets\\base.png").convert()
floor_x_pos = 0
# Bird
bird_downflap = pg.image.load(".\Resources\Assets\Bird\yellowbird-downflap.png").convert_alpha()
bird_midflap = pg.image.load(".\Resources\Assets\Bird\yellowbird-midflap.png").convert_alpha()
bird_upflap = pg.image.load(".\Resources\Assets\Bird\yellowbird-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0

bird_x_pos = 100
bird_y_pos = 230
bird_movement = 0
bird_gravity = 0.09

game_active = True

bird_img = bird_frames[bird_index]
bird_rect = bird_img.get_rect(center = (100, 230))

BIRD_FLAP_TIME = 200
BIRDFLAP = pg.USEREVENT + 1
BIRDFLAP = pg.time.set_timer(BIRDFLAP, BIRD_FLAP_TIME)

# Pipe
pipe_img = pg.image.load(".\Resources\Assets\pipe-green.png")
pipe_list = []
pipe_height = [200, 300, 400]
pipe_speed = 1

PIPE_SPAWN_TIME = 1700
SPAWNPIPE = pg.USEREVENT
pg.time.set_timer(SPAWNPIPE, PIPE_SPAWN_TIME)

# Pipe speed event
PIPESPEED = pg.USEREVENT + 2
pg.time.set_timer(PIPESPEED, 10000)

# Gameover surface
game_over_img = pg.image.load(".\Resources\Assets\gameover.png")
game_over_rect = game_over_img.get_rect(center = (144, 256))

# Score system
player_score = 0
player_can_score = True
high_score = 0
reset_score = 0

game_font = pg.font.Font('freesansbold.ttf',25)


# Sounds
ground_hit = pg.mixer.Sound(".\Resources\Sounds\sfx_die.wav")
pipe_hit = pg.mixer.Sound(".\Resources\Sounds\sfx_hit.wav")
point = pg.mixer.Sound(".\Resources\Sounds\sfx_point.wav")
flap = pg.mixer.Sound(".\Resources\Sounds\sfx_wing.wav")




"""
___________________________END___________________________
"""




# Main loop
while True: 
    events()

    # Backgrounds
    screen.blit(background_img, (0, 0))

    if game_active:
        bird_movement += bird_gravity
        rotated_bird = rotate_bird(bird_img)

        bird_rect.centery += bird_movement
 
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        pipe_score_check()

        score_display("main_game")
    
    else:
        
        update_high_score(player_score)

        score_display("game_over")


        pipe_speed = 1 
        bird_rect.center = (100, 230)
        bird_movement = 0
        pipe_list.clear()
        screen.blit(game_over_img, game_over_rect)
        reset_score = 0
    


    
    # Floors
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:  
        floor_x_pos = 0    
    
    # Gameover and UI
    


    pg.display.update()
    clock.tick(FPS)

pg.quit()