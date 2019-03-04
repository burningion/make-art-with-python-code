import pygame
pygame.init()
screenWidth, screenHeight = 1024, 1024

from math import cos, sin, radians, sqrt, pi

def rotatePoint(x1, y1, x2, y2, rotate):
    '''
    Rotates around x1, y2 by rotate degrees
    '''
    inRadians = radians(rotate)
    nx = cos(inRadians) * (x1 - x2) - sin(inRadians) * (y1 - y2) + x2
    ny = sin(inRadians) * (x1 - x2) + cos(inRadians) * (y1 - y2) + y2

    return int(nx), int(ny)

import argparse
parser = argparse.ArgumentParser(description="Image flipper")
parser.add_argument('-i', '--image', help='Filename of input image')
parser.add_argument('-o', '--output', help="Output file", default='output.jpg')
parser.add_argument('-r', '--rotate', help="Rotation in degrees", default=2)
passedIn = parser.parse_args()

screen = pygame.display.set_mode((800, 600))

newImage = pygame.image.load(passedIn.image)
blankImage = newImage.copy()


# Set transparency after load
newImage = newImage.convert_alpha()
blankImage = blankImage.convert_alpha()

imageWidth = newImage.get_width()
imageHeight = newImage.get_height()
# Scale image to fit
scaler = 10
rotate = float(passedIn.rotate)
for i in range(60):
    scaled = pygame.transform.scale(newImage, [int(imageWidth - sqrt(scaler)), int(imageHeight - sqrt(imageHeight))])

    blankImage.blit(pygame.transform.rotate(scaled, sqrt(rotate)), rotatePoint(scaler, scaler, imageWidth // 2, imageHeight // 2, sqrt(rotate)))
    scaler += 10
    rotate += rotate

# comment out the first save
# pygame.image.save(blankImage, passedIn.output)
doubleOut = pygame.Surface((imageWidth * 2, imageHeight * 2))
doubleOut.blit(blankImage, (0,0))
doubleOut.blit(pygame.transform.flip(blankImage, True, False), (imageWidth, 0))
doubleOut.blit(pygame.transform.flip(pygame.transform.rotate(blankImage, 180), True, False), (0, imageHeight))
doubleOut.blit(pygame.transform.rotate(blankImage, 180), (imageWidth, imageHeight))

# and get rid of the mirror_ prefix
pygame.image.save(doubleOut, passedIn.output)
