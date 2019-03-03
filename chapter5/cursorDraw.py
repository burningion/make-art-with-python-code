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


def draw_flat_line(screen, x1, y1, length, color):
    for x in range(x1, x1 + length):
        pygame.gfxdraw.pixel(screen, x, y1, color)


def draw_vertical_line(screen, x1, y1, length, color):
    for y in range(y1, y1 + length):
        pygame.gfxdraw.pixel(screen, x1, y, color)


def draw_plus_sign(screen, x, y, size, color):
    draw_flat_line(screen, x - (size // 2), y, size, color)
    draw_vertical_line(screen, x, y - (size // 2), size, color)


# set the start points to the center of the screen
plusX = screenWidth // 2
plusY = screenHeight // 2

# Add a new list before our loop starts
# Otherwise, the list gets forgotten every
# time the loop completes
cursorList = []

while running:
    screen.fill(black)

    draw_plus_sign(screen, plusX, plusY, 15, white)

    # loop over each of our cursor positions. if empty, skips
    for plusSign in cursorList:
        draw_plus_sign(screen, plusSign[0], plusSign[1], 10, white)

    key = pygame.key.get_pressed()

    # add our new check for the SPACEBAR
    if key[pygame.K_SPACE]:
        # take the current position of the cursor
        # and create a list holding x and y
        newPlace = [plusX, plusY]

        # add that list to our cursorList
        cursorList.append(newPlace)

    # check if our key is pressed, change the right value
    if key[pygame.K_UP]:
        plusY = plusY - 1
    elif key[pygame.K_DOWN]:
        plusY = plusY + 1
    if key[pygame.K_LEFT]:
        plusX = plusX - 1
    elif key[pygame.K_RIGHT]:
        plusX = plusX + 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(90)
