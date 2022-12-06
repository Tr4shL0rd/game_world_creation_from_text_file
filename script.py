import pygame
import sys
import math


pygame.init()

MAP = "".join(tuple(MAP.strip() for MAP in open("map.txt", "r").readlines()))
map_file = open("map.txt", "r").readline()
SCREEN_MAP_SIZE= (len(map_file)-1) * 60
#print(MAP)
SCREEN_HEIGHT = SCREEN_MAP_SIZE
SCREEN_WIDTH  = SCREEN_MAP_SIZE#SCREEN_HEIGHT * 2
MAP_SIZE      = SCREEN_HEIGHT//60#8
TILE_SIZE     = ((SCREEN_WIDTH) / MAP_SIZE)
FOV           = math.pi / 3
HALF_FOV      = FOV / 2


player_x = (SCREEN_WIDTH / 2) / 2
player_y = (SCREEN_WIDTH / 2) / 2
player_angle = math.pi




# string containing the map layout
# MAP = (
#      '########'   
#      '#   ## #'
#      '#      #'
#      '#    ###'
#      '##     #'
#      '#   #  #'
#      '#   #  #'
#      '########'
# )
# game window
win = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
# window caption
pygame.display.set_caption("Raycasting")

# tick clock
clock = pygame.time.Clock()
 
def draw_map():
    # Draws the world 
    for row in     range(MAP_SIZE):
        for col in range(MAP_SIZE):
            square = row * MAP_SIZE + col
            print(square)
            print(len(MAP))
            print()
            pygame.draw.rect(
                            win,
                            (200,200,200) if MAP[square] == '#' else (100,100,100),
                            (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                        )
            #if MAP[square] == "X":            
            #    pygame.draw.rect(
            #                win,
            #                (255,215,0),
            #                (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
            #            )

    # draws player circle
    pygame.draw.circle(win, (255, 0, 0), (int(player_x),int(player_y)), 8)
    
    # draws green line in the middle front of player
    pygame.draw.line(win, (0,255,0),(player_x,player_y),(player_x - math.sin(player_angle - HALF_FOV) * 50,player_y + math.cos(player_angle - HALF_FOV) * 50),3)
    
 
forward = True
while True:
    # loops over events
    for event in pygame.event.get():
        # checks for
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
          
    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)
 
    square = row * MAP_SIZE + col
    (player_y / TILE_SIZE) * MAP_SIZE + player_x / TILE_SIZE 
    if MAP[square] == '#':
        if forward:
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5
 
     
    # updates screen to prevent player asset freezing at past positions
    pygame.draw.rect(win,(0,0,0),(0,0,SCREEN_HEIGHT,SCREEN_HEIGHT)) 
    draw_map()
    # Player controlls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_angle -= 0.1
    if keys[pygame.K_RIGHT]: player_angle += 0.1
    if keys[pygame.K_UP]:
        forward = True
        player_x += -math.sin(player_angle) * 5
        player_y += math.cos(player_angle) * 5
    if keys[pygame.K_DOWN]:
        forward = False
        player_x -= -math.sin(player_angle) * 5
        player_y -= math.cos(player_angle) * 5
    
    clock.tick(60)    
    
    fps = str(int(clock.get_fps()))
    font = pygame.font.SysFont('Monospace Regular', 30)
    textsurface = font.render(fps, False, (255,255,255))
    win.blit(textsurface,(0,0))
    pygame.display.flip()