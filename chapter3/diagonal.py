import pygame
import pygame.gfxdraw

pygame.init()

screenWidth = 800
screenHeight = 800

screen = pygame.display.set_mode((screenWidth, screenHeight))

white = (255, 255, 255)
black = (0, 0, 0)

running = True

while running:
    # fill the screen with black
    screen.fill(black)

    # Our for loop, for the width of the screen
    for i in range(0, screenWidth):
        # Our pixel draw function uses i to know the current value
        pygame.gfxdraw.pixel(screen, i, i, white)
        pygame.gfxdraw.pixel(screen, i, screenHeight - i, white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
