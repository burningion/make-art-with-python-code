from subprocess import call

for i in range(360):
    print('Doing number %i', i)
    call(['python3', 'imageFractal.py', '-i', 'brooklyn.jpeg', '-o', 'output/' + str(i) + '.jpg', '-r', str(i)])
