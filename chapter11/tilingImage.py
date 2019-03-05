import pygame
import pygame.gfxdraw

from math import cos, sin, radians

import copy

pygame.init()

screenWidth, screenHeight = 1024, 1024
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

triangy = create_centered_triangle((0, 0), T_SIZE)
triangy1 = copy.deepcopy(triangy)

triangy1[0][1] = triangy[0][1] - T_SIZE - (T_SIZE // 2)
triangy1[1][1] = triangy[1][1] - T_SIZE - (T_SIZE // 2)
triangy1[2][1] = triangy[2][1] + T_SIZE * 2 - (T_SIZE // 2)

# Now they're both on the same plane, only a matter of shifting each over
triangy1[0][0] = triangy1[0][0] + (T_SIZE // 1.1)
triangy1[1][0] = triangy1[1][0] + (T_SIZE // 1.1)
triangy1[2][0] = triangy1[2][0] + (T_SIZE // 1.1)

other = []
for point in triangy:
    other.append(rotate_points(point,
                               (screenWidth // 2, screenHeight // 2),
                               180))

for place, point in enumerate(other):
    other[place] = [point[0] + T_SIZE - 6, point[1] - T_SIZE // 2]

red1 = pygame.image.load('1.jpg').convert()
blue = pygame.transform.scale(pygame.image.load('2.jpg').convert(),
                              (800, 800))

offx1 = [0, 0]
offx2 = [0, 0]
while running:
    screen.fill(black)

    pygame.gfxdraw.textured_polygon(screen, triangy, red1, offx1[0], offx1[1])
    pygame.gfxdraw.textured_polygon(screen, triangy1, blue, offx2[0], offx2[1])

    key = pygame.key.get_pressed()

    if key[pygame.K_UP]:
        if offx1[1] > 0:
            offx1[1] -= 1
    elif key[pygame.K_DOWN]:
        offx1[1] += 1
    if key[pygame.K_LEFT]:
        if offx1[0] > 0:
            offx1[0] -= 1
    elif key[pygame.K_RIGHT]:
        offx1[0] += 1

    if key[pygame.K_w]:
        if offx2[1] > 0:
            offx2[1] -= 1
    elif key[pygame.K_s]:
        offx2[1] += 1
    if key[pygame.K_a]:
        if offx2[0] > 0:
            offx2[0] -= 1
    elif key[pygame.K_d]:
        offx2[0] += 1

    for i in range(12):
        ttriangy = copy.deepcopy(triangy)
        ttriangy1 = copy.deepcopy(triangy1)
        ttriangy1[0][0] = ttriangy1[0][0] + (T_SIZE // 1.1 * 2 * i)
        ttriangy1[1][0] = ttriangy1[1][0] + (T_SIZE // 1.1 * 2 * i)
        ttriangy1[2][0] = ttriangy1[2][0] + (T_SIZE // 1.1 * 2 * i)
        ttriangy[0][0] = ttriangy[0][0] + (T_SIZE // 1.1 * 2 * i)
        ttriangy[1][0] = ttriangy[1][0] + (T_SIZE // 1.1 * 2 * i)
        ttriangy[2][0] = ttriangy[2][0] + (T_SIZE // 1.1 * 2 * i)
        for i in range(12):
            tttriangy = copy.deepcopy(ttriangy)
            tttriangy1 = copy.deepcopy(ttriangy1)
            tttriangy1[0][1] = tttriangy1[0][1] + T_SIZE * i * 1.5
            tttriangy1[1][1] = tttriangy1[1][1] + T_SIZE * i * 1.5
            tttriangy1[2][1] = tttriangy1[2][1] + T_SIZE * i * 1.5
            tttriangy[0][1] = tttriangy[0][1] + T_SIZE * i * 1.5
            tttriangy[1][1] = tttriangy[1][1] + T_SIZE * i * 1.5
            tttriangy[2][1] = tttriangy[2][1] + T_SIZE * i * 1.5
            pygame.gfxdraw.textured_polygon(screen, tttriangy,
                                            red1, offx1[0], offx1[1])
            pygame.gfxdraw.textured_polygon(screen, tttriangy1,
                                            blue, offx2[0], offx2[1])

        pygame.gfxdraw.textured_polygon(screen, ttriangy,
                                        red1, offx1[0], offx1[1])
        pygame.gfxdraw.textured_polygon(screen, ttriangy1,
                                        blue, offx2[0], offx2[1])

    # Circle below for checking that triangle is right
    # pygame.draw.circle(screen, red, (screenWidth // 2, screenHeight // 2), 50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick()
