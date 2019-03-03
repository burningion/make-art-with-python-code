import pygame
import pygame.gfxdraw

import math
pygame.init()

screenWidth = 400
screenHeight = 400

screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)

running = True

plusX = screenWidth // 2 - screenWidth // 4
plusY = screenHeight // 2 - screenHeight // 4


def draw_flat_line(screen, x1, y1, length, color):
    for x in range(x1, x1 + length):
        pygame.gfxdraw.pixel(screen, x, y1, color)


def draw_vertical_line(screen, x1, y1, length, color):
    for y in range(y1, y1 + length):
        pygame.gfxdraw.pixel(screen, x1, y, color)


def draw_plus_sign(screen, x, y, size, color):
    draw_flat_line(screen, x - (size // 2), y, size, color)
    draw_vertical_line(screen, x, y - (size // 2), size, color)


# Add a new list before our loop starts
cursorList = []

while running:
    screen.fill(black)

    # draw cursorList
    for i, plusSign in enumerate(cursorList):
        rR = math.sin(i * .01) * 127 + 128
        rG = math.sin(i * .01 + 5) * 127 + 128
        rB = math.sin(i * .01 + 10) * 127 + 128

        # Generate a separate fader for all of them to be scaled by
        # Remember, we need from 0 - 1, not -1 to 1, hence the add
        # and divide.
        fader = (math.sin(i * .02) + 1) / 2
        rR = rR * fader
        rG = rG * fader
        rB = rB * fader

        # try changing the value below from .005 - 5.2
        # you'll get some interesting results in between
        sizer = int(math.sin(i * .043) * 35 + 35)
        draw_plus_sign(screen, plusSign[0], plusSign[1], sizer, (rR, rG, rB))

    draw_plus_sign(screen, plusX, plusY, 15, white)

    # loop over each of our cursor positions. if empty, skips
    # First we take top left quarter of screen, make a copy
    cropped = pygame.Surface((screenWidth // 2, screenHeight // 2))
    cropped.blit(screen, (0, 0), pygame.Rect(0, 0,
                                             screenWidth // 2,
                                             screenHeight // 2))

    # flip that copy on just the y axis, paste below
    belowFlipped = pygame.transform.flip(cropped, False, True)
    screen.blit(belowFlipped, pygame.Rect(0, screenHeight // 2,
                                          screenWidth // 2, screenHeight))

    # flip original copy on just x axis, paste to the right
    topRight = pygame.transform.flip(cropped, True, False)
    screen.blit(topRight, pygame.Rect(screenWidth // 2, 0,
                                      screenWidth, screenHeight // 2))

    # finally flip both axis, paste bottom right
    bottomRight = pygame.transform.flip(cropped, True, True)
    screen.blit(bottomRight, pygame.Rect(screenWidth // 2,
                                         screenHeight // 2, screenWidth,
                                         screenHeight))

    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        newPlace = [plusX, plusY]
        cursorList.append(newPlace)

    if key[pygame.K_UP]:
        plusY = plusY - 1
    elif key[pygame.K_DOWN]:
        plusY = plusY + 1
    if key[pygame.K_LEFT]:
        plusX = plusX - 1
    elif key[pygame.K_RIGHT]:
        plusX = plusX + 1
    for event in pygame.event.get():
        # if you try to quit, let's leave this loop
        if event.type == pygame.QUIT:
            running = False
    # this is how we update the screen we've been drawing on.
    pygame.display.flip()
