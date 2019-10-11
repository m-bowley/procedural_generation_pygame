from Map_Generator import create_map

SCREEN_WIDTH = 10
SCREEN_HEIGHT = 8
TILE_SIZE = 32 # Dimensions of the tiles - change if neccessary

WIDTH = SCREEN_WIDTH * TILE_SIZE
HEIGHT = SCREEN_HEIGHT * TILE_SIZE

# Map variables

TILE_ACROSS = int(WIDTH/TILE_SIZE) # Use the previous variables to set a tile width
TILE_DOWN = int(HEIGHT/TILE_SIZE) # and tile height

room_tile = "sprite_00.png"
dirt_tile = "sprite_01.png"
player = "player.png"

Map = create_map()

global screen_pos
screen_pos = [0, 0]

def on_key_down(key):
    global screen_pos
    if key == key.RIGHT:
        screen_pos[0] += 1
    if key == key.LEFT:
        screen_pos[0] -= 1
    if key == key.UP:
        screen_pos[1] -= 1
    if key == key.DOWN:
        screen_pos[1] += 1
    clamp_pos(screen_pos)

def clamp_pos(pos):
    if pos[0] < 0: 
        pos[0] += 1
    if pos[0] >= len(Map) - SCREEN_WIDTH:
        pos[0] -= 1
    if pos[1] < 0: 
        pos[1] += 1
    if pos[1] >= len(Map[0]) - SCREEN_HEIGHT:
        pos[1] -= 1

def draw():
    for i in range(SCREEN_WIDTH):
        for j in range(SCREEN_HEIGHT):
            x = screen_pos[0] + i
            y = screen_pos[1] + j
            if Map[x][y] == 0:
                screen.blit(dirt_tile, (i*32, j*32))
            else:
                screen.blit(room_tile, (i*32, j*32))
    player_x = (SCREEN_WIDTH//2) * 32
    player_y = (SCREEN_HEIGHT//2) * 32
    screen.blit(player, (player_x, player_y))