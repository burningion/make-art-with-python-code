import pygame
import pygame.gfxdraw

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

    def __repr__(self):
        if not self.is_line():
            return "Not a line yet."

        return "Line from %s to %s" % (self.linePoints[0], self.linePoints[-1])

    def is_line(self):
        if len(self.linePoints) > 1:
            return True
        return False

    def add_linepoint(self, x, y):
        self.linePoints.append((x, y))

    def draw_line(self, screen):
        # if we're not a line yet, don't draw!
        if not self.is_line():
            return
        for place, point in enumerate(self.linePoints):
            # skip the first point, there won't be something
            # before it
            if place == 0:
                continue
            pygame.draw.line(screen, white, point, self.linePoints[place - 1])


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


# create our lines of lines with a first new, empty line
lines = [Line()]

while running:
    screen.fill(black)

    if pygame.mouse.get_focused():
        plusX, plusY = pygame.mouse.get_pos()

    draw_plus_sign(screen, plusX, plusY, 15, white)

    for line in lines:
        line.draw_line(screen)

    for event in pygame.event.get():
        # our mouse click gets checked here
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click, add line point
                lines[-1].add_linepoint(plusX, plusY)

            if event.button == 3:  # right click, new line and linepoint
                newLine = Line()
                newLine.add_linepoint(plusX, plusY)
                lines.append(newLine)

        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick()
