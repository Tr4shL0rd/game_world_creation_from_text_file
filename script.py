import pygame
import sys
import math
import argparse
parser = argparse.ArgumentParser("script.py")
parser.add_argument("-d","--debug", action="store_true", help="debug mode",dest="debug")
parser.add_argument("-i", "--ignore", action="store_true", help="ignore errors", dest="ignore")
args = parser.parse_args()
pygame.init()
if args.ignore:
    print("IGNORING ERRORS")
if args.debug:
    print("DEBUG MODE")
# Reads map from text file
MAP = "".join(tuple(MAP.strip() for MAP in open("map.txt", "r").readlines()))
MAP_FILE = open("map.txt", "r").readline()
# gets the height of the map by getting the number of lines in the file except for the last 3 
MAP_HEIGHT = len(open("map.txt", "r").readlines()[:-3])
# gets the length of the map by getting the length of the first wall line
MAP_LENGTH = len(MAP.split(" ")[0])-1
# window size if the size of the map * 60
SCREEN_MAP_SIZE = (len(MAP_FILE)-1) * 60
SCREEN_HEIGHT   = SCREEN_MAP_SIZE # 480
SCREEN_WIDTH    = SCREEN_MAP_SIZE # SCREEN_HEIGHT * 2
MAP_SIZE        = SCREEN_HEIGHT//60 # 8
TILE_SIZE       = ((SCREEN_WIDTH) // MAP_SIZE)
FOV             = math.pi / 3
HALF_FOV        = FOV / 2

player_x = (SCREEN_WIDTH / 2) / 2
player_y = (SCREEN_WIDTH / 2) / 2
player_angle = math.pi

if MAP_LENGTH != MAP_HEIGHT:
    print("WARNING: height and length is not the same!" if not args.ignore else "NOTE: height != length")
    if not args.ignore: exit()

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
            if args.debug:
                print(f"{MAP_SIZE = }")
                print(f"{square = }")
                print(f"{row = }")
                print(f"{col = }")
                print(f"row({row}) * MAP_SIZE({MAP_SIZE}) * col({col}) = {row * MAP_SIZE + col}")
                print(f"{len(MAP) = }")
                print(f"{MAP[63] = }")
                print()
            pygame.draw.rect(
                            win,
                            (200,200,200) if MAP[square] == '#' else (100,100,100),
                            (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                        )
            if MAP[square].lower() == "x":            
                pygame.draw.rect(
                            win,
                            (255,215,0),
                            (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
                        )

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