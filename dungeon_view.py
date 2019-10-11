import Map_Generator

WIDTH = Map_Generator.WIDTH
HEIGHT = Map_Generator.HEIGHT

room_tile = "sprite_00.png"
dirt_tile = "sprite_01.png"

Map = Map_Generator.create_map()


def draw():
    for i in range(WIDTH//32):
        for j in range(HEIGHT//32):
            if Map[i][j] == 0:
                screen.blit(dirt_tile, (i*32, j*32))
            else:
                screen.blit(room_tile, (i*32, j*32))