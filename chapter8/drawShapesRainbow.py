import pygame
import pygame.gfxdraw

import random

pygame.init()

screenWidth = 400
screenHeight = 400

screen = pygame.display.set_mode((screenWidth, screenHeight))

clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)

running = True


class Line():
    def __init__(self):
        self.linePoints = []
        # Make sure we have a default mode to draw with
        self.draw_mode = 1
        # make sure we choose a random color
        self.color = random.choice(rainbowPalette)

    def __repr__(self):
        if not self.is_line():
            return "Not a line yet."

        return "Line from %s to %s" % (self.linePoints[0], self.linePoints[-1])

    def is_line(self):
        if len(self.linePoints) > 1:
            return True
        return False

    def is_shape(self):
        if len(self.linePoints) > 2:
            return True
        return False

    def add_linepoint(self, x, y):
        self.linePoints.append((x, y))

    # New function, to call the right mode of drawing
    def draw(self, screen):
        if self.draw_mode == 1:
            self.draw_line(screen)

        elif self.draw_mode == 2:
            self.draw_shape(screen)

        elif self.draw_mode == 3:
            self.draw_circle(screen)

    def draw_line(self, screen):
        if not self.is_line():
            return
        for place, point in enumerate(self.linePoints):
            if place == 0:
                continue
            pygame.draw.line(screen, self.color, point,
                             self.linePoints[place - 1])

    def draw_shape(self, screen):
        if not self.is_line():
            return
        if not self.is_shape():
            self.draw_line(screen)
            return
        pygame.draw.polygon(screen, self.color, self.linePoints)

    def draw_circle(self, screen):
        for point in self.linePoints:
            pygame.draw.circle(screen, self.color, point, 5)


plusX = screenWidth // 2
plusY = screenHeight // 2


def draw_flat_line(screen, x1, y1, length, color):
    for x in range(x1, x1 + length):
        pygame.gfxdraw.pixel(screen, x, y1, color)


def draw_vertical_line(screen, x1, y1, length, color):
    for y in range(y1, y1 + length):
        pygame.gfxdraw.pixel(screen, x1, y, color)


def draw_plus_sign(screen, x, y, size, color):
    draw_flat_line(screen, x - (size // 2), y, size, color)
    draw_vertical_line(screen, x, y - (size // 2), size, color)


# add our colors
rainbowPalette = [(67, 121, 43), (81, 146, 126), (55, 59, 86),
                  (57, 36, 67), (83, 57, 92), (126, 28, 61),
                  (148, 47, 37), (173, 50, 6), (188, 84, 29),
                  (164, 118, 41), (197, 190, 20)]


# create our lines of lines with a first new, empty line
lines = [Line()]

DRAW_LINES = 1
DRAW_SHAPE = 2
DRAW_CIRCLES = 3

while running:
    screen.fill(black)

    if pygame.mouse.get_focused():
        plusX, plusY = pygame.mouse.get_pos()

    draw_plus_sign(screen, plusX, plusY, 15, white)

    # Make sure we check which keys are being pressed
    key = pygame.key.get_pressed()

    # Keys 1 - 3 change the shapes for the current line's drawing mode
    if key[pygame.K_1]:
        lines[-1].draw_mode = DRAW_LINES

    if key[pygame.K_2]:
        lines[-1].draw_mode = DRAW_SHAPE

    if key[pygame.K_3]:
        lines[-1].draw_mode = DRAW_CIRCLES

    for line in lines:
        line.draw(screen)

    for event in pygame.event.get():
        # our mouse click gets checked here
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                lines[-1].add_linepoint(plusX, plusY)

            if event.button == 3:  # right click, new line
                newLine = Line()
                newLine.add_linepoint(plusX, plusY)
                lines.append(newLine)

        # if you try to quit, let's leave this loop
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick()
