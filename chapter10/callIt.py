import argparse
parser = argparse.ArgumentParser(description="Image flipper animator")
parser.add_argument('-i', '--image', help='Filename of input image')
passedIn = parser.parse_args()

from subprocess import call
import os

# if there isn't a directory called output, make it
# all the images will go there
if not os.path.isdir('output/'):
    call('mkdir output'.split(' '))

# for now let's start at 0 and go through a perfect loop
for i in range(360):
    print('Doing number %i', i)
    callString = 'python3 imageFractalPygame.py -i ' + passedIn.image + ' -o output/' + str(i) + '.jpg -r ' + str(i)
    call(callString.split(' '))

# after we're done, turn it into a movie using this command
# ffmpeg -i %d.jpg -profile:v high -level 4.0 -strict -2 out.mp4

call(['ffmpeg', '-i', 'output/%d.jpg', '-profile:v', 'high', '-level', '4.0', '-strict', '-2', 'out.mp4'])
