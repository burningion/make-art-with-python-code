import pygame
import pygame.gfxdraw
import random  # add our random library

pygame.init()

screenWidth = 800
screenHeight = 800

screen = pygame.display.set_mode((screenWidth, screenHeight))

white = (255, 255, 255)
black = (0, 0, 0)

running = True


def draw_flat_line(screen, x1, y1, length, color):
    for x in range(x1, x1 + length):
        pygame.gfxdraw.pixel(screen, x, y1, color)


def draw_vertical_line(screen, x1, y1, length, color):
    for y in range(y1, y1 + length):
        pygame.gfxdraw.pixel(screen, x1, y, color)


# Changes to our while running loop begin below
while running:
    screen.fill(black)
    # let's do a hundred lines per frame
    for i in range(100):
        thisX, thisY = (random.randrange(0, screenWidth),
                        random.randrange(0, screenHeight))

        thisLength = random.randrange(0, 100)
        # we have a random x and y, and a random length
        draw_flat_line(screen, thisX, thisY, thisLength, white)

    for event in pygame.event.get():
        # if you try to quit, let's leave this loop
        if event.type == pygame.QUIT:
            running = False
    # this is how we update the screen we've been drawing on.
    pygame.display.flip()
