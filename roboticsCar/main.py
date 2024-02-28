import pygame
import math
import time

import numpy as np
from tensorflow import keras


def moveCar(speed, direction, car_position):

    print(direction)
    angle_radians = math.radians(direction)
    sin_value = math.sin(angle_radians) * speed
    cos_value = math.cos(angle_radians) * speed


    car_y = car_position[1]
    car_x = car_position[0]
    car_y += sin_value
    car_x += cos_value


    pygame.draw.rect(window, (255, 0, 0), car_rect)

    return car_x, car_y, speed, direction

scale = 0.35

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

car_direction = 0

# create a clock object to regulate the framerate
clock = pygame.time.Clock()

car_rect = pygame.Rect(car_x, car_y, car_width, car_height)

def calculateLength(car_pos, direction, offset):



    angle_radians = math.radians(direction+offset)


    # calculate the x and y endoints of each line
    length = 4000
    x1 = car_pos[0]
    y1 = car_pos[1]

    x2 = math.sin(angle_radians) * length
    y2 = math.cos(angle_radians) * length

    #find the intectepts between lines should they exist

    for i in range(0, len(map_boundaries)):
        #Check if the lines intersect
        x3 = map_boundaries[i][0][0]
        y3 = map_boundaries[i][0][1]
        x4 = map_boundaries[i][1][0]
        y4 = map_boundaries[i][1][1]

        if(x1==x2):
            m1 = (y2-y1)/(x2-x1)
            m2 = (y4-y3)/(x4-x3)

            intersection_y = y1 + m1*(x3-x1)

    


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

numfeelers = 100

feelers  = [0]*numfeelers
LIDAR = [0]*numfeelers

for i in range(numfeelers): 
        LIDAR[i] = [calculateLength(car_position, car_direction, i*(360/numfeelers)), i*(360/numfeelers)]
        feelers[i] = ((car_position, calculateFeeler(car_position, car_direction, i*(360/numfeelers))))
        

for i in range(numfeelers):   
    print(feelers) 

result, intersection = lines_touching(map_boundaries, feelers, line1, line2)



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

    accelaration = 1
    turning  = 1
    breaking = 0.8

    # move the car based on the arrow keys

    if keys[pygame.K_0]:
        car_speed = 0
    if keys[pygame.K_1]:
        car_speed = 1
    if keys[pygame.K_2]:
        car_speed = 2
    if keys[pygame.K_3]:
        car_speed = 3
    if keys[pygame.K_4]:
        car_speed = 4
    if keys[pygame.K_5]:
        car_speed = 5
    if keys[pygame.K_6]:
        car_speed = 6
    if keys[pygame.K_7]:
        car_speed = 7
    if keys[pygame.K_8]:
        car_speed = 8
    if keys[pygame.K_9]:
        car_speed = 9

    if keys[pygame.K_w]:
         car_speed+=accelaration
         print(car_speed)

       

    if keys[pygame.K_s]:
        car_speed-= accelaration
        print(car_speed)

             
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

    for i in range(numfeelers): 
        feelers[i] = (car_position, calculateFeeler(car_position, car_direction, i*(360/numfeelers)))
    
    

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
