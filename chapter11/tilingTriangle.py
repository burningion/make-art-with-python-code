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
    rads = radians(degrees)
    ourCos = cos(rads)
    ourSin = sin(rads)

    x = translate[0] * ourCos - translate[1] * ourSin
    y = translate[0] * ourSin + translate[1] * ourCos

    return [x + pivot[0], y + pivot[1]]


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


def create_rotated_triangle(center, radius, rotation):
    ogTri = create_centered_triangle(center, radius)
    newTri = []

    for point in ogTri:
        newTri.append(rotate_points(point, center, rotation))
    return newTri


def translate_points(points, x, y):
    newArray = []
    for point in points:
        newArray.append([point[0] + x, point[1] + y])
    return newArray


running = True

triangy = create_rotated_triangle((screenWidth // 2, screenHeight // 2),
                                  T_SIZE, 0)
initialShift = (screenWidth // 2 + abs(triangy[0][0] - triangy[1][0])  // 2,
                screenHeight // 2 - T_SIZE // 2)

theDistance = abs(triangy[0][0] - triangy[1][0])
triangyUpsidey = create_rotated_triangle(initialShift, T_SIZE, 180)

# Now they're both on the same plane, only a matter of shifting each over

while running:
    screen.fill(black)

    for i in range(35):
        for j in range(35):
            pygame.draw.polygon(screen, red,
                                translate_points(triangy, theDistance * i - 500, j * 100 - i - 500))
            pygame.draw.polygon(screen, yellow,
                                translate_points(triangyUpsidey, theDistance * i - 500, j * 33 - 500))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick()
