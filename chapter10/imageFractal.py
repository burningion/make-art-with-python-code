import PIL
from PIL import Image, ImageOps

from math import cos, sin, radians, sqrt

def rotatePoint(x1, y1, x2, y2, rotate):
    '''
    Rotates around x1, y2 by rotate degrees
    '''
    inRadians = radians(rotate)
    nx = cos(inRadians) * (x1 - x2) - sin(inRadians) * (y1 - y2) + x2
    ny = sin(inRadians) * (x1 - x2) + cos(inRadians) * (y1 - y2) + y2

    return int(nx), int(ny)

# Let's set up our command line arguments
import argparse
parser = argparse.ArgumentParser(description="Image flipper")
parser.add_argument('-i', '--image', help='Filename of input image')
parser.add_argument('-o', '--output', help="Output file", default='output.jpg')
parser.add_argument('-r', '--rotate', help="Rotation in degrees", default=0)
passedIn = parser.parse_args()

# Output image size
finalSize = 1024, 1024
centerPoint = 512, 512
# Input image resize
size = 1024, 1024

# Open our passed in image filename
im = Image.open(passedIn.image)

# Resize it to the size above, using a resize algorithm called LANCZOS
im = im.resize(size, PIL.Image.LANCZOS).rotate(float(passedIn.rotate))
im = im.convert('RGBA')
# Create a new blank RGB image
out = Image.new('RGBA', finalSize)

# Paste in the first rescaled image at top left corner (0,0)
out.paste(im)

topLeftX = 0
topLeftY = 0
rotation = 0
for i in range(34):
    topLeftX += 5
    topLeftY += 5
    rotation -= 5
    curr = im.resize((int(size[0] - sqrt(topLeftX)), int(size[1] - sqrt(topLeftY))), PIL.Image.LANCZOS)
    curr = curr.rotate(rotation)
    
    out.paste(curr, rotatePoint(topLeftX, topLeftY, centerPoint[0], centerPoint[1], rotation), curr)
# Save the image out

doubleOut = Image.new('RGB', (finalSize[0] * 2, finalSize[1] * 2))
doubleOut.paste(out, (0,0))
doubleOut.paste(ImageOps.mirror(out), (1024, 0))
doubleOut.paste(ImageOps.mirror(out.rotate(180)), (0, 1024))
doubleOut.paste(out.rotate(180), (1024, 1024))
doubleOut.save(passedIn.output)
