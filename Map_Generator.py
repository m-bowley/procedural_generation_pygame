# Importing modules
import secrets # Secrets is a crypto grade randomness library - in my opinion better than random for this.
import math # For the math
from collections import namedtuple
from pygame import Rect

WIDTH = 1024
HEIGHT = 768

# Map variables
TILE_SIZE = 32 # Dimensions of the tiles - change if neccessary
TILE_ACROSS = int(WIDTH/TILE_SIZE) # Use the previous variables to set a tile width
TILE_DOWN = int(HEIGHT/TILE_SIZE) # and tile height

MAX_ROOM_SIZE = 7
MIN_ROOM_SIZE = 3
ROOM_PADDING = 2

MAP_BORDER = 1

NUMBER_OF_ROOMS = 12

Room = namedtuple('Room', ['width', 'height', 'pos_x', 'pos_y'])

def generate_room():
    rm_width = MIN_ROOM_SIZE + secrets.randbelow(MAX_ROOM_SIZE - MIN_ROOM_SIZE + 1)
    rm_height = MIN_ROOM_SIZE + secrets.randbelow(MAX_ROOM_SIZE - MIN_ROOM_SIZE + 1)

    rm_pos_x = secrets.randbelow(TILE_ACROSS - rm_width)
    if rm_pos_x < MAP_BORDER:
        rm_pos_x = MAP_BORDER
    rm_pos_y = secrets.randbelow(TILE_DOWN - rm_height)
    if rm_pos_y < MAP_BORDER:
        rm_pos_y = MAP_BORDER

    return Room(rm_width, rm_height, rm_pos_x, rm_pos_y)

def create_rooms():
    Rooms = []
    for i in range(NUMBER_OF_ROOMS):
        intersect = True
        while intersect: 
            intersect = False
            rm = generate_room()
            for other in Rooms:
                room = other[0]
                padded_pos_x = rm.pos_x - 1
                padded_pos_y = rm.pos_y - 1
                padded_width = rm.width + 3
                padded_height = rm.height + 3
                rm_1 = Rect((room.pos_x*32, room.pos_y*32), (room.width*32, room.height*32))
                rm_2 = Rect((padded_pos_x*32, padded_pos_y*32), (padded_width*32, padded_height*32))
                if rm_1.colliderect(rm_2):
                    intersect = True
        Rooms.append([rm, {"NORTH": None, "SOUTH": None, "EAST": None, "WEST": None}])
    return Rooms

def create_corridors(rm, Rooms):
    candidates = {"NORTH": None, "SOUTH": None, "EAST": None, "WEST": None}
    for other in Rooms:
        if other[0] != rm[0]:
            current_room = rm[0]
            other_room = other[0]
            left_marker = max(current_room.pos_x, other_room.pos_x)
            right_marker = min(current_room.pos_x + current_room.width, other_room.pos_x + other_room.width)
            horizontal_overlap = list(range(left_marker, right_marker))
            if len(horizontal_overlap) > 0:
                print("Overlap Found")
                vertical_corridors(candidates, other, rm, horizontal_overlap)
            top_marker = max(current_room.pos_y, other_room.pos_y)
            bottom_marker = min(current_room.pos_y + current_room.height, other_room.pos_y + other_room.height)
            vertical_overlap = list(range(top_marker, bottom_marker))
            if len(vertical_overlap) > 0:
                print("Overlap Found")
                horizontal_corridors(candidates, other, rm, vertical_overlap)
    return candidates
                

def vertical_corridors(candidates, other, rm, horizontal_overlap):
    current_room = rm[0]
    current_connections = rm[1]
    other_room = other[0]
    other_connections = other[1]
    if current_room.pos_y > other_room.pos_y and other_connections["SOUTH"] == None and current_connections["NORTH"] != 0:
        connector = candidates["NORTH"]
        if connector == None:
            candidates["NORTH"] = (other, horizontal_overlap)
            other_connections["SOUTH"] = 0
        else:
            if other_room.pos_y + other_room.height > connector[0][0].pos_y + connector[0][0].height:
                connector[0][1]["SOUTH"] = None
                candidates["NORTH"] = (other, horizontal_overlap)
                other_connections["SOUTH"] = 0
    if current_room.pos_y < other_room.pos_y and other_connections["NORTH"] == None and current_connections["SOUTH"] != 0:
        connector = candidates["SOUTH"]
        if connector == None:
            candidates["SOUTH"] = (other, horizontal_overlap)
            other_connections["NORTH"] = 0
        else:
            if other_room.pos_y < connector[0][0].pos_y:
                connector[0][1]["NORTH"] = None
                candidates["SOUTH"] = (other, horizontal_overlap)
                other_connections["NORTH"] = 0

def horizontal_corridors(candidates, other, rm, vertical_overlap):
    current_room = rm[0]
    current_connections = rm[1]
    other_room = other[0]
    other_connections = other[1]
    if current_room.pos_x > other_room.pos_x and other_connections["EAST"] == None and current_connections["WEST"] != 0:
        connector = candidates["WEST"]
        if connector == None:
            candidates["WEST"] = (other, vertical_overlap)
            other_connections["EAST"] = 0
        else:
            if other_room.pos_x < connector[0][0].pos_x:
                connector[0][1]["EAST"] = None
                candidates["WEST"] = (other, vertical_overlap)
                other_connections["EAST"] = 0
    if current_room.pos_x < other_room.pos_x and other_connections["WEST"] == None and current_connections["EAST"] != 0:
        connector = candidates["EAST"]
        if connector == None:
            candidates["EAST"] = (other, vertical_overlap)
            other_connections["WEST"] = 0
        else:
            if other_room.pos_x + other_room.width < connector[0][0].pos_x + connector[0][0].width:
                connector[0][1]["WEST"] = None
                candidates["EAST"] = (other, vertical_overlap)
                other_connections["WEST"] = 0

def create_map():
    Map = []
    for x in range(TILE_ACROSS):
        row = []
        for i in range(TILE_DOWN):
            row.append(0)
        Map.append(row)
    Rooms = create_rooms()
    for rm in Rooms:
        for i in range(rm[0].width):
            for j in range(rm[0].height):
                Map[rm[0].pos_x+i][rm[0].pos_y+j] = 1
        corridors = create_corridors(rm, Rooms)
        #Create the corridors on the map array
        for key, value in corridors.items():
            if value is not None and value is not 0:
                dir = [0, 0]
                start_pos = [rm[0].pos_x, rm[0].pos_y]
                end_pos = [value[0][0].pos_x, value[0][0].pos_y]
                mid_overlap = value[1][len(value[1])//2]
                if key == "NORTH":
                    dir[1] = -1
                    start_pos[0] = mid_overlap
                    start_pos[1] -= 1
                    end_pos[0] = mid_overlap
                    end_pos[1] += value[0][0].height
                elif key == "SOUTH":
                    dir[1] = 1
                    start_pos[0] = mid_overlap
                    start_pos[1] += rm[0].height
                    end_pos[0] = mid_overlap
                    end_pos[1] -= 1
                elif key == "EAST":
                    dir[0] = 1
                    start_pos[0] += rm[0].width
                    start_pos[1] = mid_overlap
                    end_pos[0] -= 1
                    end_pos[1] = mid_overlap
                elif key == "WEST":
                    dir[0] = -1
                    start_pos[0] -= 1
                    start_pos[1] = mid_overlap
                    end_pos[0] += value[0][0].width
                    end_pos[1] = mid_overlap
                Map[start_pos[0]][start_pos[1]] = 2
                Map[end_pos[0]][end_pos[1]] = 2 
                distance = (start_pos[0] - end_pos[0]) + (start_pos[1] - end_pos[1])
                print(distance)
                next_pos = start_pos
                for i in range(abs(distance)):
                    next_pos = [next_pos[0] + dir[0], next_pos[1] + dir[1]]
                    print(next_pos)
                    Map[next_pos[0]][next_pos[1]] = 2 

    return Map
    