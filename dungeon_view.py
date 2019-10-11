import Map_Generator

WIDTH = Map_Generator.WIDTH
HEIGHT = Map_Generator.HEIGHT

room_tile = "sprite_00.png"
dirt_tile = "sprite_01.png"

Map = Map_Generator.create_map()

def draw():
    for y in range(HEIGHT//32):
        for x in range(WIDTH//32):
            if Map[y][x] == 0:
                screen.blit(dirt_tile, (x*32, y*32))
            else:
                screen.blit(room_tile, (x*32, y*32))