# importing the required libraries
import numpy as np
import math

# control points of the Bezier surface
CP = np.array([[[0, 0, 0 ], [0, 15, 15],[0, 15, -10], [0, 30, 5 ]],
               [[15, 0, 15], [15, 15, -10],[15, 15, 5 ], [15, 30, 0 ]],
               [[15, 0, -10 ], [15, 15, 5 ],[15, 15, 0 ], [15, 30, 15 ]],
               [[30, 0, 5 ], [30, 15, 0 ],[30, 15, 15 ], [30, 30, 0]]])
# Printer parameters and max and min layer height
bedWidth=300
Nozzle_diameter = 0.5
scale_z = 1 # sor scalling the z corrdinates
min_layer_height = Nozzle_diameter*0.1
max_layer_height = Nozzle_diameter*0.75
u_increments = 51

# make a copy from Bezier surface control points to use it for the projected surface
PCP = CP.copy()
lines = [] # define an empty list to append the coordinates
max_y_dist = [] # define an emptu list which will be used to calculate the amount and number of Y incremets

#defining some variables
x1 = 0
y1 = 0
z1 = 0
x0 = 0
y0 = 0
z0 = 0
v = 0
V = 0
t = 0

# for loop to find the amount of each u increment
for i in range(0,4):
    for j in range(0,4):
        max_y_dist.append(CP[i][j][1])
v_increments=(abs(max(max_y_dist))+abs(min(max_y_dist)))/Nozzle_diameter
v_increments=math.floor(v_increments)
# Make sure that the v_increments is even number
if (v_increments%2==0):
    pass
else:
    v_increments-=1

# apply scalling for Z corrdinates
for i in range(0,4):
    for j in range(0, 4):
        CP[i][j][2] = CP[i][j][2]*scale_z

# Make all Z values equal to 0 for the projected surface
for k in range(0,4):
    for p in range(0, 4):
        PCP[k][p][2] = 0

# defiining some variables
Z_max = 0
x_zmax = 0
y_zmax =0
Max_Height_of_top_layer = 0
Max_Distance_between_layers = Nozzle_diameter
t=1
currnet_loop = 0

# Calculating the number of layers required to build the the part
while (Max_Distance_between_layers>max_layer_height):
    for V in range(0,v_increments): # The range must be odd for example 60 NOT 61
        v = 1 - V/(v_increments-1)
        for u in np.linspace(1, 0, u_increments):
            x1, y1, z1 = pow(1.0-v, 3) * (pow(1.0-u, 3) * ((1-t) * PCP[0][0] + t * CP[0][0]) + 3.0 * u * pow(1.0-u, 2) * ((1-t) * PCP[1][0] + t * CP[1][0]) + 3.0 * pow(u, 2) * (1-u) * ((1-t) * PCP[2][0] + t * CP[2][0]) + pow(u, 3) * ((1-t) * PCP[3][0] + t * CP[3][0]))       +        3.0 * v * pow(1-v, 2) * (pow(1-u, 3) * ((1-t) * PCP[0][1] + t * CP[0][1]) + 3.0 * u * pow(1-u, 2) * ((1-t) * PCP[1][1] + t * CP[1][1]) + 3.0 * pow(u, 2) * (1-u) * ((1-t) * PCP[2][1] + t * CP[2][1]) + pow(u, 3) * ((1-t) * PCP[3][1] + t * CP[3][1]))        +         3.0 * (1-v) * pow(v, 2) * (pow(1-u, 3) * ((1-t) * PCP[0][2] + t * CP[0][2]) + 3.0 * u * pow(1-u, 2) * ((1-t) * PCP[1][2] + t * CP[1][2]) + 3.0 * pow(u, 2) * (1-u) * ((1-t) * PCP[2][2] + t * CP[2][2]) + pow(u, 3) * ((1-t) * PCP[3][2] + t * CP[3][2]))      +      pow(v, 3) * (pow(1-u, 3) * ((1-t) * PCP[0][3] + t * CP[0][3]) + 3.0 * u * pow(1-u, 2) * ((1-t) * PCP[1][3] + t * CP[1][3]) + 3.0 * pow(u, 2) * (1-u) * ((1-t) * PCP[2][3] + t * CP[2][3]) + pow(u, 3) * ((1-t) * PCP[3][3] + t * CP[3][3]))
            if (z1 > Z_max):
                Z_max = z1
                x_zmax = u
                y_zmax = v
    if (currnet_loop==0):
        Max_Height_of_top_layer = Z_max
        t=0
    else:
        Max_Distance_between_layers = Max_Height_of_top_layer - Z_max + min_layer_height
    Z_max=0
    t += 0.01
    currnet_loop +=1

# number of layers
Layers = math.ceil(1/(1-t))
print("Estimated max layer height: ", Max_Distance_between_layers)
print("Number of layer to be printed: ", Layers)

# adding offset to the Bezier surface to avoid printing layers with 0 thickness
for i in range(0,4):
    for j in range(0, 4):
        CP[i][j][2] = CP[i][j][2] + min_layer_height * Layers

# Redifingin the variables Or resit the variables to be 0
v = 0
V = 0
t = 0

# Starting the Layer for loop
for NOL in range(0, Layers):
    lines.append([])
    # Calculating the t value using the number of layers and the current layer
    t = NOL / (Layers - 1)

    # Starting the v for loop
    for V in range(0,v_increments): # The range must be odd for example 60 NOT 61
        # this will allow to start at the same Y coordinate when switching to new layer
        if (NOL % 2) != 0:
            v = 1 - V/(v_increments-1)
        else:
            v = V/(v_increments-1)
        lines[NOL].append([])

        # Starting the u for loop
        for u in np.linspace(1, 0, u_increments):
            # this will allow to start at the same X coordinate when switching to new line
            if (V % 2) == 0:
                u = 1 - u
            # calculating the corrdinates using the general equation 3.4.3 in the report
            x1, y1, z1 = pow(1.0-v, 3) * (pow(1.0-u, 3) * ((1-t) * PCP[0][0] + t * CP[0][0]) + 3.0 * u * pow(1.0-u, 2) * ((1-t) * PCP[1][0] + t * CP[1][0]) + 3.0 * pow(u, 2) * (1-u) * ((1-t) * PCP[2][0] + t * CP[2][0]) + pow(u, 3) * ((1-t) * PCP[3][0] + t * CP[3][0]))       +        3.0 * v * pow(1-v, 2) * (pow(1-u, 3) * ((1-t) * PCP[0][1] + t * CP[0][1]) + 3.0 * u * pow(1-u, 2) * ((1-t) * PCP[1][1] + t * CP[1][1]) + 3.0 * pow(u, 2) * (1-u) * ((1-t) * PCP[2][1] + t * CP[2][1]) + pow(u, 3) * ((1-t) * PCP[3][1] + t * CP[3][1]))        +         3.0 * (1-v) * pow(v, 2) * (pow(1-u, 3) * ((1-t) * PCP[0][2] + t * CP[0][2]) + 3.0 * u * pow(1-u, 2) * ((1-t) * PCP[1][2] + t * CP[1][2]) + 3.0 * pow(u, 2) * (1-u) * ((1-t) * PCP[2][2] + t * CP[2][2]) + pow(u, 3) * ((1-t) * PCP[3][2] + t * CP[3][2]))      +      pow(v, 3) * (pow(1-u, 3) * ((1-t) * PCP[0][3] + t * CP[0][3]) + 3.0 * u * pow(1-u, 2) * ((1-t) * PCP[1][3] + t * CP[1][3]) + 3.0 * pow(u, 2) * (1-u) * ((1-t) * PCP[2][3] + t * CP[2][3]) + pow(u, 3) * ((1-t) * PCP[3][3] + t * CP[3][3]))
            lines[NOL][V].append([x1, y1, z1])

# open new file to start writing to it the Gcode instructions
f = open("Curve_tool_path" + ".gcode", 'w')
# the following lines are instruction for the printer
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

# Calculating the middle of the build platform
origin = bedWidth / 2  # origin
layer = 1  # current layer/slice
E1 = 0  # extrusion accumulator
extrusionImplifier = 1

# defining variables
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
# Creating an empty list to be use to stor the max distance between layers
CheckMaxHeight = []

# staritng the for loop to writing the position coordinates to the Gcode file
for line in lines:
    f.write(";Layer " + str(layer) + " of " + str(len(lines)) + "\n")
    # fan
    if (layer == 2):
        f.write("M106 S127\n")
    if (layer == 3):
        f.write("M106 S255\n")

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
                    yDist = abs(py2 - py1)

                # the following code used to increase the amount of material extruded for the first layers to make sure it sticks on the bed
                if (layer == 1):
                    extrusionImplifier = 1
                elif (layer == 2):
                    extrusionImplifier = 1
                else:
                    extrusionImplifier = 1

                if (layer>1):
                    # move to the new positon without extruding
                    f.write("G0 F1000 X" + str(origin + px0) + " Y" + str(origin + py0) + " Z" + str(pz0) + "\n")
                    px00, py00, pz00 = lines[layer - 2][-indexOfLine-1][(-indexOfPoints-1)]
                    px10, py10, pz10 = lines[layer - 2][-indexOfLine-1][(-indexOfPoints-2)]
                    # calculaitg the Z distance
                    zdist = (abs(pz0 - pz00) + abs(pz1 - pz10)) / 2
                    CheckMaxHeight.append(zdist)
                    # calculating the travel destance
                    dist = math.sqrt(pow(px1 - px0, 2) + pow(py1 - py0, 2) + pow(pz1 - pz0, 2))
                    #calculating the area of the section
                    area = (yDist - zdist) * zdist + math.pi * (zdist / 2) * (zdist / 2)
                    # calculating the amoult of the filimant to be fed into the nozzle
                    E1 += (area * dist * 4)/(math.pi *  1.75 * 1.75 * extrusionImplifier)
                    # writing the instruction to the Gcode file
                    f.write("G1 F1000 X" + str(origin + px1) + " Y" + str(origin + py1) + " Z" + str(pz1) + " E" + str(E1) + "\n")
            indexOfPoints += 1
        indexOfLine += 1
        indexOfPoints = 0
    indexOfLine = 0
    layer += 1

# printing the max and min layer thickness of the part
print("Max layer thickness is: ",max(CheckMaxHeight))
print("Min layer thickness is: ",min(CheckMaxHeight))
# some instruction at the end of the printing process
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
