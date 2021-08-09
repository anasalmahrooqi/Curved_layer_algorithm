
import numpy as np
import math

lines = []

LayerHeight = 0.1
Layers = 30

x1 = 0
y1 = 0
z1 = 0
x0 = 0
y0 = 0
z0 = 0

v = 0
V = 0
t = 0

for NOL in range(0, Layers):
    lines.append([])
    t = NOL / (Layers - 1)

    CP = np.array([[[0, 0,   0 + LayerHeight*Layers], [0, 15,    15 + LayerHeight*Layers], [0, 15,    -10 + LayerHeight*Layers], [0, 30, 5 + LayerHeight*Layers]],
                   [[15, 0, 15 + LayerHeight*Layers], [15, 15, -10 + LayerHeight*Layers], [15, 15, 5 + LayerHeight*Layers], [15, 30, 0 + LayerHeight*Layers]],
                   [[15, 0,  -10 + LayerHeight*Layers], [15, 15,  5 + LayerHeight*Layers], [15, 15,  0 + LayerHeight*Layers], [15, 30, 15 + LayerHeight*Layers]],
                   [[30, 0, 5 + LayerHeight*Layers], [30, 15, 0 + LayerHeight*Layers], [30, 15, 15 + LayerHeight*Layers], [30, 30, 0 + LayerHeight*Layers]]])

    PCP = np.array([[[0, 0, LayerHeight], [0, 15, LayerHeight], [0, 15, LayerHeight], [0, 30, LayerHeight]],
                    [[15, 0, LayerHeight], [15, 15, LayerHeight], [15, 15, LayerHeight], [15, 30, LayerHeight]],
                    [[15, 0, LayerHeight], [15, 15, LayerHeight], [15, 15, LayerHeight], [15, 30, LayerHeight]],
                    [[30, 0, LayerHeight], [30, 15, LayerHeight], [30, 15, LayerHeight], [30, 30, LayerHeight]]])

    for V in range(0,60): # The range must be odd for example 60 NOt 61
        if (NOL % 2) != 0:
            v = 1 - V/59
        else:
            v = V/59
        # print(v)
        lines[NOL].append([])

        for u in np.linspace(1, 0, 51):
            if (V % 2) == 0:
                u = 1 - u

            x1, y1, z1 = pow(1.0-v, 3) * (pow(1.0-u, 3) * ((1-t) * PCP[0][0] + t * CP[0][0]) + 3.0 * u * pow(1.0-u, 2) * ((1-t) * PCP[1][0] + t * CP[1][0]) + 3.0 * pow(u, 2) * (1-u) * ((1-t) * PCP[2][0] + t * CP[2][0]) + pow(u, 3) * ((1-t) * PCP[3][0] + t * CP[3][0]))       +        3.0 * v * pow(1-v, 2) * (pow(1-u, 3) * ((1-t) * PCP[0][1] + t * CP[0][1]) + 3.0 * u * pow(1-u, 2) * ((1-t) * PCP[1][1] + t * CP[1][1]) + 3.0 * pow(u, 2) * (1-u) * ((1-t) * PCP[2][1] + t * CP[2][1]) + pow(u, 3) * ((1-t) * PCP[3][1] + t * CP[3][1]))        +         3.0 * (1-v) * pow(v, 2) * (pow(1-u, 3) * ((1-t) * PCP[0][2] + t * CP[0][2]) + 3.0 * u * pow(1-u, 2) * ((1-t) * PCP[1][2] + t * CP[1][2]) + 3.0 * pow(u, 2) * (1-u) * ((1-t) * PCP[2][2] + t * CP[2][2]) + pow(u, 3) * ((1-t) * PCP[3][2] + t * CP[3][2]))      +      pow(v, 3) * (pow(1-u, 3) * ((1-t) * PCP[0][3] + t * CP[0][3]) + 3.0 * u * pow(1-u, 2) * ((1-t) * PCP[1][3] + t * CP[1][3]) + 3.0 * pow(u, 2) * (1-u) * ((1-t) * PCP[2][3] + t * CP[2][3]) + pow(u, 3) * ((1-t) * PCP[3][3] + t * CP[3][3]))

            lines[NOL][V].append([x1, y1, z1])


f = open("test3" + ".gcode", 'w')
f.write("M109 S210.000000\n")
f.write(";Start GCode\n")
f.write("G28 X0 Y0 Z0\n")
f.write("G92 E0\n")
f.write("G29\n")

f.write("M82 ;absolute extrusion mode\n")
f.write("M201 X500.00 Y500.00 Z100.00 E5000.00 ;Setup machine max acceleration\n")
f.write("M203 X500.00 Y500.00 Z10.00 E50.00 ;Setup machine max feedrate\n")
f.write("M204 P500.00 R1000.00 T500.00 ;Setup Print/Retract/Travel acceleration\n")
f.write("M205 X8.00 Y8.00 Z0.40 E5.00 ;Setup Jerk\n")
f.write("M220 S100 ;Reset Feedrate\n")
f.write("M221 S100 ;Reset Flowrate\n")

f.write("G92 E0 ;Reset Extruder\n")
f.write("G1 Z2.0 F3000 ;Move Z Axis up\n")
f.write("G1 X10.1 Y20 Z0.28 F5000.0 ;Move to start position\n")
f.write("G1 X10.1 Y200.0 Z0.28 F1500.0 E15 ;Draw the first line\n")
f.write("G1 X10.4 Y200.0 Z0.28 F5000.0 ;Move to side a little\n")
f.write("G1 X10.4 Y20 Z0.28 F1500.0 E30 ;Draw the second line\n")
f.write("G92 E0 ;Reset Extruder\n")
f.write("G1 Z2.0 F3000 ;Move Z Axis up\n")

bedWidth=300
extrudeRate = 0.05
extrudeRate2 = 0.2857
origin = bedWidth / 2  # origin
layer = 1  # current layer/slice
E = 0  # extrusion accumulator
E1 = 0  # extrusion accumulator
layerHeight=0.2
CurrentLayer=0
extrusionImplifier = 1

px00=0
py00=0
pz00=0
px10=0
py10=0
pz10=0
px2=0
py2=0
pz2=0


indexOfPoints = 0
indexOfLine = 0
print(lines[0])
print(lines[1])
print(lines[2])
print(lines[3])

CheckMaxHeight = []

for line in lines:

    f.write(";Layer " + str(layer) + " of " + str(len(lines)) + "\n")

    # fan
    if (layer == 2):
        f.write("M106 S127\n")
    if (layer == 3):
        f.write("M106 S255\n")
    # print(line)

    for points in line:
        for px0,py0,pz0 in points:

            if ((len(points) - 1) == indexOfPoints):
                pass
            else:
                px1, py1, pz1 = points[indexOfPoints+1]

                if ((len(line) - 1) == indexOfLine):
                    pass
                else:
                    px2, py2, pz2 = line[indexOfLine+1][0]
                    print(abs(py2 - py1))
                    yDist = abs(py2 - py1)



                # move to start of line
                f.write("G0 F1000 X" + str(origin + px0) + " Y" + str(origin + py0) + " Z" + str(pz0) + "\n")
                # move to end while extruding
                if (layer == 1):
                    extrusionImplifier = 1
                elif (layer == 2):
                    extrusionImplifier = 1
                else:
                    extrusionImplifier = 1

                if (layer>1):
                    px00, py00, pz00 = lines[layer - 2][-indexOfLine-1][(-indexOfPoints-1)]
                    px10, py10, pz10 = lines[layer - 2][-indexOfLine-1][(-indexOfPoints-2)]

                zdist = (abs(pz0 - pz00) + abs(pz1 - pz10)) / 2
                # print(px00, py00, pz00, px10, py10, pz10)
                # print(px0, py0, pz0, px1, py1, pz1)
                CheckMaxHeight.append(zdist)
                # print(zdist)
                dist = math.sqrt(pow(px1 - px0, 2) + pow(py1 - py0, 2) + pow(pz1 - pz0, 2))
                # print(dist)
                area = (yDist - zdist) * zdist + math.pi * (zdist / 2) * (zdist / 2)
                # area = 0.4*zdist
                # print(area)
                E1 += (area * dist * 4)/(math.pi *  1.75 * 1.75 * extrusionImplifier)
                # E1 += ((0.5*zdis*dist)/((math.pi*0.25*0.25)))*extrudeRate*2.5
                E += dist * extrudeRate * (0.5 + (pz1 / (LayerHeight * layer)))

                # print((area*dist * 4) / (math.pi * 1.75 * 1.75 * extrusionImplifier))
                # print((area * dist * 4)/(math.pi *  1.75 * 1.75 * extrusionImplifier))
                # print("  ")
                # print((area*dist*4)/(math.pi*1.75*1.75*extrusionImplifier))
                # print(dist * extrudeRate * (0.5 + (pz1/(maxLayerHeight*layer))))
                # print(dist)
                # E += dist * extrudeRate
                f.write("G1 F600 X" + str(origin + px1) + " Y" + str(origin + py1) + " Z" + str(pz1) + " E" + str(E1) + "\n")
            indexOfPoints += 1
        indexOfLine += 1
        indexOfPoints = 0
    indexOfLine = 0
    layer += 1
    # print(layer)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

# print(len(lines))

print("Max layer thickness is: ",max(CheckMaxHeight))
print("Min layer thickness is: ",min(CheckMaxHeight))
#postamble
f.write("M140 S0\n")
f.write("M107\n")
f.write("G91 ;Relative positioning\n")
f.write("G1 E-2 F2700 ;Retract a bit\n")
f.write("G1 E-2 Z0.2 F2400 ;Retract and raise Z\n")
f.write("G1 Z10 ;Raise Z more\n")
f.write("G90 ;Absolute positionning\n")
f.write("M106 S0 ;Turn-off fan\n")
f.write("M104 S0 ;Turn-off hotend\n")
f.write("M140 S0 ;Turn-off bed\n")
f.write("M84 X Y E ;Disable all steppers but Z\n")
f.write("M82 ;absolute extrusion mode\n")
f.write("M104 S0\n")
f.write(";End of Gcode\n")