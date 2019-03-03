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

        draw_plus_sign(screen, plusSign[0], plusSign[1], 15, (rR, rG, rB))

    draw_plus_sign(screen, plusX, plusY, 15, white)

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
