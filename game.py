import pygame
import sys
import random

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
def game_floor():
    screen.blit(floor_base, (floor_x_pos,900))
    screen.blit(floor_base, (floor_x_pos + 500,900))

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    return True

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom=(700,random_pipe_pos-300))
    bottom_pipe = pipe_surface.get_rect(midtop=(700,random_pipe_pos))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes: 
        pipe.centerx -= 5
    
    return pipes

def draw_pipes(pipes):
    for pipe in pipes: 
        if pipe.bottom >= 1024:
           screen.blit(pipe_surface,pipe)
        else: 
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
def get_count(pipes):
    counter = 0
    for pipe in pipes:
        if pipe.right < 0:
            counter += 1
    return counter // 2
def get_high_score():
    with open('high_score.txt') as f:
        lines = f.readlines()
        temp = str(lines[0])
    return temp
def set_high_score(high_score):
    with open('high_score.txt') as f:
        lines = f.readlines()
        temp = int(lines[0])
        if high_score > temp:
            f = open("high_score.txt", "w")
            f.write(str(high_score))
            f.close()
pygame.init()
clock = pygame.time.Clock()
gravity = 0.25
bird_movement = 0
game_counter = 0
screen = pygame.display.set_mode((500,1000))

background = pygame.image.load("sprites/background-day.png").convert()
background = pygame.transform.scale2x(background)

bird = pygame.image.load("sprites/bluebird-midflap.png").convert_alpha()
bird_rect = bird.get_rect(center=(100,512))

floor_base = pygame.image.load("sprites/base.png").convert()
floor_base = pygame.transform.scale2x(floor_base)
floor_x_pos = 0
game_floor()
message = pygame.image.load("sprites/message.png").convert_alpha()
message = pygame.transform.scale2x(message)
game_over_rect = message.get_rect(center=(288,500))

pipe_surface = pygame.image.load('sprites/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [400,600,800]

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

game_active = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_SPACE and game_active == False:
                bird_rect.center = (100, 500)
                bird_movement = 0
                pipe_list.clear()
                game_active = True
        if event.type == SPAWNPIPE and game_active:
           pipe_list.extend(create_pipe())
    screen.blit(background, (0,0))
    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird, bird_rect)
        pipe_list = move_pipes(pipe_list)
        text_surface = my_font.render(str(get_count(pipe_list)), False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))
        game_counter = int(get_count(pipe_list))
        draw_pipes(pipe_list)
        game_active = check_collision(pipe_list)
    else:
        screen.blit(message, game_over_rect)
        temp_str = 'HIGHEST SCORE: ' + get_high_score()
        text_surface = my_font.render(temp_str, False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))
        set_high_score(game_counter)
    floor_x_pos -= 1
    game_floor()
    if floor_x_pos <= -500:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)
