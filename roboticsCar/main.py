import pygame
import math
import time
import tensorflow as tf
import numpy as np
from tensorflow import keras


def moveCar(speed, direction, car_position):


    angle_radians = math.radians(direction)
    sin_value = math.sin(angle_radians) * speed
    cos_value = math.cos(angle_radians) * speed


    car_y = car_position[1]
    car_x = car_position[0]
    car_y += sin_value
    car_x += cos_value


    pygame.draw.rect(window, (255, 0, 0), car_rect)

    return car_x, car_y, speed, direction
def calculateFeeler(car_pos, direction, offset):

    length = 150

    direction = direction + offset
    angle_radians = math.radians(direction)
    outy = car_pos[1]+ math.sin(angle_radians) * length
    outx = car_pos[0] + math.cos(angle_radians) * length


    return outx, outy

scale = 0.1

# initialize Pygame
pygame.init()




# set the dimensions of the window
win_width = 3200*scale
win_height = 3200*scale

# create the window
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Car Sim")

# set the background color
background_color = (255, 255, 255)

# set the initial position of the car
car_x = 300*scale
car_y = 300*scale

# set the dimensions of the car
car_width = 5
car_height = 5

# set the speed of the car
car_speed = 0

car_direction = 0;

# create a clock object to regulate the framerate
clock = pygame.time.Clock()

car_rect = pygame.Rect(car_x, car_y, car_width, car_height)

def lines_touching(Lines, feelers, index1, index2):
    """Checks if two lines from a Lines[] array are touching and returns the point of intersection if they are not parallel"""
   # print(f"LINES!!")
   # print(Lines[index1][0])
    x1, y1 = Lines[index1][0]
    x2, y2 = Lines[index1][1]
  #  print(feelers)
    x3, y3 = feelers[index2][0]
    x4, y4 = feelers[index2][1]

   # print(x1, y1, x2, y2)
  #  print(x3, y3, x4, y4)
    # Check if one or both lines are vertical
    if x2 - x1 == 0 and x4 - x3 == 0:
     #   print(f"Both lines are vertical and parallel, so they do not intersect")
        return False, None
    elif x2 - x1 == 0:
      #  print(f"First line is vertical")
        slope2 = (y4 - y3) / (x4 - x3)
        x_intersect = x1
        y_intersect = slope2 * (x_intersect - x3) + y3
    elif x4 - x3 == 0:
      #  print(f"Second line is vertical")
        slope1 = (y2 - y1) / (x2 - x1)
        x_intersect = x3
        y_intersect = slope1 * (x_intersect - x1) + y1
        print(x_intersect, y_intersect)

    else:
       # print(f" Calculate slopes")
        slope1 = (y2 - y1) / (x2 - x1)
        slope2 = (y4 - y3) / (x4 - x3)

      #  print(f" Check if slopes are equal")
        if slope1 == slope2:
       #     print(f"Check if lines are overlapping")
            if (x1 <= x3 <= x2 or x1 <= x4 <= x2 or x3 <= x1 <= x4 or x3 <= x2 <= x4) and \
               (y1 <= y3 <= y2 or y1 <= y4 <= y2 or y3 <= y1 <= y4 or y3 <= y2 <= y4):
       #         print(f"Lines do do overlap")
                return True, None
            else:
                return False, None
        else:
        ##    print(f" Calculate point of intersection")
            x_intersect = ((y3 - y1) + (slope1 * x1 - slope2 * x3)) / (slope1 - slope2)
            y_intersect = slope1 * (x_intersect - x1) + y1

        # Check if point of intersection lies on both lines
        if (x1 <= x_intersect <= x2 or x2 <= x_intersect <= x1) and \
           (x3 <= x_intersect <= x4 or x4 <= x_intersect <= x3) and \
           (y1 <= y_intersect <= y2 or y2 <= y_intersect <= y1) and \
           (y3 <= y_intersect <= y4 or y4 <= y_intersect <= y3):
            return True, (x_intersect, y_intersect)

  #  print(f"Checking Intecepts")

    if (x1 <= x_intersect <= x2 or x2 <= x_intersect <= x1) and \
           (x3 <= x_intersect <= x4 or x4 <= x_intersect <= x3) and \
           (y1 <= y_intersect <= y2 or y2 <= y_intersect <= y1) and \
           (y3 <= y_intersect <= y4 or y4 <= y_intersect <= y3):
            return True, (x_intersect, y_intersect)
    else:

        return False, None
def getColissions(feelers, walls):
    index1 = 0;

    for feeler in feelers:
        index2 = 0;
        for wall in walls:
            #print(feeler ,f"WALL  - - " , wall)
            result, intercept = lines_touching(walls, feelers, index2, index1)
            if result:
               # print (feelers[index1][1])
                #print(intercept)
                feelers_list = [[[value for value in subsubtuple] for subsubtuple in subtuple] for subtuple in feelers]

                feelers_list[index1][1] = intercept
                tuple(tuple(tuple(value for value in subsublist) for subsublist in subtuple) for subtuple in feelers_list)
                feelers = tuple(feelers_list)
            index2 += 1
        index1 += 1
    return feelers
def drawMap():


    #inside square
    pygame.draw.line(window, (0, 0, 0), (1000 * scale, 1000 * scale), (2200 * scale, 1000 * scale))
    pygame.draw.line(window, (0, 0, 0), (1000 * scale, 1000 * scale), (1000 * scale, 2200 * scale))
    pygame.draw.line(window, (0, 0, 0), (2200 * scale, 1000 * scale), (2200 * scale, 2200 * scale))
    pygame.draw.line(window, (0, 0, 0), (1000 * scale, 2200 * scale), (2200 * scale, 2200 * scale))


    #outside square
    pygame.draw.line(window, (0, 0, 0), (0 * scale, 0 * scale), (3200 * scale, 0 * scale), 3)
    pygame.draw.line(window, (0, 0, 0), (0 * scale, 0 * scale), (0 * scale, 3200 * scale), 3)
    pygame.draw.line(window, (0, 0, 0), (3200 * scale, 3200 * scale), (3200 * scale, 0 * scale), 3)
    pygame.draw.line(window, (0, 0, 0), (3200 * scale, 3200 * scale), (0 * scale, 3200 * scale), 3)

def drawFeelers(feelerData):
    for feeler in feelerData:
        pygame.draw.line(window, (0,255,0), feeler[0], feeler[1])






#internal box


map_boundaries = [
    # inside square
    ((1000 * scale, 1000 * scale), (2200 * scale, 1000 * scale)),
    ((1000 * scale, 1000 * scale), (1000 * scale, 2200 * scale)),
    ((2200 * scale, 1000 * scale), (2200 * scale, 2200 * scale)),
    ((1000 * scale, 2200 * scale), (2200 * scale, 2200 * scale)),

    # outside square
    ((0 * scale, 0 * scale), (3200 * scale, 0 * scale)),
    ((0 * scale, 0 * scale), (0 * scale, 3200 * scale)),
    ((3200 * scale, 3200 * scale), (3200 * scale, 0 * scale)),
    ((3200 * scale, 3200 * scale), (0 * scale, 3200 * scale)),
]

line1 = 0
line2 = 0
car_position = (car_x, car_y)

feelers  = [(car_position, calculateFeeler(car_position, car_direction, 0)),
            (car_position, calculateFeeler(car_position, car_direction, 90)),
            (car_position, calculateFeeler(car_position, car_direction, -90)),
            (car_position, calculateFeeler(car_position, car_direction, 45)),
            (car_position, calculateFeeler(car_position, car_direction, -45)),
            (car_position, calculateFeeler(car_position, car_direction, 22.5)),
            (car_position, calculateFeeler(car_position, car_direction, -22.5))
            ]

result, intersection = lines_touching(map_boundaries,feelers, line1, line2)



if result:
    print(f"Lines {line1} and {line2} intersect at {intersection}")
else:
    print(f"Lines {line1} and {line2} do not intersect")

# main game loop
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # if the user clicks the close button, exit the game
            pygame.quit()
            quit()

        # draw the background
    window.fill(background_color)





    # get the state of the arrow keys
    keys = pygame.key.get_pressed()

    accelaration = 0.1
    turning  = 1
    breaking = 0.8

    # move the car based on the arrow keys
    if keys[pygame.K_w]:
         car_speed+=accelaration
    if keys[pygame.K_s]:
        car_speed-= accelaration
    if keys[pygame.K_a]:
        car_direction -= turning*car_speed
    if keys[pygame.K_d]:
        car_direction += turning*car_speed
    if keys[pygame.K_b]:
        if(car_speed>breaking):
            car_speed -= breaking
        elif (car_speed<-(breaking)):
            car_speed += breaking
        else:
            car_speed = 0



    # draw the car




    car_position = (car_x, car_y)
    #print(car_direction)





    carData = moveCar(car_speed, car_direction, car_position)

    car_x = carData[0]
    car_y = carData[1]


    feelers[0] = (car_position, calculateFeeler(car_position, car_direction, 0))
    feelers[1] = (car_position, calculateFeeler(car_position, car_direction, 90))
    feelers[2] = (car_position, calculateFeeler(car_position, car_direction, -90))
    feelers[3] = (car_position, calculateFeeler(car_position, car_direction, 22.5))
    feelers[4] = (car_position, calculateFeeler(car_position, car_direction, -22.5))
    feelers[5] = (car_position, calculateFeeler(car_position, car_direction, 45))
    feelers[6] = (car_position, calculateFeeler(car_position, car_direction, -45))

    result, intersection = lines_touching(map_boundaries, feelers, line1, line2)

    feelerData = getColissions(feelers, map_boundaries)

    drawFeelers(feelerData)

    drawMap()
    car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
    pygame.draw.rect(window, (255, 0, 0), car_rect)

    # update the display
    pygame.display.update()






    # regulate the framerate
    clock.tick(60)
