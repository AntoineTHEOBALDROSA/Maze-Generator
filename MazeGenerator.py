from dis import dis
import time
import pygame
import random


pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PASTEL_PURPLE = (195, 155, 211)

# set visual parameters
SIZE = 14  # perfect size : SIZE = (WIDTH-2*PADDING)/maze_width
PADDING = 50  # padding from top left

# allow the program to draw the maze faster
# greater this number is, faster the maze will be built
# set None if you don't wanna see the built of the maze
# DO NOT SET IT TO 0
DRAW_ONLY_ONE_ON = 10000
assert DRAW_ONLY_ONE_ON != 0, "Please set DRAW_ONLY_ONE_ON to a value other than 0"

# Break random walls in the maze
RANDOM_GAPS = 75

#############
# MAZE ALGO #
#############


def generate_wall_maze(height, width):
    '''
    entry : width (int), height (int)
    return : maze_map (dict)
    generate a maze (of size width x height) full of wall 
    '''
    maze_map = dict()
    for row in range(height):
        for column in range(width):
            maze_map[(row+1, column+1)] = {'E': 1, 'W': 1, 'N': 1, 'S': 1}

    return maze_map


def algorithm(maze_map, type):
    '''
    entry : maze_map (dict), type (str or int)
    return : maze_map (dict)
    create the maze (Depth-First Search algorithm)
    '''
    visited = dict()
    pile = []
    maze_map_distance = dict()
    distance = 0

    # mark all cells as non-visited (False) and set their distance to 0
    for cell in maze_map.keys():
        visited[cell] = False
        maze_map_distance[cell] = None

    # set entry and exit
    maze_map[max(maze_map)]["E"] = 0
    maze_map[(min(maze_map))]["W"] = 0

    # select a radom start (the color doesn't make any sens if you select it)
    #start = (random.randint(1, max(maze_map)[0]), random.randint(1, max(maze_map)[1]))

    # set the start as the top left
    start = min(maze_map)

    # mark this start as visited
    pile.append(start)
    visited[start] = True

    draw_counter = 0

    while pile:
        if DRAW_ONLY_ONE_ON != None:  # None : no construction
            if draw_counter % DRAW_ONLY_ONE_ON == 0:
                draw_maze(WIN, maze_map, maze_map_distance, type)
        draw_counter += 1

        current_cell = pile[-1]

        #print(distance, current_cell)
        visited[current_cell] = True

        # get distance from start of the current_cell
        if type == "color":
            if maze_map_distance[current_cell] == None:
                maze_map_distance[current_cell] = distance

        current_cell_neighboor_list = possible_neighboor(
            pile[-1], visited, maze_map)

        # verify there is at least 1 valid neighboor (non-visited one)
        ct = 0
        for elt in current_cell_neighboor_list:
            if elt != None:
                ct += 1

        if ct == 0:  # there is only "None" element in current_cell_neighboor_list
            pile.pop()
            distance -= 1

        else:  # there is at least a non-visited neighboor in current_cell_neighboor_list
            random_neighboor = random.randint(0, 3)
            # trying to get the valid neighboor (and not the "None" elt)
            while current_cell_neighboor_list[random_neighboor] == None:
                random_neighboor = random.randint(0, 3)

            #maze_map_distance[current_cell] = distance

            # we open the wall
            if random_neighboor == 0:  # we chose the top neighboor
                maze_map[current_cell]['N'] = 0
                maze_map[current_cell_neighboor_list[random_neighboor]]['S'] = 0

            elif random_neighboor == 1:  # we chose the left neighboor
                maze_map[current_cell]['W'] = 0
                maze_map[current_cell_neighboor_list[random_neighboor]]['E'] = 0

            elif random_neighboor == 2:  # we chose the bottom neighboor
                maze_map[current_cell]['S'] = 0
                maze_map[current_cell_neighboor_list[random_neighboor]]['N'] = 0

            elif random_neighboor == 3:  # we chose the right neighboor
                maze_map[current_cell]['E'] = 0
                maze_map[current_cell_neighboor_list[random_neighboor]]['W'] = 0

            # we make the same thing with the new neighboor
            pile.append(current_cell_neighboor_list[random_neighboor])
            distance += 1

    # this is a personnal adition to make the maze a little bit more complex, as right now there is only 1 path
    # that can lead to the end, this will make the maze a little funnier.

    # creating random gaps
    # max_maze_map = max(maze_map)
    # removed = 0

    # while removed < RANDOM_GAPS:
    #     draw_counter += 1
    #     rand_x = random.randint(2, max_maze_map[1]-1)
    #     rand_y = random.randint(2, max_maze_map[0]-1)
    #     rand_direction = random.choice(["E", "W", "N", "S"])
    #     if maze_map[(rand_x, rand_y)][rand_direction] == 1:
    #         maze_map[(rand_x, rand_y)][rand_direction] = 0
    #         if rand_direction == "E":
    #             maze_map[(rand_x, rand_y+1)]["W"] = 0
    #         elif rand_direction == "W":
    #             maze_map[(rand_x, rand_y-1)]["E"] = 0
    #         elif rand_direction == "N":
    #             maze_map[(rand_x-1, rand_y)]["S"] = 0
    #         elif rand_direction == "S":
    #             maze_map[(rand_x+1, rand_y)]["N"] = 0
    #         removed += 1

    draw_maze(WIN, maze_map, maze_map_distance, type)

    return maze_map


def possible_neighboor(cell, visited, maze_map):
    '''
    entry : cell (tuple)
    return : list_neighboor (list)
    return a list of all neighboor of a cell
    this list contains all neighboor in order : top, left, bottom, right
        None = the neighboor is out of the maze / already vistied
        tuple = the coordinates of the neighboor
    '''
    list_neighboor = []
    # example of cell : cell = (2,3)

    if cell[0] != 1 and visited[(cell[0]-1, cell[1])] == False:
        list_neighboor.append((cell[0]-1, cell[1]))  # top
    else:
        list_neighboor.append(None)

    if cell[1] != 1 and visited[(cell[0], cell[1]-1)] == False:
        list_neighboor.append((cell[0], cell[1]-1))  # left
    else:
        list_neighboor.append(None)

    if cell[0] != max(maze_map)[0] and visited[(cell[0]+1, cell[1])] == False:
        list_neighboor.append((cell[0]+1, cell[1]))  # bottom
    else:
        list_neighboor.append(None)

    if cell[1] != max(maze_map)[1] and visited[(cell[0], cell[1]+1)] == False:
        list_neighboor.append((cell[0], cell[1]+1))  # right
    else:
        list_neighboor.append(None)

    return list_neighboor

#############
# INTERFACE #
#############


def color_dist(distance, maze_size):
    '''
    entry : distance (int), maze_size (int)
    return a color determine by the distance
    formula : value = 3*255*distance/maze_size
    '''
    value = int(3.7*255*distance/maze_size)
    if value <= 255:
        value = (255, 255 - value, 0)

    elif value > 255 and value <= 255 * 2:
        value = (2 * 255 - value, 0, value - 255)

    elif value > 255 * 2:
        value = (0, 0, 255 * 3 - value)

    return value


def draw_background(win, maze, maze_map_distance, type):
    '''
    draw the background of the maze
    type=0 --> blank ; type=1 --> color
    '''

    if type == 0 or type == "blank":
        max_maze_map = max(maze)
        pygame.draw.rect(win, WHITE, (PADDING, PADDING,
                         max_maze_map[1]*SIZE, max_maze_map[0]*SIZE))

    elif type == 1 or type == "color":
        for cell, distance in maze_map_distance.items():
            # ex:  (1, 1): 1
            if distance == None:
                # if the cell is not visited yet, we let it white (we have to overdraw)
                pygame.draw.rect(win, WHITE,
                                 (PADDING+(cell[1]-1)*SIZE, PADDING+(cell[0]-1)*SIZE, PADDING+cell[1]*SIZE, PADDING+cell[0]*SIZE))
            else:
                #print((PADDING+(cell[1]-1)*SIZE, PADDING+(cell[0]-1)*SIZE, PADDING+cell[1]*SIZE, PADDING+cell[0]*SIZE))
                pygame.draw.rect(win, color_dist(distance, len(maze_map_distance)),
                                 (PADDING+(cell[1]-1)*SIZE, PADDING+(cell[0]-1)*SIZE, PADDING+cell[1]*SIZE, PADDING+cell[0]*SIZE))

            # overwrite bc idk why pygame does is drawing rectangle wrong :(
            pygame.draw.rect(win, PASTEL_PURPLE,
                             (WIDTH-PADDING, 0, WIDTH, HEIGHT))
            pygame.draw.rect(win, PASTEL_PURPLE,
                             (0, HEIGHT-PADDING, WIDTH, HEIGHT))


def draw_walls(win, maze):
    '''
    draw walls of the maze
    '''
    for pixel, orientation in maze.items():
        # example :  (1, 1): {'E': 1, 'W': 0, 'N': 0, "S": 0}
        if orientation["E"] == 1:
            pygame.draw.line(win, BLACK, (pixel[1]*SIZE+PADDING, (pixel[0]-1)
                             * SIZE+PADDING), (pixel[1]*SIZE+PADDING, pixel[0]*SIZE+PADDING), 2)
        if orientation["W"] == 1:
            pygame.draw.line(win, BLACK, ((pixel[1]-1)*SIZE+PADDING, (pixel[0]-1)*SIZE+PADDING), ((
                pixel[1]-1)*SIZE+PADDING, pixel[0]*SIZE+PADDING), 2)
        if orientation["N"] == 1:
            pygame.draw.line(win, BLACK, ((pixel[1]-1)*SIZE+PADDING, (pixel[0]-1)
                             * SIZE+PADDING), (pixel[1]*SIZE+PADDING, (pixel[0]-1)*SIZE+PADDING), 2)
        if orientation["S"] == 1:
            pygame.draw.line(win, BLACK, ((
                pixel[1]-1)*SIZE+PADDING, pixel[0]*SIZE+PADDING), (pixel[1]*SIZE+PADDING, pixel[0]*SIZE+PADDING), 2)


def draw_maze(win, maze, maze_map_distance, type):
    '''
    entry : win (window), maze (maze map)
    return : nothing
    draw the maze onto pygame window
    '''

    # draw the background of the maze
    # type=0 --> blank ; type=1 --> color
    draw_background(win, maze, maze_map_distance, type)

    # draw the walls of the maze
    draw_walls(win, maze)

    pygame.display.update()


def main():
    run = True

    WIN.fill(PASTEL_PURPLE)
    maze_height, maze_width = 50, 50

    type = "color"  # "blank" -> no color ; "color" -> color

    maze = algorithm(generate_wall_maze(maze_height, maze_width), type)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    maze = algorithm(generate_wall_maze(
                        maze_height, maze_width), type)
                    #draw_maze(WIN, maze)

    pygame.quit()


main()
