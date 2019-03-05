import pygame
import pygame.gfxdraw

from math import cos, sin, sqrt, radians

pygame.init()

screenWidth, screenHeight = 800, 800
screenCenter = [screenWidth // 2, screenHeight // 2]

SQUARE_SIZE = 100

screen = pygame.display.set_mode((screenWidth, screenHeight))

clock = pygame.time.Clock()

white = (255, 255, 255)
yellow = (0, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)


def rotate_point(toTurn, pivot, degrees):
    translate = [toTurn[0] - pivot[0], toTurn[1] - pivot[1]]
    rads = radians(degrees)
    ourCos = cos(rads)
    ourSin = sin(rads)

    x = translate[0] * ourCos - translate[1] * ourSin
    y = translate[0] * ourSin + translate[1] * ourCos

    return [x + pivot[0], y + pivot[1]]


def rotate_points(points, pivot, degrees):
    rotatedPoints = []
    for point in points:
        rotatedPoints.append(rotate_point(point, pivot, degrees))
    return rotatedPoints


def translate_points(points, dx, dy):
    newArray = []
    for point in points:
        newArray.append([point[0] + dx, point[1] + dy])
    return newArray


def create_centered_square(length, centerPoint):
    hlength = length // 2
    topLeft = [centerPoint[0] - hlength, centerPoint[1] - hlength]
    topRight = [centerPoint[0] + hlength, centerPoint[1] - hlength]
    bottomLeft = [centerPoint[0] - hlength, centerPoint[1] + hlength]
    bottomRight = [centerPoint[0] + hlength, centerPoint[1] + hlength]

    # needs to be in proper drawing order for polygon to draw right
    return [topLeft, bottomLeft, bottomRight, topRight]


def create_midpoints_square(length, centerPoint, pointsPerLine):
    distance = length / pointsPerLine
    #print("distance: %i" % distance)
    left, right, bottom, top = [], [], [], []
    for i in range(pointsPerLine):
        left.append([centerPoint[0] - length / 2,
                     centerPoint[1] - length / 2 + (i * distance)])
        right.append([centerPoint[0] + length / 2,
                      centerPoint[1] + length / 2 - (i * distance)])
        bottom.append([centerPoint[0] - length / 2 + (i * distance),
                       centerPoint[1] + length / 2])
        top.append([centerPoint[0] + length / 2 - (i * distance),
                    centerPoint[1] - length / 2])

    return left + bottom + right + top


def find_index_of_closest(theList, thePoint):
    lowest = 800
    place = 0
    xoffs, yoffs = 0, 0
    for m, point in enumerate(theList):
        distance = sqrt(pow(point[0] - thePoint[0], 2) + pow(point[1] - thePoint[1], 2))
        if distance < lowest:
            place = m
            lowest = distance
            xoffs = thePoint[0] - point[0]
            yoffs = thePoint[1] - point[1]
    return place, xoffs, yoffs


def draw_flat_line(screen, x1, y1, length, color):
    for x in range(x1, x1 + length):
        pygame.gfxdraw.pixel(screen, x, y1, color)


def draw_vertical_line(screen, x1, y1, length, color):
    for y in range(y1, y1 + length):
        pygame.gfxdraw.pixel(screen, x1, y, color)


def draw_plus_sign(screen, x, y, size, color):
    draw_flat_line(screen, x - (size // 2), y, size, color)
    draw_vertical_line(screen, x, y - (size // 2), size, color)


theSquare = create_midpoints_square(SQUARE_SIZE, screenCenter, 5)

plusX, plusY = screenCenter

one = translate_points(theSquare, -100, 100)
two = translate_points(theSquare, 100, 100)
three = translate_points(theSquare, -150, 150)
four = translate_points(theSquare, 150, 150)
five = translate_points(theSquare, -200, 200)
six = translate_points(theSquare, 200, 200)

odd = 0
half = 400

drawMain = True
running = True

while running:
    screen.fill(black)

    pygame.draw.polygon(screen, red, theSquare)

    for i in range(15):
        for j in range(15):
            if i % 2 == 0:
                if j % 2 == 0:
                    pygame.draw.polygon(screen, blue,
                                        translate_points(theSquare,
                                                         100 * i - half - 100,
                                                         j * 100 - half - 100))
                else:
                    pygame.draw.polygon(screen, yellow,
                                        translate_points(theSquare,
                                                         100 * i - half - 100,
                                                         j * 100 - half - 100))
            else:
                if j % 2 == 0:
                    pygame.draw.polygon(screen, yellow,
                                        translate_points(theSquare,
                                                         100 * i - half - 100,
                                                         j * 100 - half - 100))
                else:
                    pygame.draw.polygon(screen, blue,
                                        translate_points(theSquare,
                                                         100 * i - half - 100,
                                                         j * 100 - half - 100))

    if pygame.mouse.get_focused():
        plusX, plusY = pygame.mouse.get_pos()

    draw_plus_sign(screen, plusX, plusY, 5, white)
    if drawMain:
        pygame.draw.polygon(screen, red, theSquare)

    key = pygame.key.get_pressed()

    if key[pygame.K_d]:
        drawMain = False

    if key[pygame.K_f]:
        drawMain = True

    if key[pygame.K_s]:
        import pickle
        pickle.dump(theSquare, open('out.pkl', 'wb'))

    for event in pygame.event.get():
        # our mouse click gets checked here
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                place, xoffs, yoffs = find_index_of_closest(theSquare, [plusX, plusY])

                if place in range(1, 6):
                    opposite = 15 - place
                    theSquare[place] = [plusX, plusY]
                    theSquare[opposite] = [theSquare[opposite][0] + xoffs, theSquare[opposite][1] + yoffs]

                if place in range(6, 10):
                    opposite = 19 - (place - 6)
                    theSquare[place] = [plusX, plusY]
                    theSquare[opposite] = [theSquare[opposite][0] + xoffs, theSquare[opposite][1] + yoffs]

        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick()
