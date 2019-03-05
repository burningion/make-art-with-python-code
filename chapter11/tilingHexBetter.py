import pygame
import pygame.gfxdraw

from math import cos, sin, radians

pygame.init()

screenWidth, screenHeight = 800, 800
T_SIZE = 50

screen = pygame.display.set_mode((screenWidth, screenHeight))

clock = pygame.time.Clock()

white = (255, 255, 255)
yellow = (0, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)


def rotate_points(toTurn, pivot, degrees):
    translate = [toTurn[0] - pivot[0], toTurn[1] - pivot[1]]
    degrees = radians(degrees)
    ourCos = cos(degrees)
    ourSin = sin(degrees)

    x = translate[0] * ourCos - translate[1] * ourSin
    y = translate[0] * ourSin + translate[1] * ourCos

    return [x + pivot[0], y + pivot[1]]


def translate_points(points, x, y):
    newArray = []
    for point in points:
        newArray.append([point[0] + x, point[1] + y])
    return newArray


def create_centered_triangle(center, radius):
    C1 = [center[0], center[1] - radius]
    r120 = {'cos': cos(radians(120)), 'sin': sin(radians(120))}
    r240 = {'cos': cos(radians(240)), 'sin': sin(radians(240))}

    rX = [C1[0] - center[0], C1[1] - center[1]]
    rL, rR = [0, 0], [0, 0]

    '''
    b.x = c.x * cos( 120 degrees ) - ( c.y * sin( 120 degrees ) )
    b.y = c.x * sin( 120 degrees ) + ( c.y * cos( 120 degrees ) )
    a.x = c.x * cos( 240 degrees ) - ( c.y * sin( 240 degrees ) )
    a.y = c.x * sin( 240 degrees ) + ( c.y * cos( 240 degrees ) )
    '''
    rL[0] = rX[0] * r120['cos'] - rX[1] * r120['sin']
    rL[1] = rX[0] * r120['sin'] + rX[1] * r120['cos']
    rR[0] = rX[0] * r240['cos'] - rX[1] * r240['sin']
    rR[1] = rX[0] * r240['sin'] + rX[1] * r240['cos']

    left = [rL[0] + center[0], rL[1] + center[1]]
    right = [rR[0] + center[0], rR[1] + center[1]]
    return [left, right, C1]


running = True

triangy = create_centered_triangle((screenWidth // 2, screenHeight // 2),
                                   T_SIZE)

# colors for the rotation, this is the patter we want. there are others
colors = [red, red, blue, blue, yellow, yellow]

other = []
for i in range(30, 360, 60):
    new = []
    for point in triangy:
        new.append(rotate_points(point,
                                 (screenWidth // 2, screenHeight // 2 - T_SIZE),
                                 i))
    other.append(new)

while running:
    screen.fill(black)

    for i in range(10):
        for num, tri in enumerate(other):
            for a in range(10):
                moved = translate_points(tri, i * 150 - 650, a * 260 - 650)
                pygame.draw.polygon(screen, colors[num], moved)
                moved = translate_points(moved, 75, 130)
                pygame.draw.polygon(screen, colors[num], moved)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick()
