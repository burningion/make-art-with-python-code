from pyx import *
import pickle 
unit.set(wscale=10)

doubleArray = pickle.load(open('./out.pkl', 'rb'))
print(doubleArray)
c = canvas.canvas()

p = path.line(doubleArray[0][0], doubleArray[0][1], doubleArray[1][0], doubleArray[1][1])
for place, point in enumerate(doubleArray):
    if place == 0 or place == 1:
        continue
    p.pathitems.append(path.lineto(doubleArray[place][0], doubleArray[place][1]))

p.append(path.closepath())
print(p)
c.stroke(p, [trafo.mirror(180), style.linewidth.THIN])
#c.fill(p)

cc = canvas.canvas()
for i in range(10):
    for j in range(10):
        cc.insert(c, [trafo.translate(i * 73, j * 73)])
        '''
        if j % 2 == 0:
            if (i + 1) % 2 == 0:
                cc.insert(c, [trafo.translate(i * 145, j * 145), color.rgb.blue])
            else:
                cc.insert(c, [trafo.translate(i * 145, j * 145), color.rgb.green])
        else:
            if (i + 1) % 2 == 0:
                cc.insert(c, [trafo.translate(i * 145, j * 145), color.rgb.green])
            else:
                cc.insert(c, [trafo.translate(i * 145, j * 145), color.rgb.blue])
        '''
c.writePDFfile("addjoin")
c.writeSVGfile("addjoin")
c.writeEPSfile("addjoin")
cc.writePDFfile("totally")
cc.writeSVGfile("totally")
