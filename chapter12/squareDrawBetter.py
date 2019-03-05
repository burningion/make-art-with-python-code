import pygame
import pygame.gfxdraw

from math import cos, sin, radians, sqrt

pygame.init()

screenWidth, screenHeight = 800, 800
screenCenter = [screenWidth // 2, screenHeight // 2]

SQUARE_SIZE = 100
LINE_POINTS = 6
OFFSCREEN = 300


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


def find_index_of_opposite(theList, thePlace):
    # add the duplicate corners, divide by four sides
    segmentLength = (len(theList) + 4) // 4

    if thePlace < segmentLength:
        return (segmentLength - 1) * 3 - thePlace
    elif thePlace < (segmentLength * 2):
        return (segmentLength - 1) * 4 - (thePlace - (segmentLength - 1))


def draw_flat_line(screen, x1, y1, length, color):
    for x in range(x1, x1 + length):
        pygame.gfxdraw.pixel(screen, x, y1, color)


def draw_vertical_line(screen, x1, y1, length, color):
    for y in range(y1, y1 + length):
        pygame.gfxdraw.pixel(screen, x1, y, color)


def draw_plus_sign(screen, x, y, size, color):
    draw_flat_line(screen, x - (size // 2), y, size, color)
    draw_vertical_line(screen, x, y - (size // 2), size, color)


def get_longest(linePoints):
    longest = [0, 0]
    for i in linePoints:
        if abs(i[0]) > longest[0]:
            longest[0] = i[0]
        elif abs(i[1]) > longest[1]:
            longest[1] = i[1]
    return longest


theSquare = create_midpoints_square(SQUARE_SIZE,
                                    (SQUARE_SIZE // 2, SQUARE_SIZE // 2),
                                    LINE_POINTS)

theSquare = rotate_points(theSquare, (SQUARE_SIZE // 2, SQUARE_SIZE // 2), 45)
plusX, plusY = screenCenter

SQUARE_SIZE = 145
drawMain = True
running = True

while running:
    screen.fill(black)
    surface1 = pygame.Surface((SQUARE_SIZE + get_longest(theSquare)[0] * 2,
                               SQUARE_SIZE + get_longest(theSquare)[1] * 2),
                              flags=pygame.SRCALPHA)
    surface2 = pygame.Surface((SQUARE_SIZE + get_longest(theSquare)[0] * 2,
                               SQUARE_SIZE + get_longest(theSquare)[1] * 2),
                              flags=pygame.SRCALPHA)

    pygame.draw.polygon(surface1, yellow,
                        translate_points(theSquare,
                                         get_longest(theSquare)[0],
                                         get_longest(theSquare)[1]))
    pygame.draw.polygon(surface2, blue,
                        translate_points(theSquare,
                                         get_longest(theSquare)[0],
                                         get_longest(theSquare)[1]))

    for i in range(15):
        for j in range(15):
            if i % 2 == 0:
                if j % 2 == 0:
                    screen.blit(surface1, (SQUARE_SIZE * i - OFFSCREEN,
                                           j * SQUARE_SIZE - OFFSCREEN))
                else:
                    screen.blit(surface2, (SQUARE_SIZE * i - OFFSCREEN,
                                           j * SQUARE_SIZE - OFFSCREEN))
            else:
                if j % 2 == 0:
                    screen.blit(surface2, (SQUARE_SIZE * i - OFFSCREEN,
                                           j * SQUARE_SIZE - OFFSCREEN))
                else:
                    screen.blit(surface1, (SQUARE_SIZE * i - OFFSCREEN,
                                           j * SQUARE_SIZE - OFFSCREEN))

    if pygame.mouse.get_focused():
        plusX, plusY = pygame.mouse.get_pos()

    draw_plus_sign(screen, plusX, plusY, 5, white)
    if drawMain:
        pygame.draw.polygon(screen, red,
                            translate_points(theSquare, SQUARE_SIZE * 5 - 200,
                                             5 * SQUARE_SIZE - 200))

    key = pygame.key.get_pressed()

    if key[pygame.K_d]:
        drawMain = False

    if key[pygame.K_f]:
        drawMain = True

    if key[pygame.K_s]:
        import pickle
        print("Saving Drawing...")
        pickle.dump(theSquare, open('out.pkl', 'wb'))

    for event in pygame.event.get():
        # our mouse click gets checked here
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                place, xoffs, yoffs = find_index_of_closest(translate_points(theSquare,
                                                                             SQUARE_SIZE * 5 - 200,
                                                                             5 * SQUARE_SIZE - 200),
                                                            [plusX, plusY])
                print("Index touched: %i" % place)
                print("xoffs: %i, yoffs: %i" % (xoffs, yoffs))

                if place in range(1, LINE_POINTS):
                    opposite = find_index_of_opposite(theSquare, place)
                    theSquare[place] = [theSquare[place][0] + xoffs,
                                        theSquare[place][1] + yoffs]
                    theSquare[opposite] = [theSquare[opposite][0] + xoffs,
                                           theSquare[opposite][1] + yoffs]

                if place in range(LINE_POINTS + 1, LINE_POINTS * 2):
                    opposite = find_index_of_opposite(theSquare, place)
                    theSquare[place] = [theSquare[place][0] + xoffs,
                                        theSquare[place][1] + yoffs]
                    theSquare[opposite] = [theSquare[opposite][0] + xoffs,
                                           theSquare[opposite][1] + yoffs]

        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick()
